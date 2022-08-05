from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


# Form Classes
class RegisterForm(Form):
    username = StringField(
        'Username', validators=[DataRequired(), Length(min=6, max=64)]
    )
    first_name = StringField(
        'First Name', validators=[DataRequired(), Length(min=1, max=64)]
    )
    last_name = StringField(
        'Last Name', validators=[DataRequired(), Length(min=1, max=64)]
    )
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=64)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=20)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = StringField(
        'Email', validators=[DataRequired(), Length(min=6, max=64)]
    )
