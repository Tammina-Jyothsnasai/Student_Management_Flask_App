
import csv
import re
from io import StringIO

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response
)

from extensions import mysql

student_bp = Blueprint("students", __name__)


# Fetch one student
def get_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT id, name, email, phone, status
        FROM students
        WHERE id = %s
        """,
        (student_id,)
    )
    student = cur.fetchone()
    cur.close()
    return student


# Validate student details
def validate_student(name, email, phone, exclude_id=None):
    errors = []

    name = name.strip()
    email = email.strip().lower()
    phone = phone.strip()

    if not name or len(name) > 100:
        errors.append("Enter a name between 1 and 100 characters.")

    if (
        not email
        or len(email) > 150
        or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)
    ):
        errors.append("Enter a valid email address.")

    if not re.fullmatch(r"[0-9]{7,15}", phone):
        errors.append("Phone number must contain 7 to 15 digits.")

    if errors:
        return errors

    cur = mysql.connection.cursor()

    if exclude_id is None:
        cur.execute(
            "SELECT id FROM students WHERE email = %s OR phone = %s",
            (email, phone)
        )
    else:
        cur.execute(
            """
            SELECT id FROM students
            WHERE (email = %s OR phone = %s) AND id != %s
            """,
            (email, phone, exclude_id)
        )

    duplicate = cur.fetchone()
    cur.close()

    if duplicate:
        errors.append(
            "This email address or phone number is already registered."
        )

    return errors


# Dashboard, search and pagination
@student_bp.route("/")
def home():
    search = request.args.get("search", "").strip()
    page = max(request.args.get("page", 1, type=int) or 1, 1)

    per_page = 10
    offset = (page - 1) * per_page
    cur = mysql.connection.cursor()

    if search:
        pattern = f"%{search}%"

        cur.execute(
            """
            SELECT COUNT(*) FROM students
            WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s
            """,
            (pattern, pattern, pattern)
        )
        total_matching = cur.fetchone()[0]

        cur.execute(
            """
            SELECT id, name, email, phone, status
            FROM students
            WHERE name LIKE %s OR email LIKE %s OR phone LIKE %s
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            """,
            (pattern, pattern, pattern, per_page, offset)
        )
    else:
        cur.execute("SELECT COUNT(*) FROM students")
        total_matching = cur.fetchone()[0]

        cur.execute(
            """
            SELECT id, name, email, phone, status
            FROM students
            ORDER BY id DESC
            LIMIT %s OFFSET %s
            """,
            (per_page, offset)
        )

    students = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM students WHERE status = %s",
        ("Active",)
    )
    active_records = cur.fetchone()[0]

    cur.execute(
        """
        SELECT COUNT(*) FROM students
        WHERE email IS NOT NULL AND email != ''
        """
    )
    email_records = cur.fetchone()[0]

    cur.close()

    total_pages = max(
        1, (total_matching + per_page - 1) // per_page
    )

    if page > total_pages:
        return redirect(
            url_for("students.home", search=search, page=total_pages)
        )

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        active_records=active_records,
        email_records=email_records,
        search=search,
        page=page,
        total_pages=total_pages,
        total_matching=total_matching,
        start_record=offset + 1 if total_matching else 0,
        end_record=min(offset + len(students), total_matching)
    )


# Add student
@student_bp.route("/students/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        errors = validate_student(name, email, phone)

        if errors:
            for error in errors:
                flash(error, "danger")

            return render_template(
                "add_student.html",
                student={"name": name, "email": email, "phone": phone}
            )

        cur = mysql.connection.cursor()

        try:
            cur.execute(
                """
                INSERT INTO students (name, email, phone)
                VALUES (%s, %s, %s)
                """,
                (name, email, phone)
            )
            mysql.connection.commit()
            flash("Student added successfully!", "success")

        except Exception:
            mysql.connection.rollback()
            flash(
                "Could not add student. Check the database and "
                "ensure the email and phone are unique.",
                "danger"
            )
            return render_template(
                "add_student.html",
                student={"name": name, "email": email, "phone": phone}
            )

        finally:
            cur.close()

        return redirect(url_for("students.home"))

    return render_template(
        "add_student.html",
        student={"name": "", "email": "", "phone": ""}
    )


# View student
@student_bp.route("/students/<int:student_id>")
def view_student(student_id):
    student = get_student(student_id)

    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("students.home"))

    return render_template("view_student.html", student=student)


# Edit student
@student_bp.route(
    "/students/<int:student_id>/edit",
    methods=["GET", "POST"]
)
def edit_student(student_id):
    student = get_student(student_id)

    if not student:
        flash("Student not found.", "warning")
        return redirect(url_for("students.home"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()

        errors = validate_student(
            name, email, phone, exclude_id=student_id
        )

        if errors:
            for error in errors:
                flash(error, "danger")

            student = (
                student_id, name, email, phone, student[4]
            )
            return render_template("edit_student.html", student=student)

        cur = mysql.connection.cursor()

        try:
            cur.execute(
                """
                UPDATE students
                SET name = %s, email = %s, phone = %s
                WHERE id = %s
                """,
                (name, email, phone, student_id)
            )
            mysql.connection.commit()
            flash("Student details updated successfully!", "success")

        except Exception:
            mysql.connection.rollback()
            flash("Could not update the student.", "danger")
            student = (
                student_id, name, email, phone, student[4]
            )
            return render_template("edit_student.html", student=student)

        finally:
            cur.close()

        return redirect(url_for("students.home"))

    return render_template("edit_student.html", student=student)


# Change student status
@student_bp.route(
    "/students/<int:student_id>/status",
    methods=["POST"]
)
def change_status(student_id):
    new_status = request.form.get("status", "").strip()

    if new_status not in ("Active", "Inactive"):
        flash("Invalid student status.", "danger")
        return redirect(url_for("students.home"))

    cur = mysql.connection.cursor()

    try:
        cur.execute(
            """
            UPDATE students
            SET status = %s
            WHERE id = %s
            """,
            (new_status, student_id)
        )

        updated = cur.rowcount
        mysql.connection.commit()

        if updated:
            flash(f"Student status changed to {new_status}.", "success")
        else:
            flash("Student not found or status unchanged.", "info")

    except Exception:
        mysql.connection.rollback()
        flash("Could not update student status.", "danger")

    finally:
        cur.close()

    return redirect(url_for("students.home"))


# Delete student
@student_bp.route(
    "/students/<int:student_id>/delete",
    methods=["POST"]
)
def delete_student(student_id):
    cur = mysql.connection.cursor()

    try:
        cur.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )
        deleted = cur.rowcount
        mysql.connection.commit()

        if deleted:
            flash("Student deleted successfully.", "success")
        else:
            flash("Student not found.", "warning")

    except Exception:
        mysql.connection.rollback()
        flash("Could not delete the student.", "danger")

    finally:
        cur.close()

    return redirect(url_for("students.home"))


# Export students to CSV
@student_bp.route("/students/export")
def export_students():
    cur = mysql.connection.cursor()

    cur.execute(
        """
        SELECT id, name, email, phone, status
        FROM students
        ORDER BY id
        """
    )

    students = cur.fetchall()
    cur.close()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID", "Student Name", "Email Address",
        "Phone Number", "Status"
    ])
    writer.writerows(students)

    return Response(
        "\ufeff" + output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition":
                "attachment; filename=studenthub_students.csv"
        }
    )


# Test database connection
@student_bp.route("/db-test")
def db_test():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DATABASE()")
    database_name = cur.fetchone()[0]
    cur.close()

    return f"Connected successfully to: {database_name}"
