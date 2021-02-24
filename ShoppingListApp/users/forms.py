from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

from ShoppingListApp.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=50)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.find_by_username(username.data)
        if user is not None:
            raise ValidationError(f"User with username '{username.data}' already exists. "
                                  f"Please choose another username.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
