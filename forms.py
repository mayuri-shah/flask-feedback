from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class Register(FlaskForm):
    username = StringField("User Name : ",validators=[InputRequired()])
    password = PasswordField("Password : ",validators=[InputRequired()])
    email = StringField("Email : ")
    firstname = StringField("First Name : ")
    lastname = StringField("Last Name : ")

class Login(FlaskForm):
    username = StringField("User Name : ",validators=[InputRequired()])
    password = PasswordField("Password : ",validators=[InputRequired()])

class Feedback_Form(FlaskForm):
    title = StringField("Title : ",validators=[InputRequired()])
    content = StringField("Content : ",validators=[InputRequired()])