from handlers.base_handler import BaseHandler
from models.user import User
from models.book import Book
from models.book_listing import BookListing
import logging

class AddBookHandler(BaseHandler):
    def get(self, action):
        email = self.session.get('email')
        user = User.get_user(email)
        if not user:
            return self.redirect('/login')
        logging.info(user)
        selling = False
        if action == 'sell':
            selling = True
        context = {
            'title': "Book Xchange - List a Book!",
            'user': user,
            'selling': selling,
            'getAction': True
        }
        template = self.template_env.get_template('addbook.html')
        self.response.write(template.render(context))

    def post(self, action):
        # Lets _try_ to add the book and all that.
        error = False
        binding = ''
        condition = ''
        google_id = self.request.get('google_id')
        try:
            binding = self.request.get('binding')
            condition = self.request.get('condition')
        except:
            pass
        comments = self.request.get('comments')
        # Quietly ignore errors for now
        try:
            price = float(self.request.get('price'))
        except:
            price = 0.0
        new_book = Book.add_book(google_id)
        if new_book is None:
            logging.debug('Error inserting book with google_id of ' + google_id + '!')
            error = True
        else:
            email = self.session.get('email')
            user = User.get_user(email)
            print(action)
            logging.info(action)
            if action == 'sell':
                BookListing.sell_book(new_book, user['id'], price, condition, comments)
            else:
                BookListing.request_book(new_book, user['id'], price, condition, comments)
        context = {
            'title': "Book Xchange - Book Listed!",
            'user': user,
            'error': error
        }
        template = self.template_env.get_template('addbook.html')
        self.response.write(template.render(context))