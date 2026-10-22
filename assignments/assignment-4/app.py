
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def signup():
    return render_template("signup.html")


@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    email = request.form.get("email")
    address = request.form.get("address")
    password = request.form.get("password")

    return f"""
    <h1>Signup Successful!</h1>
    <p>Username: {username}</p>
    <p>Email: {email}</p>
    <p>Address: {address}</p>
    <p>Password received successfully.</p>
    """


if __name__ == "__main__":
    app.run(debug=True)