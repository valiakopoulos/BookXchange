import sys, os
if 'BOOKXCHANGE_PROD' not in os.environ:
    sys.path.append("C:\\Python27\\lib\\site-packages\\")
reload(sys)
sys.setdefaultencoding('utf-8')

import os, logging, webapp2, jinja2
from handlers import *


# Setup configuration
config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'cs595isgreat',}
config['SECRET_KEY'] = 'cs595isgreat'
config['SAML_PATH'] = os.path.join(os.path.dirname(__file__), 'saml')
config['STATIC_PATH'] = os.path.join(os.path.dirname(__file__), 'static')

# Add appropriate routes
# HAML Team - If you're adding new handles add them here. Make sure the a comma is added!
routes = [
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route('/addbook/<action><:/?>', handler=AddBookHandler, name='addbook'),
    webapp2.Route('/search', handler=SearchHandler, name='search'),
    webapp2.Route('/searchbook', handler=SearchBookHandler, name='searchbook'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/static/<directory>/<file>', StaticFileHandler),
    webapp2.Route('/user/<user_id><:/?>', handler=UserHandler, name='user'),
    webapp2.Route('/deactivate', handler=DeactivateBookHandler, name='deactivate'),
]

# If this variable is set, then use SAML.
if 'BOOKXCHANGE_PROD' in os.environ:
    print("Using UWM Login system")
    routes.append(webapp2.Route('/saml', handler=AuthHandler, name='saml'))
    routes.append(webapp2.Route('/saml/', handler=AuthHandler, name='samlslash'))
    routes.append(webapp2.Route('/saml/attrs', handler=AttrsHandler, name='samlattrs'))
    routes.append(webapp2.Route('/saml/metadata', handler=MetadataHandler, name='samlmetadata'))

app = webapp2.WSGIApplication(routes, config=config, debug=True)