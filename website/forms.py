from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms import validators as valid

class LoginForm(Form):
    username = StringField('User Id', [valid.Required('Please enter your user id')])
    password = PasswordField('Password', [valid.Required('Please enter your password')])
