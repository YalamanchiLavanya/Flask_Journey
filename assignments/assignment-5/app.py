
from flask import Flask, render_template

app = Flask(__name__)

# List of 10 student records
students = [
    {"id": 1, "name": "Ravi", "percentage": 92},
    {"id": 2, "name": "Sita", "percentage": 85},
    {"id": 3, "name": "Lohitha", "percentage": 78},
    {"id": 4, "name": "Arjun", "percentage": 68},
    {"id": 5, "name": "Priya", "percentage": 55},
    {"id": 6, "name": "Kiran", "percentage": 88},
    {"id": 7, "name": "Anu", "percentage": 73},
    {"id": 8, "name": "Rahul", "percentage": 45},
    {"id": 9, "name": "Divya", "percentage": 81},
    {"id": 10, "name": "Manoj", "percentage": 35}
]


# Function to calculate grade
def calculate_grade(percentage):
    if percentage > 80:
        return "A"
    elif percentage > 70:
        return "B"
    elif percentage > 60:
        return "C"
    elif percentage > 50:
        return "D"
    else:
        return "F"


# Display all student records
@app.route("/")
def home():
    for student in students:
        student["grade"] = calculate_grade(student["percentage"])

    return render_template("students.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)