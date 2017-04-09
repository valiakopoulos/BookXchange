from models import _User, _Book, _BookListing, connect
from sqlalchemy import or_
from copy import deepcopy
import logging, datetime

class BookListing():
    @classmethod
    def get_requested_books(cls):
        """
        Returns a list of books that are currently listed as "Wanted".
        """
        try:
            db = connect()
            query = db.query(
                _BookListing.id,
                _BookListing.price,
                _BookListing.comments,
                _BookListing.date_added,
                _BookListing.listing_type,
                _Book.google_id,
                _Book.google_link,
                _Book.title,
                _Book.subtitle,
                _Book.authors,
                _Book.publisher,
                _Book.published_date,
                _Book.description,
                _Book.ISBN_13,
                _Book.ISBN_10,
                _Book.pages,
                _Book.small_thumbnail,
                _Book.thumbnail,
                _User.username,
                _User.email,
                _User.first_name,
                _User.last_name,
                _User.rating).join(_Book, _User).filter(_BookListing.listing_type == 'Wanted')
            results = query.all()
            db.close()
            return results
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def get_available_books(cls):
        """
        Returns a list of books that are currently listed as "For Sale".
        """
        try:
            db = connect()
            query = db.query(
                _BookListing.id,
                _BookListing.price,
                _BookListing.comments,
                _BookListing.date_added,
                _BookListing.listing_type,
                _Book.google_id,
                _Book.google_link,
                _Book.title,
                _Book.subtitle,
                _Book.authors,
                _Book.publisher,
                _Book.published_date,
                _Book.description,
                _Book.ISBN_13,
                _Book.ISBN_10,
                _Book.pages,
                _Book.small_thumbnail,
                _Book.thumbnail,
                _User.username,
                _User.email,
                _User.first_name,
                _User.last_name,
                _User.rating).join(_Book, _User).filter(_BookListing.listing_type == 'For Sale')
            results = query.all()
            db.close()
            return results
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def sell_book(cls, book_id, user_id, price, condition, description):
        """
        Lists a book as "For Sale"
        """
        try:
            db = connect()
            new_listing = _BookListing(book_id=book_id, user_id=user_id, price=price, condition=condition,
                                       comments=description, date_added=datetime.datetime.now(), listing_type='For Sale')
            db.add(new_listing)
            db.commit()
            return True
        except:
            db.rollback()
            db.close()
            raise
    
    @classmethod
    def request_book(cls, book_id, user_id, price, condition, description):
        """
        Lists a book as "Wanted"
        """
        try:
            db = connect()
            new_listing = _BookListing(book_id=book_id, user_id=user_id, price=price, 
                                       comments=description, date_added=datetime.datetime.now(), listing_type='Wanted')
            db.add(new_listing)
            db.commit()
            return True
        except:
            db.rollback()
            db.close
            raise

    @classmethod
    def search_listings(cls, searchTerms, filters={}):
        """
        Search all listings given the search terms and filters.
        """
        # Please note, this is a search of only books in the database - we might expand this later.
        # Right now it'll grab all books, but we should exclude ones that are no longer active in the 
        # future.

        # Now begin working with the query
        try:
            db = connect()
            query = db.query(
                _BookListing.id,
                _BookListing.price,
                _BookListing.comments,
                _BookListing.date_added,
                _BookListing.listing_type,
                _Book.google_id,
                _Book.google_link,
                _Book.title,
                _Book.subtitle,
                _Book.authors,
                _Book.publisher,
                _Book.published_date,
                _Book.description,
                _Book.ISBN_13,
                _Book.ISBN_10,
                _Book.pages,
                _Book.small_thumbnail,
                _Book.thumbnail,
                _User.username,
                _User.email,
                _User.first_name,
                _User.last_name,
                _User.rating).join(_Book, _User)

            # Now add the search terms as filters. This is a killer SQL query and probably wouldn't be done this
            # way in real life. But for a small server, it'd survive.
            conditions = []
            for term in searchTerms.split(' '):
                length = len(term)
                if length == 10:
                    try:
                        isbn10 = int(term)
                        conditions.append(_Book.isbn10 == isbn10)
                    except ValueError:
                        pass
                elif length == 13:
                    try:
                        isbn13 = int(term)
                        conditions.append(_Book.isbn13 == isbn13)
                    except ValueError:
                        pass
                term = '%' + term + '%'
                conditions.append(_Book.title.like(term))
                conditions.append(_Book.subtitle.like(term))
                conditions.append(_Book.authors.like(term))
                conditions.append(_Book.publisher.like(term))
                conditions.append(_Book.description.like(term))
            query = query.filter(or_(*conditions))

            # Now's a good time to add filters!
            if 'listing_type' in filters:
                query = query.filter(_BookListing.listing_type == filters['listing_type'])
            if 'condition' in filters:
                conditions = []
                for cond in filters['condition']:
                    conditions.append(_BookListing.condition == cond)
                query = query.filter(or_(*conditions))
            if 'max_price' in filters:
                query = query.filter(_BookListing.price <= filters['max_price'])
            if 'low_price' in filters:
                query = query.filter(_BookListing.price >= filters['low_price'])

            results = query.all()
            db.close()
            return results
        except:
            db.rollback()
            db.close()
            raise