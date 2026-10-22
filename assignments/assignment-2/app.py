
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return '<h1>About Page</h1><a href="/">Go to Home</a>'

# GET request
@app.route('/getdata', methods=['GET'])
def getdata():
    name = request.args.get('name')
    batchno = request.args.get('batchno')
    return {
        'name': name,
        'batchno': batchno
    }

# POST request
@app.route('/postdata', methods=['POST'])
def postdata():
    data = request.get_json()
    name = data.get('name')
    skills = data.get('skills')
    return {
        'name': name,
        'skills': skills
    }

if __name__ == '__main__':
    app.run(debug=True)