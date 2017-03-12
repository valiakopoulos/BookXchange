from handlers.base_handler import BaseHandler
from models.user import User
from models.book_listing import BookListing
import logging

class MainHandler(BaseHandler):
    def get(self):
        email = self.session.get('email')
        user = User.get_user(email)
        logging.info(user)
        buybooks = BookListing.get_available_books()
        sellbooks = BookListing.get_requested_books()
        context = {
            'title': "Book Xchange",
            'user': user,
            'buybooks': buybooks,
            'sellbooks': sellbooks
        }
        print(context)
        template = self.template_env.get_template('home.html')
        self.response.write(template.render(context))