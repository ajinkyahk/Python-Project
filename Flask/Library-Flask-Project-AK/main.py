from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


db.create_all()

ALL_BOOKS = db.session.query(Book).all()


@app.route('/')
def home():
    ALL_BOOKS = db.session.query(Book).all()
    return render_template('index.html', books=ALL_BOOKS)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        print(request.form['book-rating'])
        book_dict = {
            'title': request.form['book-name'],
            'author': request.form['author-name'],
            'rating': request.form['book-rating'],
        }
        new_book = Book(title=book_dict['title'], author=book_dict['author'], rating=book_dict['rating'])
        print(new_book.id)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    book_id = id
    book_to_update = Book.query.get(book_id)
    if request.method == 'POST':
        book_to_update.rating = request.form['new-rating']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', book=book_to_update)


@app.route('/delete/<int:id>')
def delete(id):
        book_id = id
        book_to_delete = Book.query.get(book_id)
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
