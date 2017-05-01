from models import _User, _Book, _BookListing, connect
from sqlalchemy import or_
from copy import deepcopy
import logging, datetime

class BookListing():
    @classmethod
    def get_requested_books(cls, user_id):
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
                _BookListing.status,
                _BookListing.condition,
                _BookListing.binding,
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
                _User.id.label('user_id'),
                _User.username,
                _User.email,
                _User.first_name,
                _User.last_name,
                _User.rating).join(_Book, _User).filter(_BookListing.listing_type == 'Wanted').filter(_User.id == user_id).filter(_BookListing.active==1)
            results = query.all()
            db.close()
            return results
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def get_available_books(cls, user_id):
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
                _BookListing.status,
                _BookListing.condition,
                _BookListing.binding,
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
                _User.id.label('user_id'),
                _User.username,
                _User.email,
                _User.first_name,
                _User.last_name,
                _User.rating).join(_Book, _User).filter(_BookListing.listing_type == 'For Sale').filter(_User.id == user_id).filter(_BookListing.active==1)
            results = query.all()
            db.close()
            print(results)
            return results
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def sell_book(cls, book_id, user_id, price, binding, condition, description):
        """
        Lists a book as "For Sale"
        """
        try:
            db = connect()
            new_listing = _BookListing(book_id=book_id, user_id=user_id, price=price, condition=condition,
                                       comments=description, binding=binding, date_added=datetime.datetime.now(), listing_type='For Sale')
            db.add(new_listing)
            db.commit()
            return True
        except:
            db.rollback()
            db.close()
            raise
    
    @classmethod
    def request_book(cls, book_id, user_id, price, binding, condition, description):
        """
        Lists a book as "Wanted"
        """
        try:
            db = connect()
            new_listing = _BookListing(book_id=book_id, user_id=user_id, price=price, 
                                       comments=description, binding=binding, date_added=datetime.datetime.now(), listing_type='Wanted')
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
                _BookListing.status,
                _BookListing.condition,
                _BookListing.binding,
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
                _User.id.label('user_id'),
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
                        conditions.append(_Book.ISBN_10 == isbn10)
                    except ValueError:
                        pass
                elif length == 13:
                    try:
                        isbn13 = int(term)
                        conditions.append(_Book.ISBN_13 == isbn13)
                    except ValueError:
                        pass
                term = '%' + term + '%'
                conditions.append(_Book.title.like(term))
                conditions.append(_Book.subtitle.like(term))
                conditions.append(_Book.authors.like(term))
                conditions.append(_Book.publisher.like(term))
                conditions.append(_Book.description.like(term))
            query = query.filter(or_(*conditions)).filter(_BookListing.active==1)

            # Now's a good time to add filters!
            if 'listing_type' in filters:
                query = query.filter(_BookListing.listing_type == filters['listing_type'])
            if 'binding' in filters:
                query = query.filter(_BookListing.binding == filters['binding'])
            if 'condition' in filters:
                query = query.filter(_BookListing.condition == filters['condition'])
            if 'max_price' in filters:
                query = query.filter(_BookListing.price <= filters['max_price'])
            if 'low_price' in filters:
                query = query.filter(_BookListing.price >= filters['low_price'])
            if 'ordering' in filters:
                if filters['ordering'] == '2':
                    query = query.order_by(_BookListing.price.desc())
                else:
                    query = query.order_by(_BookListing.price.asc())
            else:
                print('give up')
                query = query.order_by(_BookListing.price.asc())

            results = query.all()
            db.close()
            return results
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def deactivate(cls, listing_id):
        try:
            db = connect()
            result = db.query(_BookListing).filter(_BookListing.id==listing_id).one()
            result.active = '0'
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise
        
    @classmethod
    def remove(cls, listing_id):
        try:
            db = connect()
            result = db.query(_BookListing).filter(_BookListing.id==listing_id).delete()
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def mark_on_hold(cls, listing_id):
        try:
            db = connect()
            result = db.query(_BookListing).filter(_BookListing.id==listing_id).one()
            result.status = 'On Hold'
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def mark_sold(cls, listing_id):
        try:
            db = connect()
            result = db.query(_BookListing).filter(_BookListing.id==listing_id).one()
            result.status = 'Sold'
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise

    @classmethod
    def get_owner(cls, listing_id):
        try:
            db = connect()
            result = db.query(_BookListing.user_id).filter(_BookListing.id==listing_id).one()
            user_id = result.user_id
            print(user_id)# = user_id['user_id']
            db.close()
        except:
            db.rollback()
            db.close()
            raise
        return user_id