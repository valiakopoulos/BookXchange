from handlers.base_handler import BaseHandler
from models.user import User
from models.book import Book
from models.book_listing import BookListing
import logging

class DeactivateBookHandler(BaseHandler):
    def post(self):
        email = self.session.get('email')
        user = User.get_user(email)
        id = self.request.get('listing_id');
        id = id.split('_')[2]
        owner = BookListing.get_owner(id)
        logging.info('Book Listing ID: ' + id)
        if int(id) == int(user['id']) or user['is_admin']:
            BookListing.deactivate(id)
            self.response.write('Deactivated')
        else:
            self.response.set_status(500)
            self.response.write('Error')