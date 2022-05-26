from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from email_validator import validate_email, EmailNotValidError
from flask_bootstrap import Bootstrap

EMAIL = 'admin@email.com'
PASSWORD = '12345678'


class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired(), Email()])
    password = PasswordField(label='password', validators=[DataRequired(), Length(max=8)])
    submit = SubmitField(label='LogIn')


app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'hsubebaejijkeb3brrbe'


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        if login_form.email.data == EMAIL and login_form.password.data == PASSWORD:
            print(login_form.email.data)
            return render_template('success.html')
        else:
            return render_template('denied.html')
    else:
        return render_template('login.html', form=login_form)


if __name__ == '__main__':
    app.run(debug=True)
