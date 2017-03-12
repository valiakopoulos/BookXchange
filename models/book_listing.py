from google.appengine.ext import ndb
from models.book import Book
from models.user import User
import logging, datetime

class BookListing(ndb.Model):
    book = ndb.KeyProperty(kind=Book)
    owner = ndb.KeyProperty(kind=User)
    price = ndb.FloatProperty(default=0.0)
    condition = ndb.StringProperty(default='')
    active = ndb.BooleanProperty(default=True)
    description = ndb.StringProperty(default='')
    forSale = ndb.BooleanProperty(default=False)
    wanted = ndb.BooleanProperty(default=False)
    dateAdded = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def sell_book(cls, book, owner, price, condition='', description=''):
        new_listing = BookListing(book=book, owner=owner, price=price, condition=condition, description=description, forSale=True, parent=owner)
        return new_listing.put()

    @classmethod
    def buy_book(cls, book, owner, price, condition='', description=''):
        new_listing = BookListing(book=book, owner=owner, price=price, condition=condition, description=description, wanted=True, parent=owner)
        return new_listing.put()

    @classmethod
    def search(cls, searchTerms):
        #http://stackoverflow.com/questions/14291863/ndb-query-partial-string-matching
        searchTerms = searchTerms.lower().split()
        return BookListing.query(Book.searchTerms.IN(searchTerms)).fetch()

    @classmethod
    def get_requested_books(cls):
        return BookListing.query(BookListing.forSale == False).fetch()

    @classmethod
    def get_available_books(cls):
        return BookListing.query(BookListing.forSale == True).fetch()