from flask import Flask
app = Flask(__name__)
#Multiple Routes to one view functions
@app.route('/')
@app.route('/home')
def home():
    return f'Welcome to Day-3 Learning about Static vs Dynamic Routing'
@app.route('/lavanya')
def details():
    return f'HI This is lavanya'
#static routing -->/name/lavanya
#dynamic routing -->/name/<name>
@app.route('/name/lavanya')   #static route
def data():
    return f'welcome Lavanya'

@app.route('/name/<name>')
def student_name(name):
    return f'Hello {name}'
#now we want to create related to course names
@app.route('/courses/<course_name>')
def courses(course_name):
    return f'<b>This Course is:{course_name}</b>'

#Converters -->int,str,float,path,uuid
#Integer converters
@app.route('/student/<int:student_id>')
def studentid(student_id):
    return f'the ID of Student is {student_id}'

#Float Convertor
@app.route('/percentage/<float:percentage>')
def studpercentages(percentage):
    return f'The Percentage of Student is {percentage}'

#path Converters
@app.route('/path/<path:file_name>')
def filepath(file_name):
    return f'The path is {file_name}'

#uuid converters -->Universal Unique Identifier
@app.route('/student_id/<uuid:stu_id>')
def student_id(stu_id):
    return f'The Search for Student is {stu_id}'

if __name__=="__main__":
    #host=0.0.0.0 (because it is address of IPV4)
    #port=5000
    app.run(host='0.0.0.0',
           port=5001,debug=True )