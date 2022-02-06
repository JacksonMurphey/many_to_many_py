from BOOK_app.config.mysqlconnection import connectToMySQL
from BOOK_app.models import author

class Book:

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM books;'
        results = connectToMySQL('books').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO books (title, num_of_pages, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, NOW(), NOW());'
        return connectToMySQL('books').query_db(query, data)

    @classmethod
    def get_one_with_author(cls, data):
        query = 'SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;'
        results = connectToMySQL('books').query_db(query, data)
        book = (cls(results[0]))

        if results[0]['authors.id'] == None:
            return (cls(results[0]))
        else:
            for author_dict in results:
                author_data = {
                    'id' : author_dict['authors.id'],
                    'name' : author_dict['name'],
                    'created_at' : author_dict['authors.created_at'],
                    'updated_at' : author_dict['authors.updated_at'],
                }
                book.authors.append(author.Author(author_data))
        return book 

    @classmethod
    def add_fav_author(cls, data):
        query = 'INSERT INTO favorites (book_id, author_id) VALUES (%(id)s, %(author_id)s)'
        return connectToMySQL('books').query_db(query, data)
        
    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );"
        results = connectToMySQL('books').query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        return books

