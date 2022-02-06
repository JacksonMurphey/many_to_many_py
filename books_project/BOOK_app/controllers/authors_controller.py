
from BOOK_app import app
from flask import render_template, redirect, request
from BOOK_app.models.author import Author
from BOOK_app.models.book import Book

@app.route('/')
def index():
    #we will user this for login and registration
    return redirect('/authors')

@app.route('/authors')
def author_dash():
    
    authors = Author.get_all()
    return render_template('authors_dash.html', authors=authors)

@app.route('/authors/create', methods=['POST'])
def create_author():
    Author.save(request.form)
    return redirect('/authors')

@app.route('/authors/<int:author_id>')
def show_author(author_id):
    data = {
        'id': author_id
    }
    
    books = Book.unfavorited_books(data)
    author = Author.get_one_with_book(data)
    return render_template('authors_view.html',author=author, books=books)

@app.route('/authors/<int:author_id>/addfav', methods=['POST'])
def author_addFav(author_id):
    data = {
        'book_id' : request.form['book_id'],
        'id': author_id
    }
    
    Author.add_fav_book(data)
    Author.save(request.form)
    return redirect(f'/authors/{author_id}')
