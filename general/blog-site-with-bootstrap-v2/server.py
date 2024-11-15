from flask import Flask, render_template, request
import datetime as dt
import requests
import smtplib

my_email = "xxxx@gmail.com"
password = "****"

response = requests.get(url='https://api.npoint.io/674f5423f73deab1e9a7')
response.raise_for_status()
all_posts = response.json()

time_now = dt.datetime.now()
year = time_now.year

app = Flask(__name__)

def send_email(name, email, phone, message):
    """
    Function to send the email with input parameters.
    """
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # Make the connection secure
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="xxxxxx@gmail.com",
            msg=email_message
        )


@app.route('/')
def home():
    return render_template("index.html", current_year=year, posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        print(name)
        print(email)
        print(phone)
        print(message)
        send_email(name=name, email=email, phone=phone, message=message)
        return "<h1>Successfully sent your message!</h1>"
    elif request.method == 'GET':
        return render_template("contact.html")


@app.route('/post/<id>')
def get_post(id):
    return render_template("post.html", post_id=int(id), posts=all_posts)


# Add the following code to run this script directly
if __name__ == "__main__":
    # Set debug to True to enable hot reloading
    app.run(debug=True)
