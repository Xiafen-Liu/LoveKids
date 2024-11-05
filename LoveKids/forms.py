from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, TextAreaField
from wtforms.validators import InputRequired, email


class GuestCheckoutForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), email()])
    phone = StringField("Mobile Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    submit = SubmitField("Confirm Order")

class UserInquiryForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), email()])
    phone = StringField("Mobile Number", validators=[InputRequired()])
    message = TextAreaField("Message", validators=[InputRequired()])
    submit = SubmitField("Submit your inquiry")

class LoginForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    submit = SubmitField("Log In")

class SignupForm(FlaskForm):
    username = StringField("User Name", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    firstname = StringField("First Name", validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired(), email()])
    phone = StringField("Mobile Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    submit = SubmitField("Sign Up")