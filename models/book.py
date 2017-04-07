from models import _Book, db
from sqlalchemy import or_
# Book API Calls - placed here since it has to do with data and will work closely with the database.
from apiclient.discovery import build
service = build('books', 'v1', developerKey='AIzaSyAn733zHPazBuXZ_HRomciIVzgr5pJpcHk')

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class Book():

    @classmethod
    def parse_book(cls, data):
        book = data['volumeInfo']
        book['google_id'] = data['id']
        book['selfLink'] = data['selfLink']
        book['authors'] = ', '.join(book['authors'])
        for identifier in book['industryIdentifiers']:
            id_type = identifier['type']
            iden = identifier['identifier']
            book[id_type] = iden
        if 'ISBN_13' not in book:
             book['ISBN_13'] = ''
        if 'ISBN_10' not in book:
             book['ISBN_10'] = ''
        book = convert(book)
        return book

    @classmethod
    def find_book(cls, isbn=None, google_id=None, page=None, searchTerms=None):
        if isbn is not None:
            # In this case here, we're only returning one book. Search by the ISBN and return the massaged data.
            response = service.volumes().list(source="public", q="isbn:" + isbn).execute()
            if response['totalItems'] == 0:
                return None
            return cls.parse_book(response['items'][0])
        if google_id is not None:
            # Return the book by its Google ID
            try:
                response = service.volumes().get(volumeId=google_id).execute()
            except:
                return None
            return cls.parse_book(response)
        if searchTerms is not None:
            # Primitive search. Lets begin with 0 books.
            books = []
            isbn10 = isbn13 = None
            splitTerms = searchTerms.split(' ')
            nums = []
            for i in range(len(splitTerms)):
                term = splitTerms[i]
                if len(term) == 10:
                    try:
                        isbn10 = int(term)
                    except:
                        pass
                if len(term) == 13:
                    try:
                        isbn13 = int(term)
                    except:
                        pass
                splitTerms[i] = '%' + term + '%'
            if isbn10 is not None:
                query = db.query(_Book).filter(_Book.isbn10 == isbn10)
                if query.count() > 0:
                    result = query.all();
                    for book in result:
                        books.append(book)
            if isbn13 is not None:
                query = db.query(_Book).filter(_Book.isbn13 == isbn13)
                if isbn10 is not None:
                    query = query.filter(_Book.isbn10 != isbn10)
                if query.count() > 0:
                    result = query.all();
                    for book in result:
                        books.append(book)
            # ISBN search over. Lets check other possible matches.
            for term in splitTerms:
                query = db.query(_Book)
                if isbn10 is not None:
                    query = query.filter(_Book.isbn10 != isbn10)
                if isbn13 is not None:
                    query = query.filter(_Book.isbn13 != isbn13)
                query = query.filter(or_(
                        _Book.title.like(term),
                        _Book.subtitle.like(term),
                        _Book.authors.like(term),
                        _Book.publisher.like(term),
                        _Book.description.like(term)
                    ))
                result = query.all();
                for book in result:
                    books.append(book)
            # There might be duplicates :-(
            book_ids = set()
            final_books = []
            for book in books:
                if book.id not in book_ids:
                    final_books.append(book)
                    book_ids.add(book.id)
            return final_books
            # I want to use the Google API for this - but nothing yet. :-D
            """
            response = service.volumes().list(libraryRestrict='my-library', q=searchTerms).execute()
            if response['totalItems'] == 0:
                return None
            else:
                books = []
                for book in response['items']:
                    books.append(cls.parse_book(book))
                print(books)
                return books
            """
        return None

    #@classmethod
    #def add_book_to_library(cls, google_id):
    #    response = service.volumes().get(volumeId=google_id).execute()

    @classmethod
    def add_book(cls, google_id):
        query = db.query(_Book).filter(_Book.google_id == google_id)
        if query.count() > 0:
            result = query.first()
            return result.id
        book = cls.find_book(google_id=google_id)
        if book is None:
            return None
        if 'subtitle' not in book:
            book['subtitle'] = ''
        new_book = _Book(google_id=google_id, google_link=book['selfLink'], title=book['title'], subtitle=book['subtitle'],
                     authors=book['authors'], publisher=book['publisher'],
                     description=book['description'], ISBN_10=book['ISBN_10'], ISBN_13=book['ISBN_13'], pages=book['pageCount'],
                     small_thumbnail=book['imageLinks']['smallThumbnail'], thumbnail=book['imageLinks']['thumbnail']) # published_date=book['publishedDate'],
        db.add(new_book)
        db.flush()
        db.commit()

        return new_book.id

"""
from google.appengine.ext import ndb
import logging, datetime

class Book(ndb.Model):
    title = ndb.StringProperty()
    author = ndb.StringProperty()
    edition = ndb.StringProperty()
    isbn10 = ndb.StringProperty()
    isbn13 = ndb.StringProperty()
    binding = ndb.StringProperty()
    reviews = ndb.IntegerProperty(default=0)
    rating = ndb.FloatProperty(default=0.0)
    dateAdded = ndb.DateTimeProperty(auto_now_add=True)
    #searchTerms = ndb.ComputedProperty(_computed_property, repeated=True)
        #lambda self: (" ".join(self.author + [self.title, self.isbn13, self.isbn10])).lower().split(), repeated=True)

    @classmethod
    def add_book(cls, title, author, edition, isbn10, isbn13, binding):
        new_book = Book(title=title, author=author, edition=edition, isbn10=isbn10, isbn13=isbn13, binding=binding)
        return new_book.put()

    @classmethod
    def search(cls, searchTerms):
        searchTerms = searchTerms.lower().split()
        return Book.query(Book.searchTerms.IN(searchTerms)).fetch()

    @classmethod
    def exists(cls, isbn13):
        return False
"""