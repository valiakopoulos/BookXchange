from google.appengine.ext import ndb
from models.user import User
from models.book import Book
from models.book_listing import BookListing
import logging, datetime

class Transaction(ndb.Model):
    seller = ndb.KeyProperty(kind=User)
    buyer = ndb.KeyProperty(kind=User)
    book = ndb.KeyProperty(kind=Book)
    listing = ndb.KeyProperty(kind=BookListing)
    price = ndb.FloatProperty(default=0.0)
    dateSold = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_transaction(cls, seller, buyer, book, price):
        new_transaction = Transaction(seller=seller, buyer=buyer, book=book, price=price)
        return new_transaction.put()