#Create a resume html page to be rendered in default root
#Create a dynamic route for reading subject and subject marks (float) 
#Create a dynamic route for generating a uuid for a subject 
#Create a static route for '/' and '/home' to render resume.html
#Create a navigation to navigate from home to about page using url_for



from flask import Flask, render_template
import uuid

app = Flask(__name__)

# Static route
@app.route("/")
def index():
    return render_template("index.html")

# Static route
@app.route("/home")
def home():
    return render_template("index.html")

# Dynamic route read subject and float marks
@app.route("/subject/<subject>/<float:marks>")
def subject_marks(subject, marks):
    return f"Subject: {subject} and Marks: {marks:.2f}"

# Dynamic route generate UUID for a subject
@app.route("/uuid/<subject>")
def subject_uuid(subject):
    unique_id = uuid.uuid4()
    return f"Subject: {subject} and UUID: {unique_id}"

# Static route: about page
@app.route("/about")
def about():
    return "<h1>About Page</h1><p>Welcome to my Flask application!</p>Back to Home</a>"

if __name__ == "__main__":
    app.run(debug=True)