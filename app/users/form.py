from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, PasswordField,
                     SubmitField, BooleanField, TextAreaField)
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    user_name = StringField('Usernames: ', 
                           validators=[DataRequired(), Length(min=2, max=69)])
    email = EmailField('Email: ', validators=[DataRequired()])
    paswd = PasswordField("Password: ", validators=[DataRequired()])
    confirm = PasswordField ("Confirm password: ", 
                             validators=[DataRequired(), EqualTo('paswd')])
    submit = SubmitField("Submit Now!")
    
    def validate_user_name(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError("UserName already defined!")
    
    def validate_email(self, mail):
        em=User.query.filter_by(email=mail.data).first()
        if em:
            raise ValidationError("Email already defined!")
    
class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    paswd  = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField('Log In') 
    remember = BooleanField('Keep Logged in')
    
class EditUser(FlaskForm):
    user_name = StringField('Usernames: ', 
                           validators=[DataRequired(), Length(min=2, max=69)])
    email = EmailField('Email: ', validators=[DataRequired()])
    
    submit = SubmitField("Update Now!")
    
    profile_img = FileField("New Profile Picture",
                           validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    def validate_user_name(self, username):
        if self.user_name.data == current_user.user_name:
            user = User.query.filter_by(user_name=username.data).first()
            if user:
                raise ValidationError("UserName already defined!")
    
    def validate_email(self, mail):
        if self.email.data != current_user.email:
            em=User.query.filter_by(email=mail.data).first()
            if em:
                raise ValidationError("Email already defined!")
            

class RequestResetForm(FlaskForm):
    email=EmailField("Email: ", validators=[DataRequired()])
    submit=SubmitField("Request Password Reset")
    
    def validate_email(self, mail):
        user=User.query.filter_by(email=mail.data).first()
        if not user:
            raise ValidationError("There is no account with this email Register")
        
class ResetPassword(FlaskForm):
    paswd = PasswordField("Password: ", validators=[DataRequired()])
    confirm = PasswordField ("Confirm password: ", 
                             validators=[DataRequired(), EqualTo('paswd')])
    submit = SubmitField("Reset Password")
