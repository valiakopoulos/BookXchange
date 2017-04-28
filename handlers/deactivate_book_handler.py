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
        logging.info('Book Listing ID: ' + id)
        if user['is_admin']:
            BookListing.deactivate(id)
        self.response.write('Deleted')