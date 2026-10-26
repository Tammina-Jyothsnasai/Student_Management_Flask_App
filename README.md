# Student Management System Using Flask

## Project Overview

The **Student Management System** is a web application developed using Python Flask to manage student information through a simple and user-friendly interface.

The application allows users to add new student records, view student details, update existing information, and delete records when required. It is designed to make student data management easier and more organized.

## Features

- **View Students:** Display student records in an organized format.
- **Add Students:** Enter and save new student information.
- **Edit Student Details:** Update existing student records.
- **View Individual Records:** Open a separate page to view a student's details.
- **Delete Student Records:** Remove student information when it is no longer needed.
- **User-Friendly Interface:** Navigate through the application using HTML templates and CSS styling.
- **Flask Routing:** Handle different student management operations through separate routes.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Backend web framework |
| HTML5 | Structure of web pages |
| CSS3 | Styling and page layout |
| Jinja2 | Dynamic rendering of HTML templates |
| Git and GitHub | Version control and project hosting |

## Project Structure

```text
Student_Management_Flask_App/
│
├── app.py
├── config.py
├── extensions.py
├── .gitignore
├── README.md
│
├── routes/
│   └── student_routes.py
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── add_student.html
    ├── edit_student.html
    └── view_student.html
```

## How the Application Works

1. The user opens the application in a web browser.
2. Flask receives the request and directs it to the appropriate route.
3. The student routes handle operations such as adding, viewing, editing, and deleting records.
4. HTML templates display the relevant pages.
5. CSS provides the styling and layout of the application.

## Installation and Setup

### Prerequisites

Make sure the following are installed on your system:

- Python 3
- pip
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Tammina-Jyothsnasai/Student_Management_Flask_App.git
```

### Step 2: Open the Project Folder

```bash
cd Student_Management_Flask_App
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

### Step 4: Install Dependencies

Install Flask:

```bash
pip install Flask
```

If the project uses additional Python packages, install those as well. If a `requirements.txt` file is available, use:

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python app.py
```

Open the local URL displayed in your terminal, commonly:

```text
http://127.0.0.1:5000/
```

## Learning Outcomes

Through this project, I gained practical experience in:

- Developing a web application using Python and Flask.
- Organizing application code using separate route files.
- Connecting backend logic with HTML templates.
- Designing web pages using HTML and CSS.
- Implementing basic CRUD operations for student records.
- Using Git and GitHub to manage and publish project code.

## Future Enhancements

- Add user authentication and authorization.
- Improve input validation and error handling.
- Add search and filtering options for student records.
- Improve the interface for mobile and tablet screens.
- Add automated testing for application routes.

## Author

**T. Jyothsna Sai**

GitHub: [Tammina-Jyothsnasai](https://github.com/Tammina-Jyothsnasai)

---

If you find this project useful, feel free to explore the repository and its source code.
