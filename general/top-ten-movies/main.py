from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_api_key'
Bootstrap5(app)


class RateMovieForm(FlaskForm):
    updated_rating = StringField(label='Your Rating Out of 10 (e.g. 7.5)',
                                 validators=[DataRequired(message="Please enter the rating.")])
    updated_review = StringField(label='Your Review', validators=[DataRequired(message="Please enter the review.")])
    submit = SubmitField('Done')


class AddMovieForm(FlaskForm):
    new_movie_title = StringField(label='Movie Title',
                                  validators=[DataRequired(message="Please enter the movie title.")],
                                  render_kw={"placeholder": "Enter movie title"})
    submit = SubmitField('Add')


# CREATE DB
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top-ten-movies.db'
db.init_app(app)


# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True)
    ranking: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)


# Create the database table
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    # Alternatively, use `all_movies_list = result.scalars().all()`
    # `result.scalars().all()` fetches all the results from the database at once and returns them as a Python list
    all_movies = result.scalars()
    all_movies_list = list(all_movies)
    all_movies_list.reverse()

    # Assign unique rankings using enumerate
    for index, movie in enumerate(all_movies_list):
        movie.ranking = index + 1  # Rankings start at 1

    db.session.commit()

    all_movies_list.reverse()
    return render_template("index.html", all_movies_list=all_movies_list)


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    edit_form = RateMovieForm()
    # Fetch the movie to update， using the id retrieved back
    # Alternatively, use id = request.args.get('id')
    movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    if edit_form.validate_on_submit():
        new_rating = float(edit_form.updated_rating.data)
        new_review = edit_form.updated_review.data
        movie_to_update.rating = new_rating
        movie_to_update.review = new_review
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie=movie_to_update, form=edit_form)


@app.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        title_to_search = add_form.new_movie_title.data
        payload = {
            "query": title_to_search,
            "api_key": os.getenv("API_KEY")
        }
        url = "https://api.themoviedb.org/3/search/movie"
        response = requests.get(url=url, params=payload)
        response.raise_for_status()
        print(response.text)
        all_search_results = response.json()["results"]
        return render_template('select.html', results=all_search_results)
    return render_template('add.html', form=add_form)


@app.route("/select", methods=['GET', 'POST'])
def select():
    movie_id = request.args.get('movie_id')
    payload = {
        "api_key": os.getenv("API_KEY")
    }
    response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=payload)
    response.raise_for_status()
    print(response.text)
    release_date = response.json()["release_date"]
    image_url_suffix = response.json()["poster_path"]

    new_movie = Movie(
        title=response.json()["title"],
        year=int(release_date[:4]),
        description=response.json()["overview"],
        img_url=f"https://media.themoviedb.org/t/p/original{image_url_suffix}",
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=new_movie.id))


@app.route("/delete")
def delete():
    # Fetch the movie to update， using the id retrieved back
    id = request.args.get('id')
    movie_to_delete = db.session.execute(db.select(Movie).where(Movie.id == id)).scalar()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
