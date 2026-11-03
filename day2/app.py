from flask import Flask
#Create a Flask application instance
app = Flask(__name__)
#__name__ is saying its a flask object
#now we will start defining the routes
@app.route('/')
def home():
    """Default home page"""
    return "Hello PFS-VSP-004 guys keep going"
@app.route('/lavanya')
def details():
    """Details about Lavanya"""
    return "Lavanya is Python Full Stack Traniee at Codegnan"
@app.route('/profile')
def profile():
    """Profile of Lavanya"""
    return "Lavanya is a recent graduate in BTECH"
@app.route('/students')
def data():
    """Students info"""
    return "Studnets are from Codegnan"
if __name__=="__main__":
    #if port is already in use change the port number
    app.run(host="0.0.0.0",
            port=5000,debug=True)

