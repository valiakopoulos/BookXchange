from handlers.base_handler import BaseHandler
from models.user import User
import logging

class ChangeAdminHandler(BaseHandler):
    def get(self):
        email = self.session.get('email')
        user = User.get_user(email)
        User.change_admin(int(user['id']))
        self.redirect('/')