from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from tmdbv3api import TMDb
from tmdbv3api import Movie

tmdb = TMDb()
tmdb.api_key = 'API KEY'
tmdb.language = 'en'
tmdb.debug = True
movie = Movie()

Movie_IMG = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ANY SECRETE KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Movie_Form(FlaskForm):
    movie_title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(80), nullable=True)
    img_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f"<Movie {self.title}>"


db.drop_all()
db.create_all()

ALL_MOVIES = db.session.query(Movies).all()


@app.route("/")
def home():
    ALL_MOVIES = Movies.query.order_by(Movies.rating).all()
    for i in range(len(ALL_MOVIES)):
        ALL_MOVIES[i].ranking = len(ALL_MOVIES) - i
    db.session.commit()
    return render_template("index.html", movies=ALL_MOVIES)


@app.route("/delete/<int:id>")
def delete(id):
    movie_id = id
    movie_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = Movie_Form()
    if request.method == "POST" and form.validate_on_submit():
        m_title = request.form['movie_title']
        search = movie.search(m_title)
        return render_template('select.html', movies=search)
    return render_template('add.html', form=form)


@app.route("/select")
def select_movie():
    movie_api_id = request.args.get('id')
    movie_to_add = movie.details(movie_api_id)
    new_movie = Movies(id=movie_to_add['id'], title=movie_to_add['title'],
                       img_url=f"{Movie_IMG}{movie_to_add['poster_path']}",
                       year=movie_to_add['release_date'].split('-')[0],
                       description=movie_to_add['overview']
                       )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('edit', id=movie_api_id))


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    movie_id = id
    movie_to_update = Movies.query.get(movie_id)
    print(movie_to_update.title)
    if request.method == 'POST':
        movie_to_update.rating = request.form['rating']
        movie_to_update.review = request.form['review']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie_to_update)


if __name__ == '__main__':
    app.run(debug=True)
