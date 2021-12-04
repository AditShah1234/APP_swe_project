from flask import Flask, render_template, redirect, url_for,request, send_file, session
from flask.sessions import NullSession
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, RadioField, TextAreaField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets.core import PasswordInput
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from wtforms.fields import StringField
from wtforms.widgets import TextArea

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'ghghchgcghchhddgdgf'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
Bootstrap(app)

class member:
  def __init__(self, mobileno, email,username, password):
    self.mobileno = mobileno
    self.email = email
    self.username =username
    self.password = password


persons = []


import sqlite3
    
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    password_confirm = PasswordField('password_confirm', validators=[InputRequired(), Length(min=4, max=15)])
    mobile_number = StringField('mobile_number', validators=[InputRequired(), Length(10)])
    gender = RadioField('gender', choices=[('Male','Male'),('Female','Female')])

class ForgotPassForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=80)])
    password_confirm = PasswordField('password_confirm', validators=[InputRequired(), Length(min=4, max=15)])
    
class Personal_info(FlaskForm):
    height = StringField('height', validators=[InputRequired(), Length(min=1, max=2)])
    weight = StringField('weight', validators=[InputRequired(), Length(min=1, max=3)])
    age = StringField('age', validators=[InputRequired(), Length(min=1, max=3)])
    remark =TextAreaField('Special Remark', render_kw={"rows": 70, "cols": 11})

class Mental_info(FlaskForm):
    q1 = RadioField('q1', choices=[('Yes','Yes'),('No','No')])
    q2 = RadioField('q2', choices=[('Yes','Yes'),('No','No')])
    q3 = RadioField('q3', choices=[('Yes','Yes'),('No','No')])
    q4 = RadioField('q4', choices=[('Yes','Yes'),('No','No')])
    q5 = RadioField('q5', choices=[('Yes','Yes'),('No','No')])
    q6 = RadioField('q6', choices=[('Yes','Yes'),('No','No')])
    q7 = RadioField('q7', choices=[('Yes','Yes'),('No','No')])
    q8 = RadioField('q8', choices=[('Yes','Yes'),('No','No')])
    q9 = RadioField('q9', choices=[('Yes','Yes'),('No','No')])



    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        print(username, password)
        # if username == "admin" and password == "admin":
        if username == "admin":
           
            return redirect(url_for('admin'))

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        check = c.execute("SELECT * FROM member WHERE username=?",(username,))
        check = c.fetchall()
        print(check)
        if len(check) ==0:
            return render_template("signup.html", form=form, message = "Please sign up")
        
        actual_pass = check[0][2]
        print(actual_pass)
        if actual_pass != password:
            return render_template('login.html', form=form, message = "Password is wrong")
        else:
            
            session["username"] = username
            if check[0][6] == "null" or check[0][6] == None:

                return redirect(url_for('personal_info'))
            else:
                return redirect(url_for('page1'))
     

        
    elif request.method == 'GET':

        return render_template('login.html', form=form)






@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        username = form.username.data
        emailid = form.email.data
        password2 = form.password_confirm.data
        password = form.password.data
        mobileno = form.mobile_number.data
        gender = form.gender.data
     
        p  =  member(mobileno, emailid,username, password)
        persons.append(p)
        print(username,emailid, password,mobileno,gender, password2)
      
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        check = c.execute("SELECT * FROM member WHERE username=?",(p.username,))
        check = c.fetchall()
        print(check)
        if len(check) !=0:
            return render_template("signup.html", form=form, message = "The user name exist select other username")


        c.execute("INSERT INTO member VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ", (p.username, p.email, p.password,gender,mobileno,None,None,None,None,None,None, None))
        conn.commit()
        # c.execute("select * from member")
        # print(c.fetchall())
        conn.close()
        return redirect(url_for('index'))
     
    elif request.method == 'GET':
        return render_template("signup.html", form=form)






    
