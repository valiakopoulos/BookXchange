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
