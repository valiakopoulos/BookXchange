from handlers.base_handler import BaseHandler
import logging

class LogoutHandler(BaseHandler):
    def get(self):
        try:
            del self.session['email']
        except KeyError:
            # This will happen if the user is already logged out. Ignore it and move on with life
            pass
        return self.redirect('/')