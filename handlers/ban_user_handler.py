from handlers.base_handler import BaseHandler
from models.user import User
import logging

class BanUserHandler(BaseHandler):
    def post(self):
        email = self.session.get('email')
        user = User.get_user(email)
        id = self.request.get('user_id');
        logging.info('Banning user with ID: ' + id)
        if user['is_admin']:
            User.ban_user(id)
            self.response.write('Banned')
        else:
            self.response.set_status(500)
            self.response.write('Error')