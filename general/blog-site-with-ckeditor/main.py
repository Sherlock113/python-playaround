from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from datetime import datetime

# Get the current date
current_date = datetime.now()
formatted_date = current_date.strftime("%B %d, %Y")

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap5(app)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class AddPostForm(FlaskForm):
    title = StringField(label='New Blog Post Title',
                        validators=[DataRequired(message="Please enter the title")])
    subtitle = StringField(label='New Blog Post Subtitle',
                           validators=[DataRequired(message="Please enter the subtitle.")])
    author = StringField(label='New Blog Post Author', validators=[DataRequired(message="Please enter the author.")])
    background_image_url = StringField(label='Background Image URL', validators=[URL(message="Please enter the URL.")])
    body = CKEditorField('Content', validators=[DataRequired(message="Please enter the blog content.")])
    submit = SubmitField('Submit')


# CONFIGURE TABLE
class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost).order_by(BlogPost.id))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # Alternatively, use `requested_post = db.get_or_404(BlogPost, post_id)`
    requested_post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=requested_post)


@app.route('/new_post/', methods=["POST", "GET"])
def add_post():
    new_post_form = AddPostForm()
    if new_post_form.validate_on_submit():
        new_post = BlogPost(
            title=new_post_form.title.data,
            subtitle=new_post_form.subtitle.data,
            author=new_post_form.author.data,
            img_url=new_post_form.background_image_url.data,
            body=new_post_form.body.data,
            date=formatted_date
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('get_all_posts'))
    add_post = True
    return render_template("make-post.html", form=new_post_form, add_post=add_post)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
def edit_post(post_id):
    blog_to_update = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    # Auto-populate the fields in the WTForm with the blog post's data
    edit_form = AddPostForm(
        title=blog_to_update.title,
        subtitle=blog_to_update.subtitle,
        background_image_url=blog_to_update.img_url,
        author=blog_to_update.author,
        body=blog_to_update.body
    )
    if edit_form.validate_on_submit():
        blog_to_update.title = request.form.get('title')
        blog_to_update.subtitle = request.form.get('subtitle')
        blog_to_update.author = request.form.get('author')
        blog_to_update.body = request.form.get('body')
        blog_to_update.img_url = request.form.get('background_image_url')
        db.session.commit()
        return redirect(url_for('show_post', post_id=blog_to_update.id))
    return render_template("make-post.html", form=edit_form)


@app.route("/delete")
def delete():
    id = request.args.get('id')
    blog_to_delete = db.session.execute(db.select(BlogPost).where(BlogPost.id == id)).scalar()
    db.session.delete(blog_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


# Below is the code from previous lessons. No changes needed.
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5003)
