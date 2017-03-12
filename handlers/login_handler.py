from handlers.base_handler import BaseHandler
from models.user import User
import logging


class LoginHandler(BaseHandler):
    def get(self):
        logging.info("LoginHandler: get()")
        email = self.session.get('email')
        if not email:
            template = self.template_env.get_template('login.html')
            self.response.write(template.render())
        else:
            return self.redirect('/')
    
    def post(self):
        logging.info("LoginHandler: post()")
        email = self.request.get('email')
        user = User.login_user(email)
        if user:
            logging.info("post(): Logged in user")
            self.session['email'] = email
            self.redirect('/')
        else:
            logging.info("post(): Error, couldn't find the user. :-(")
            template = self.template_env.get_template('login.html')
            self.response.write(template.render())