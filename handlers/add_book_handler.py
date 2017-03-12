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
        title = self.request.get('title')
        author = self.request.get('author')
        edition = self.request.get('edition')
        isbn10 = self.request.get('isbn10')
        isbn13 = self.request.get('isbn13')
        binding = self.request.get('binding')
        condition = self.request.get('condition')
        description = self.request.get('description')
        price = float(self.request.get('price'))
        new_book = Book.add_book(title, author, edition, isbn10, isbn13, binding)
        email = self.session.get('email')
        user = User.get_user(email)
        if action == 'sell':
            BookListing.sell_book(new_book, user.key, price, condition, description)
        else:
            BookListing.buy_book(new_book, user.key, price, condition, description)
        logging.info(user)
        context = {
            'title': "Book Xchange - Book Listed!",
            'user': user
        }
        template = self.template_env.get_template('addbook.html')
        self.response.write(template.render(context))