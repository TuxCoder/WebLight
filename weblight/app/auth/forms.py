from flask.ext.wtf import Form
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length


class LoginForm(Form):
    login_name = StringField(
        "Login name",
        validators=[DataRequired()])
    password = PasswordField(
        "Password",
        validators=[DataRequired()])
    remember_me = BooleanField(
        "Keep me logged in")


class ChangePasswordForm(Form):
    current_password = PasswordField(
        "Current password",
        validators=[
            DataRequired()])
    new_password = PasswordField(
        "New password",
        validators=[
            DataRequired(),
            Length(6, 30),
            EqualTo("new_password_confirm")])
    new_password_confirm = PasswordField(
        "Confirm new password",
        validators=[DataRequired()])
