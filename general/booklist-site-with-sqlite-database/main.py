from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'
db.init_app(app)


# Define a model
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


# Create the database table
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(Book).order_by(Book.id))
    all_books = result.scalars()
    all_books_list = list(all_books)
    return render_template("index.html", all_books_list=all_books_list)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Add a new book
        new_book = Book(title=request.form.get('title'), author=request.form.get('author'),
                        rating=float(request.form.get('rating')))
        db.session.add(new_book)
        db.session.commit()
        print(f"Added book: {new_book}")
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    # Fetch the book to update， using the id retrieved back
    # Alternatively, use id = request.args.get('id')
    book_to_update = db.session.execute(db.select(Book).where(Book.id == id)).scalar()

    if request.method == 'POST':
        new_rating = float(request.form.get('new_rating'))
        book_to_update.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', book=book_to_update)


@app.route("/delete/<int:id>")
def delete(id):
    # Fetch the book to update， using the id retrieved back
    # Alternatively, use id = request.args.get('id')
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)