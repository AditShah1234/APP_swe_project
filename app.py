from flask import Flask, render_template, redirect, url_for,request, send_file
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
Bootstrap(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email
    

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    password_confirm = PasswordField('password_confirm', validators=[InputRequired(), Length(min=4, max=15)])
    mobile_number = StringField('mobile_number', validators=[InputRequired(), Length(10)])
    gender = RadioField('gender', choices=[('Male','Male'),('Female','Female')])

class ForgotPassForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])

class Personal_info(FlaskForm):
    height = StringField('height', validators=[InputRequired(), Length(min=1, max=2)])
    weight = StringField('weight', validators=[InputRequired(), Length(min=1, max=3)])
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
        
        if username == "adit" or password:
                
            return redirect(url_for('personal_info'))

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

        
        new_user = User(email=form.email.data)
        db.session.add(new_user)
        db.session.commit()
        print(username,emailid, password,mobileno,gender, password2)
        t = User.query.order_by(User.id)
        
        return redirect(url_for('index'))
     
    elif request.method == 'GET':
        return render_template("signup.html", form=form)






    
@app.route('/personal_info',  methods=['GET', 'POST'])
def personal_info():
    form = Personal_info()
    if request.method == 'POST':
        height = form.height.data
        weight = form.weight.data
        remark = form.remark.data
        print(height,remark, weight)
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
        
        print(username,emailid)
        return render_template("signup.html")
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
       
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template("mental.html",form=form)






@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)