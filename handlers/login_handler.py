from webapp2 import uri_for
from handlers.base_handler import BaseHandler
from models.user import User
import logging, os


class LoginHandler(BaseHandler):
    def get(self):
        if 'BOOKXCHANGE_PROD' in os.environ:
            return self.redirect('https://idp.uwm.edu/idp/profile/SAML2/Unsolicited/SSO?providerId=https%3A%2F%2Fbookxchange-cs595.appspot.com%2Fsaml%2Fmetadata')
        logging.info("LoginHandler: get()")
        email = self.session.get('email')
        if not email:
            template = self.template_env.get_template('login.html')
            self.response.write(template.render())
        else:
            return self.redirect('/')
    
    def post(self):
        if 'BOOKXCHANGE_PROD' in os.environ:
            return self.redirect('https://idp.uwm.edu/idp/profile/SAML2/Unsolicited/SSO?providerId=https%3A%2F%2Fbookxchange-cs595.appspot.com%2Fsaml%2Fmetadata')
        logging.info("LoginHandler: post()")
        email = 'dev' + self.request.get('email')
        user = User.get_user(email)
        print('User:', user)
        if not user:
            user = User.login_user(email, email[3:email.index('@')], 'Dev', email[3:email.index('@') - 2])
        self.session['email'] = email
        self.redirect('/')