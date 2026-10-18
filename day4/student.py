from flask import Flask
import uuid
app=Flask(__name__)
#we will generate UUID using pyhon module
# Student default page
@app.route('/')
def home():
    return "Student Routing Application"

# #student id
@app.route('/studentid/<int:student_id>')
def studentid(student_id):
    return f'the ID of Student is {student_id}'

#student attendence
@app.route('/attendence/<float:percentage>')
def studpercentages(percentage):
    return f'The  attendence Percentage of Student is {percentage}'

#Student Skills
@app.route('/skills/<s1>/<s2>')
def skills(s1,s2):
    return f'Student has {s1} and {s2} Skills'

# file path
@app.route('/path/<path:file_name>')
def filepath(file_name):
    return f'The path is {file_name}'

# #student UUID    
@app.route('/stu_id')
def generate():
    id=uuid.uuid4().hex
    print(id)
    return f'The student UUID is : {id}'


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