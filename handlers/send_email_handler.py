from handlers.base_handler import BaseHandler
from models.user import User
from models.book import Book
from models.book_listing import BookListing
import logging
import smtplib

class SendEmailHandler(BaseHandler):
    def post(self):
        email = self.session.get('email')
        user = User.get_user(email)
        lid = self.request.get('listing_id');
        uid = self.request.get('user_id');
        other_user = User.get_user(id=uid)
        server = smtplib.SMTP('smtp.1and1.com', 587)
        #server.ehlo()
        server.starttls()
        server.login("username@example.com", "password")
 
        msg = self.request.get('message');

        server.sendmail(email, other_user['email'], msg)
        server.quit()
        owner = BookListing.get_owner(id)
        logging.info('Book Listing ID: ' + id)
        if int(id) == int(user['id']) or user['is_admin']:
            BookListing.mark_on_hold(lid)
            self.response.write('Sent')
        else:
            self.response.set_status(500)
            self.response.write('Error')