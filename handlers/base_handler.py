# This code is from:
#   http://webapp2.readthedocs.io/en/latest/api/webapp2_extras/sessions.html
# It works great for a simple example. :-) 

from webapp2 import RequestHandler, cached_property, uri_for
from webapp2_extras import sessions
import jinja2
import os

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), 'templates')))
template_env.globals = {
    'uri_for': uri_for
}

class BaseHandler(RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_env = template_env
        self.context = {}
        
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()