from models import _User, _Book, _BookListing, db
from copy import deepcopy
import logging, datetime

class BookListing():
    @classmethod
    def get_requested_books(cls):
        listings = []
        query = db.query(_BookListing, _User, _Book).join(_User).join(_Book).filter(_BookListing.listing_type == 'Wanted')
        results = query.all()
        for result in results:
            new_listing = result[2].__dict__
            new_listing['first_name'] = result[1].first_name
            new_listing['last_name'] = result[1].last_name
            new_listing['condition'] = result[0].condition
            new_listing['price'] = result[0].price
            new_listing['comments'] = result[0].comments
            new_listing['listing_type'] = result[0].listing_type
            listings.append(new_listing)
        return listings

    @classmethod
    def get_available_books(cls):
        listings = []
        query = db.query(_BookListing, _User, _Book).join(_User).join(_Book).filter(_BookListing.listing_type == 'For Sale')
        results = query.all()
        for result in results:
            new_listing = result[2].__dict__
            new_listing['first_name'] = result[1].first_name
            new_listing['last_name'] = result[1].last_name
            new_listing['condition'] = result[0].condition
            new_listing['price'] = result[0].price
            new_listing['comments'] = result[0].comments
            new_listing['listing_type'] = result[0].listing_type
            listings.append(new_listing)
        return listings

    @classmethod
    def sell_book(cls, book_id, user_id, price, condition, description):
        new_listing = _BookListing(book_id=book_id, user_id=user_id, price=price, condition=condition,
                                   comments=description, date_added=datetime.datetime.now(), listing_type='For Sale')
        db.add(new_listing)
        db.commit()
    
    @classmethod
    def request_book(cls, book_id, user_id, price, condition, description):
        new_listing = _BookListing(book_id=book_id, user_id=user_id, price=price, 
                                   comments=description, date_added=datetime.datetime.now(), listing_type='Wanted')
        db.add(new_listing)
        db.commit()

    @classmethod
    def get_listings(cls, books=None):
        if books is not None:
            listings = []
            for book in books:
                query = db.query(_BookListing, _User).join(_User).filter(_BookListing.book_id == book.id)
                if query.count() > 0:
                    results = query.all()
                    for result in results:
                        print(result)
                        new_listing = deepcopy(book.__dict__)
                        new_listing['first_name'] = result[1].first_name
                        new_listing['last_name'] = result[1].last_name
                        new_listing['condition'] = result[0].condition
                        new_listing['price'] = result[0].price
                        new_listing['comments'] = result[0].comments
                        new_listing['listing_type'] = result[0].listing_type
                        listings.append(new_listing)
            return listings