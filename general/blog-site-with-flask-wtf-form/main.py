from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe Name', validators=[DataRequired(message="Enter the name of the Cafe.")])
    location = StringField(label='Cafe Location (URL on Google Maps)',
                           validators=[URL(message="Enter the URL of the Cafe location on Google Maps.")])
    opening_time = StringField(label='Opening Time (For example, 8AM)',
                               validators=[DataRequired(message="Enter the time the Cafe opens.")])
    closing_time = StringField(label='Closing Time (For example, 5:30PM)',
                               validators=[DataRequired(message="Enter the time the Cafe closes.")])
    cafe_rating = SelectField(label='Cafe Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'])
    wifi_rating = SelectField(label='Wifi Strength', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'])
    power_rating = SelectField(label='Power Socket Availability', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_cafe_list = [form.cafe.data, form.location.data, form.opening_time.data, form.closing_time.data,
                         form.cafe_rating.data, form.wifi_rating.data, form.power_rating.data]
        # Add a new line in the cafe database
        with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_cafe_list)

        return redirect('/cafes')
    return render_template('add.html', form=form)


@app.route('/cafes')
def get_cafes_info():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