@app.route('/personal_info',  methods=['GET', 'POST'])
def personal_info():
    form = Personal_info()
    print(session["username"])
    if request.method == 'POST':
        height = str(form.height.data)
        weight = str(form.weight.data)
        age = str(form.age.data)
        remark = form.remark.data
        print(height,remark, weight, age)
        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            print(str(session["username"]))
         
            username = str(session["username"])
          
            
            query = "Update member set Age = ? where username = ?"
           
            c.execute(query, (age,username , ))
            conn.commit()
            query = "Update member set Weight = ? where username = ?"
            c.execute(query, (weight,username , ))
            conn.commit()


            query = "Update member set height = ? where username = ?"
            c.execute(query, (height,username , ))

            conn.commit()

            if remark!="":
                
                c.execute('''UPDATE member SET Remark_member = ? WHERE username = ?''', (str(remark), str(session["username"]), ))
                conn.commit()

            # c.execute('''UPDATE member SET age = ? WHERE username = ?''', (str(age), str(session["info"]), ))
            c.execute("select * from member")
            print(c.fetchall())
            
            conn.close()
        except Exception as e:
            print("not ",e)
        return redirect(url_for('page1'))
    elif request.method == 'GET':
        return render_template("personal_info.html", form=form)

@app.route('/page1',  methods=['GET', 'POST'])
def page1():
    return render_template("page1.html")









@app.route('/forgot_password',  methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPassForm()
    if request.method == 'POST':
       
        username = form.username.data
        emailid = form.email.data
        password2 = form.password_confirm.data
        password = form.password.data
        
        print(username,emailid)
        conn = sqlite3.connect('database.db')
        

        c = conn.cursor()
        
        check = c.execute("SELECT * FROM member WHERE username=?",(username,))
        check = c.fetchall()
      
        if check[0][1] == emailid:
            if password ==password2:
                c.execute('''UPDATE member SET password = ? WHERE username = ?''', (str(password), username,))
                conn.commit()
               
                conn.close()

                return redirect(url_for('index'))
            else:
                return render_template("forgot_pass.html",form=form, message="Check pasword")
        else:
            return render_template("forgot_pass.html",form=form, message="check your emailid and username")
        
       
     
        # print(c.fetchall())
     
        
    elif request.method == 'GET':
        return render_template("forgot_pass.html",form=form)

@app.route('/coo', methods=['GET', 'POST'])
def coo():
    return redirect(url_for('forgot_password'))








@app.route('/physical',  methods=['GET', 'POST'])
def physical():
    if request.method == 'GET':
        return render_template("physical.html")

@app.route('/thin')
def thin():
    return send_file('assets/sample.pdf', as_attachment=True)

@app.route('/lean')
def lean():
    return send_file('assets/sample.pdf', as_attachment=True)

@app.route('/fit')
def fit():
    return send_file('assets/sample.pdf', as_attachment=True)
    




@app.route('/mental',  methods=['GET', 'POST'])
def mental():
    form = Mental_info()
    if request.method == 'POST':
        q1 = form.q1.data
        q2 = form.q2.data
        q3 = form.q3.data
        q4 = form.q4.data
        q5 = form.q5.data
        q6 = form.q6.data
        q7 = form.q7.data
        q8 = form.q8.data
        q9 = form.q9.data
        q = (q1,q2,q3,q4,q5,q6,q7,q8,q9)
        conn = sqlite3.connect('database.db')
        

        c = conn.cursor()
        c.execute('''UPDATE member SET Answer = ? WHERE username = ?''', (str(q), session["username"],))
        conn.commit()
        
        conn.close()
        
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("mental.html",form=form)




@app.route('/admin',  methods=['GET', 'POST'])
def admin():
    
    if request.method == 'GET':

        conn = sqlite3.connect('database.db')
        

        c = conn.cursor()


        c.execute("select * from member")
        rows = (c.fetchall())
        heading = ["username", "email" , "password" ,"Gender" ,"Mobile No" , 	"Age" , "height" ,	"Weight" , "Remark_member" , "Answer" , "Doctor" ,"remark_doctor" ]
    
        conn.close()

        return render_template("admin.html", rows =rows, heading = heading)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    
    # conn = sqlite3.connect('database.db')
    # print ("Opened database successfully")
    # c = conn.cursor()
    # c.execute("""CREATE TABLE member (username TEXT, email TEXT, password TEXT,Gender TEXT,Mobile No TEXT, 	Age TEXT, height TEXT,	Weight TEXT, Remark_member TEXT, Answer TEXT, Doctor TEXT,remark_doctor TEXT)""")
    # conn.commit
    # conn.close()
    


    app.run(debug=True, port=3000)
 
