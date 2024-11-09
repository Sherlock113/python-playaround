from flask import Flask, render_template
import requests
import datetime as dt

response = requests.get(url='https://api.npoint.io/080d3cd88bb0c55aa4f6')
response.raise_for_status()
all_posts = response.json()

time_now = dt.datetime.now()
year = time_now.year

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts, current_year=year)


@app.route('/post/<id>')
def get_post(id):
    # Flask converts id to a string
    # Must convert the id back to an integer
    return render_template("post.html", post_id=int(id), posts=all_posts, current_year=year)


# Add the following code to run this script directly
if __name__ == "__main__":
    # Set debug to True to enable hot reloading
    app.run(debug=True)
