from flask import Flask,render_template,url_for,request,redirect
import uuid
app=Flask(__name__)
#we will generate UUID using pyhon module
# Student default page
@app.route('/')
def home():
    return redirect(url_for('indexpage'))
    #return "Welcome to Day-4 of Learning Flask"
   
@app.route('/generate')
def generate():
    id=uuid.uuid4().hex
    print(id)
    return f'The generate id  is : {id}'

@app.route('/index')
def indexpage():
    return render_template('index.html')

@app.route('/about')
def aboutpage():
    return render_template('about.html')

if __name__=="__main__":
    app.run(host='0.0.0.0',
            port=5002,debug=True)

#Build a student routing app
# Student default page
# #student id
# #student attendence
# file path
# student UUID  
#  courses --> 