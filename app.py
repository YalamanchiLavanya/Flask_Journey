from config import Config,emailTemplates
import mysql.connector as sql
import random
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, session, redirect
import bcrypt

app = Flask(__name__)
app.secret_key = "lavanya@123"

DBconfig = Config()
from_email = DBconfig.from_email
email_app_password = DBconfig.email_app_password


# 1. Generate Password Hash
def generateHash(text):
    btext = text.encode('utf-8')
    cipher_text = bcrypt.hashpw(btext, bcrypt.gensalt(12))
    return cipher_text.decode('utf-8')


# 2. Database Connection
def getConnectionWithDB():
    try:
        connection = sql.connect(
            host=DBconfig.db_host,
            port=DBconfig.db_port,
            user=DBconfig.db_user,
            password=DBconfig.db_password,
            database=DBconfig.db_name
        )
        return connection

    except sql.Error as e:
        print("Database Connection Error:", e)
        return None


# 3. Insert User Record
def insertUserRecord(user_data):
    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        INSERT INTO users(name, email, password_hash)
        VALUES(%s, %s, %s)
        """

        values = (
            user_data['name'],
            user_data['email'],
            user_data['password_hash']
        )

        cursor.execute(query, values)
        connection.commit()

        return True

    except sql.Error as e:
        print("Insert Error:", e)
        connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 4. Read All User Records
def readUserRecords():
    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")

        data = cursor.fetchall()
        records = []

        for record in data:
            temp = {
                'ID': record[0],
                'name': record[1],
                'email': record[2],
                'PASSWORD_HASH': record[3],
                'IS_VERIFIED': record[4],
                'CREATED_AT': record[5]
            }

            records.append(temp)

        return records

    except sql.Error as e:
        print("Read Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 5. Read User Record By Email
def readUserRecordbyEmail(user_data):
    email = user_data['email']

    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
        SELECT id, name, email, password_hash
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))
        data = cursor.fetchone()

        if data is None:
            return "No Record"

        record = {
            'id': data[0],
            'name': data[1],
            'email': data[2],
            'password_hash': data[3]
        }

        return record

    except sql.Error as e:
        print("Read Email Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 6. Read User Record By ID
def readUserRecordbyId(user_data1):
    user_id = user_data1['id']

    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        data = cursor.fetchone()

        if data is None:
            return "No Record"

        record = {
            'id': data[0],
            'name': data[1],
            'email': data[2],
            'password_hash': data[3]
        }

        return record

    except sql.Error as e:
        print("Read ID Error:", e)
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 7. Update Name By ID Or Email
def updateNamebyIDorEmail(user_data):
    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        new_name = user_data['new_name']

        if 'id' in user_data:
            query = "UPDATE users SET name = %s WHERE id = %s"
            values = (new_name, user_data['id'])
        else:
            query = "UPDATE users SET name = %s WHERE email = %s"
            values = (new_name, user_data['email'])

        cursor.execute(query, values)
        connection.commit()

        return cursor.rowcount > 0

    except sql.Error as e:
        print("Update Name Error:", e)
        connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 8. Update Password By ID Or Email
def updatepasswordByIdorEmail(user_data):
    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        new_password = generateHash(user_data['new_password'])

        if 'id' in user_data:
            query = """
            UPDATE users SET password_hash = %s WHERE id = %s
            """
            values = (new_password, user_data['id'])
        else:
            query = """
            UPDATE users SET password_hash = %s WHERE email = %s
            """
            values = (new_password, user_data['email'])

        cursor.execute(query, values)
        connection.commit()

        return cursor.rowcount > 0

    except sql.Error as e:
        print("Update Password Error:", e)
        connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 9. Update Verified Status
def updateVerifiedByIdorEmail(user_data):
    connection = getConnectionWithDB()

    if connection is None:
        return False

    cursor = None

    try:
        cursor = connection.cursor()

        new_status = user_data['new_IS_VERIFIED']

        if 'id' in user_data:
            query = """
            UPDATE users SET IS_VERIFIED = %s WHERE id = %s
            """
            values = (new_status, user_data['id'])
        else:
            query = """
            UPDATE users SET IS_VERIFIED = %s WHERE email = %s
            """
            values = (new_status, user_data['email'])

        cursor.execute(query, values)
        connection.commit()

        return cursor.rowcount > 0

    except sql.Error as e:
        print("Update Verification Error:", e)
        connection.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        connection.close()


# 10. Generate OTP
def generateOTP():
    otp = random.randint(1000, 9999)
    return otp


# 11. Send OTP Through Email
def sendOTPviaemail(to_email, otp):
    try:
        message = EmailMessage()

        message['Subject'] = "OTP Notification"
        message['From'] = from_email
        message['To'] = to_email

        message.set_content(f"Your OTP is {otp}")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, email_app_password)
            server.send_message(message)

        return True

    except Exception as e:
        print("Email Error:", e)
        return False


def sendEmail(subject:str,to_email:str,body:str):
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = from_email
    message['To'] = to_email
    message.set_content(body)
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login(from_email,email_app_password)
        server.send_message(message)
    return True    



# 12. Validate User Data
def validateData(user_data):
    errors = []

    name = user_data['name']
    email = user_data['email']
    password = user_data['password']
    confirm_password = user_data['confirm_password']

    if len(name) < 2:
        errors.append("Invalid Name")

    if len(email) < 5 or '@' not in email:
        errors.append("Invalid Email")

    if len(password) < 6:
        errors.append("Password must contain at least 6 characters")

    if password != confirm_password:
        errors.append("Password Mismatch")

    return errors


# 13. Verify Duplicate Email
def verifyDuplicateEmail(user_data):

    record = readUserRecordbyEmail(user_data)

    if record == "No Record":
        return False

    elif record is False:
        return None

    else:
        return True


# ROUTES

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    global OTP
    if(request.method=="GET"):
        return render_template('register.html')
    elif(request.method=="POST"):
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        confirm_password=request.form['confirm_password']
        user_data={
            'name':name,
            'email':email,
            'password':password,
            'confirm_password':confirm_password
        }
        errors = validateData(user_data)
        if len(errors)>0:
            return render_template('register.html',errors=errors)
        else:
            is_duplicate = verifyDuplicateEmail(user_data)
            if is_duplicate == False:
                #if there is no account
                #convert password to hash value
                session['otp'] = generateOTP()
                #OTP = generateOTP()
                password_hash = generateHash(user_data['password'])
                name = user_data['name']
                email = user_data['email']
                status = insertUserRecord({
                   'name':name,
                   'email':email,
                   'password_hash':password_hash
                })
                #status of insertion
                if status == True:
                   session['username'] = email
                   # Generate OTP
                   otp = random.randint(100000, 999999)

                  # Store OTP in session
                   session['otp'] = otp
                   #sendOTPviaemail(email,otp)
                   sendEmail(subject="Verify Your Registration - Notes Management",to_email=email,
                             body=emailTemplates.send_otp_template(username=name,otp=otp))
                   return redirect('/verify')
                #    return render_template('register.html',
                #                           res="Registration Succesfully Completed")
                else:
                   return render_template('register.html',
                                          err="Registration Failed")
                              
            else:
                return render_template('register.html',
                                       err="Account already existed")



@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/verify',methods = ['GET','POST'])
def verify():
   if request.method == "GET":
      return render_template('verify.html')
   elif request.method == "POST":
      try:
          otp = int(request.form['otp'])
      except (KeyError, ValueError):
          return render_template('verify.html', err="Invalid OTP")

      if otp == session.get('otp'):
          is_verify = True
          email = session.get('username')
          updateVerifiedByIdorEmail({'email': email, 'new_IS_VERIFIED': is_verify})
          return redirect('/login')
      else:
          return render_template('verify.html',err="Invalid OTP")

if __name__=="__main__":
    app.run(host='0.0.0.0', 
            port = 5000,
            debug=True)

#Registration Flow:

#User-->register.html-->Registration form-->Post-->Python-->collecting Data-->Validating-->Verifying-->Password to password hash-->MySQL Table

#HTML <-> Python <-> MySQL

#Registration Flow
#User has to click on get Started
#Register page
#Name,email,password,confrim password and submit
#verifyDuplicateEmail() --> if account not exits
#generate OTP
#send email with otp
#redirect to verify.html
#enter the otp received on email
#if the otp matches with the session otp
#it will redirect to login
#if they are not matching,it redirects with a message
#



# @app.route('/register',methods = ['GET','POST'])
# def register():
#    if request.method == "GET":
#       renderHTMLPage()
#     elif request.method == "POST":
#       collectUserData()
#       validateUserData()
#       displayErrors()
#       status = verifyAccountExist()
#       if status:
#          insertRecord()
#       else:
#          displayErrorMessage()
