from flask import Flask, render_template
import datetime as dt
import requests

response = requests.get(url='https://api.npoint.io/674f5423f73deab1e9a7')
response.raise_for_status()
all_posts = response.json()

time_now = dt.datetime.now()
year = time_now.year

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", current_year=year, posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/post/<id>')
def get_post(id):
    return render_template("post.html", post_id=int(id), posts=all_posts)


# Add the following code to run this script directly
if __name__ == "__main__":
    # Set debug to True to enable hot reloading
    app.run(debug=True)
