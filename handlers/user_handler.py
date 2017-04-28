from handlers.base_handler import BaseHandler
from models.user import User
from models.book_listing import BookListing
import logging

class UserHandler(BaseHandler):
    def get(self, user_id):
        email = self.session.get('email')
        try:
            user = User.get_user(email)
            if user['is_banned']:
                self.redirect('/')
        except AttributeError:
            user = None
        if user is None:
            sellbooks = []
            buybooks = []
        else:
            sellbooks = BookListing.get_available_books(user_id)
            buybooks = BookListing.get_requested_books(user_id)

        try:
            other_user = User.get_user(id=user_id)
        except:
            other_user = None
        
        context = {
            'title': "Book Xchange",
            'other_user': other_user,
            'user': user,
            'buybooks': buybooks,
            'sellbooks': sellbooks
        }
        template = self.template_env.get_template('user.html')
        self.response.write(template.render(context))