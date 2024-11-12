from flask import Flask, render_template
import datetime as dt

time_now = dt.datetime.now()
year = time_now.year

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", current_year=year)


# Add the following code to run this script directly
if __name__ == "__main__":
    # Set debug to True to enable hot reloading
    app.run(debug=True)