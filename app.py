
from flask import Flask
from config import Config
from extensions import mysql
from routes.student_routes import student_bp

app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize MySQL
mysql.init_app(app)

# Register all student routes
app.register_blueprint(student_bp)


if __name__ == "__main__":
    app.run(debug=True)
