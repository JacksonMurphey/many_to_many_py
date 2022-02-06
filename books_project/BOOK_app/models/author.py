from BOOK_app.config.mysqlconnection import connectToMySQL
from BOOK_app.models import book
from flask import flash

class Author:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM authors;'
        results = connectToMySQL('books').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO authors (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());'
        return connectToMySQL('books').query_db(query, data)

    @classmethod
    def get_one_with_book(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;'
        results = connectToMySQL('books').query_db(query, data)
        author = (cls(results[0]))

        if results[0]['books.id'] == None:
            return (cls(results[0]))
        else:
            for book_dict in results:
                book_data = {
                    'id' : book_dict['books.id'],
                    'title' : book_dict['title'],
                    'num_of_pages' : book_dict['num_of_pages'],
                    'created_at' : book_dict['books.created_at'],
                    'updated_at' : book_dict['books.updated_at'],
                }
                author.books.append(book.Book(book_data))
        return author 

    @classmethod
    def add_fav_book(cls, data):
        query = 'INSERT INTO favorites (author_id, book_id) VALUES (%(id)s, %(book_id)s)'
        return connectToMySQL('books').query_db(query, data)


    #NOTE NOTE NOTE : This how to return a list of objects that the user doesnt currently have/subscribe to.  
    # Well if I can get it to work..10/4/21.. update: see unfavorited_authors
    # @classmethod
    # def no_fav_book(cls, data):
    #     query='SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );'
    #     results = connectToMySQL('books').query_db(query, data)
    #     books = []
    #     for book in results:
    #         books.append(cls(book))
    #     return books

    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
        authors = []
        results = connectToMySQL('books').query_db(query,data)
        for row in results:
            authors.append(cls(row))
        return authors
