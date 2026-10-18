from flask import Flask,redirect,render_template,url_for,request
#create a flask application instance
app=Flask(__name__)
@app.route('/')
def home():
    #return f'Flask Server is Running'
    return render_template('index.html')

#GET-->Fetching the data form db
#POST --> store the data in db,forms
#PUT -->update the data (entire row)
#DELETE -->delete the data (entire row)
#PATCH --> update a specific column in a row

#name=Lavanya,email=lavanya@codegna.com
@app.route('/getdata',methods=['GET'])
def getdata():
    name = request.args.get('name')
    email = request.args.get('email')
    return f'the name is {name} and email is {email}'

#POST
@app.route('/getdatafromPost',methods=['POST'])
def getDatafromPOST():
    data=request.get_json()
    name = data['name']
    email=data['email']
    return f'The name is {name},email is {email}'

@app.route('/postData',methods=['POST'])
def postData():
    name=request.form['name']
    email=request.form['email']
    password=request.form['password']

    if name is None or len(name)<5:
        return render_template('index.html',
                               err="Invalid Name")

    if email is None:
        return render_template('index.html',
                               err="Invalid Email")

    if password is None or len(password)<4:
        return render_template('index.html',
                               err="Invalid Password")

    return render_template('index.html',
                           msg="Successful")

#PUT
@app.route('/updateData/<email>',methods=['PUT'])
def updateData(email):
    data = request.get_json()
    email1 = data['email']
    print(email1)
    #DATABASE LOGIC for PUT
    return f"Data is updated Successfully for  {email}"

#DELETE
@app.route('/deleteData/<email>',methods=['DELETE'])
def deleteData(email):
     #DATABASE LOGIC for DELETE
     return f'Data is deleted successfull from {email}' 

@app.route('/register',methods=['GET','POST'])
def register():
    #here we will mention our condition it can be 
    #either GET or POSt
    if request.method == "GET":
        name = request.args.get('name')
    if  request.method == "POST":
        data = request.get_json()
        #in POST method we will store the data in JSON
        name = data['name']
    return f'The name is {name}'        

if __name__=="__main__":
    app.run(host='0.0.0.0',
            port=5001,debug=True)
