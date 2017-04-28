from handlers.base_handler import BaseHandler
from models.user import User
from models.book_listing import BookListing
import logging

class MainHandler(BaseHandler):
    def get(self):
        email = self.session.get('email')
        banned = False
        try:
            user = User.get_user(email)
            if user['is_banned']:
                banned = True
        except AttributeError:
            user = None
        if user is None:
            sellbooks = []
            buybooks = []
        else:
            sellbooks = BookListing.get_available_books(user['id'])
            buybooks = BookListing.get_requested_books(user['id'])

        
        context = {
            'title': "Book Xchange",
            'user': user,
            'buybooks': buybooks,
            'sellbooks': sellbooks,
            'banned': banned
        }
        template = self.template_env.get_template('home.html')
        self.response.write(template.render(context))