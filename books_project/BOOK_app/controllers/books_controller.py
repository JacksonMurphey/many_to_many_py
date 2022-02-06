from BOOK_app import app
from flask import render_template, redirect, request
from BOOK_app.models.author import Author
from BOOK_app.models.book import Book


@app.route('/books')
def book_dash():
    books = Book.get_all()
    return render_template('books_dash.html', books=books)

@app.route('/books/create', methods=['POST'])
def create_book():
    Book.save(request.form)
    return redirect('/books')

@app.route('/books/<int:book_id>')
def show_book(book_id):
    data = {
        'id': book_id
    }
    book = Book.get_one_with_author(data)
    authors = Author.unfavorited_authors(data)
    return render_template('books_view.html', book=book, authors=authors)

@app.route('/books/<int:book_id>/addfav', methods=['POST'])
def book_addFav(book_id):
    data = {
        'id' : book_id,
        'author_id': request.form['author_id']
    }
    
    Book.add_fav_author(data)
    Book.save(request.form)
    return redirect(f'/books/{book_id}')