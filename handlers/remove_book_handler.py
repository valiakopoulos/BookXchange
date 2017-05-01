from handlers.base_handler import BaseHandler
from models.user import User
from models.book import Book
from models.book_listing import BookListing
import logging

class RemoveBookHandler(BaseHandler):
    def post(self):
        email = self.session.get('email')
        user = User.get_user(email)
        id = self.request.get('book_id');
        logging.info('Removing book with ID: ' + id)
        BookListing.deactivate(id);
        self.response.write('Removed')