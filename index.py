import os
import logging
import webapp2
import jinja2
#from onelogin.saml2.utils import OneLogin_Saml2_Utils

# Handler list
from handlers import *
#from handlers.auth_handler import AuthHandler
#from handlers.attrs_handler import AttrsHandler
#from handlers.metadata_handler import MetadataHandler

# Setup configuration
config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'cs595isgreat',}
config['SECRET_KEY'] = 'cs595isgreat'
#config['SAML_PATH'] = os.path.join(os.path.dirname(__file__), 'saml')

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/addbook/<action><:/?>', handler=AddBookHandler, name='addbook')
], config=config, debug=True)

    #webapp2.Route('/saml', handler=AuthHandler, name='saml'),
    #webapp2.Route('/saml/attrs', handler=AttrsHandler, name='samlattrs'),
	#webapp2.Route('/saml/metadata', handler=MetadataHandler, name='samlmetadata')