
from flask import Flask, render_template, request, jsonify, url_for

app = Flask(__name__)


# Task 1: Navigate from Home to About using url_for
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


# Task 2: GET request to get name and batchno
@app.route("/getdata", methods=["GET"])
def get_data():
    name = request.args.get("name")
    batchno = request.args.get("batchno")

    return jsonify({
        "name": name,
        "batchno": batchno
    })


# Task 3: POST request to fetch name and skills using JSON
@app.route("/postdata", methods=["POST"])
def post_data():
    data = request.get_json()

    name = data.get("name")
    skills = data.get("skills")

    return jsonify({
        "name": name,
        "skills": skills
    })


if __name__ == "__main__":
    app.run(debug=True)