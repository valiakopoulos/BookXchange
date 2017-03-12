from handlers.base_handler import BaseHandler
from models.user import User
from models.book_listing import BookListing
import logging

class SearchHandler(BaseHandler):
    def get(self):
        # No default GET method for the search page, redirect to home.
        # We could change this to show a more detailed search page if we wanted to.
        return self.redirect('/')

    def post(self):
        email = self.session.get('email')
        user = User.get_user(email)
        logging.info(user)
        books = BookListing.search(self.request.get('search'))
        print(books)
        context = {
            'title': "Book Xchange",
            'user': user,
            'books': books
        }
        print(context)
        template = self.template_env.get_template('search.html')
        self.response.write(template.render(context))