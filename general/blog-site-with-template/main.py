from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length


class MyForm(FlaskForm):
    email = StringField(label='Email', validators=[Email(message="Invalid email address", check_deliverability=True)])
    password = PasswordField(label='Password',
                             validators=[Length(min=8, message="Must be as least 8 characters long.")])
    submit = SubmitField(label="Log in")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
bootstrap = Bootstrap4(app)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = MyForm()
    if form.validate_on_submit():  # validate_on_submit checks if it's a POST request and if it's valid.
        if form.email.data == "admin@email.com" and form.password.data == "12345678":
            # Redirect the user to the '/success' route upon successful login.
            return redirect('/success')
            # Alternatively, directly render the "success.html" page without redirecting.
            # This does not change the URL; namely, users are still at the `login` route.
            # return render_template("success.html")
        else:
            # Redirect the user to the '/denied' route for login failure.
            return redirect('/denied')
            # Alternatively, directly render the "denied.html" page without redirecting.
            # This does not change the URL; namely, users are still at the `login` route.
            # return render_template("denied.html")
    return render_template('login.html', form=form)


@app.route("/success", methods=['GET', 'POST'])
def succeed():
    return render_template('success.html')


@app.route("/denied")
def deny():
    return render_template('denied.html')


if __name__ == '__main__':
    app.run(debug=True)
