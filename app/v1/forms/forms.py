from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    """registration form
    """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')

    # def validate_username(form, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username is already in use. Please choose a different one.')

    # def validate_email(form, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email is already in use. Please choose a different one.')

    class LoginForm(FlaskForm):
        """login form"""
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')