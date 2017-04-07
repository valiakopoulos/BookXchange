from handlers.base_handler import BaseHandler
import logging, os

class LogoutHandler(BaseHandler):
    def get(self):
        if 'BOOKXCHANGE_PROD' in os.environ:
            return self.redirect('https://bookxchange-cs595.appspot.com/saml/?slo')
        try:
            del self.session['email']
        except KeyError:
            # This will happen if the user is already logged out. Ignore it and move on with life
            pass
        return self.redirect('/')