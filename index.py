import os
import logging
import webapp2
import jinja2
import sys
sys.path.insert(0, 'lib')
os.environ['APPLICATION_ID'] = 'bookxchange-cs595'
import google
google.__path__.append('/home/steve/wsl/cs595/BookXchange/lib/google')
datastore_file = '/dev/null'
from google.appengine.api import apiproxy_stub_map,datastore_file_stub
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
stub = datastore_file_stub.DatastoreFileStub('bookxchange-cs595', datastore_file, '/')
apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)
from whitenoise import WhiteNoise



from rocket import Rocket
from onelogin.saml2.utils import OneLogin_Saml2_Utils

# Handler list
from handlers import *

# Setup configuration
config = {}
config['webapp2_extras.sessions'] = {'secret_key': 'cs595isgreat',}
config['SECRET_KEY'] = 'cs595isgreat'
config['SAML_PATH'] = os.path.join(os.path.dirname(__file__), 'saml')

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route('/login', handler=LoginHandler, name='login'),
    webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
    webapp2.Route('/addbook/<action><:/?>', handler=AddBookHandler, name='addbook'),
    webapp2.Route('/search', handler=SearchHandler, name='search'),
    webapp2.Route('/saml', handler=AuthHandler, name='saml'),
    webapp2.Route('/saml/attrs', handler=AttrsHandler, name='samlattrs'),
	webapp2.Route('/saml/metadata', handler=MetadataHandler, name='samlmetadata')
], config=config, debug=True)

    #webapp2.Route('/saml', handler=AuthHandler, name='saml'),
    #webapp2.Route('/saml/attrs', handler=AttrsHandler, name='samlattrs'),
	#webapp2.Route('/saml/metadata', handler=MetadataHandler, name='samlmetadata')

def run_server():
    # Setup logging
    log = logging.getLogger('Rocket')
    log.setLevel(logging.INFO)
    log.addHandler(logging.StreamHandler(sys.stdout))

    app = webapp2.WSGIApplication([
        webapp2.Route('/', handler=MainHandler, name='home'),
        webapp2.Route('/login', handler=LoginHandler, name='login'),
        webapp2.Route('/logout', handler=LogoutHandler, name='logout'),
        webapp2.Route('/addbook/<action><:/?>', handler=AddBookHandler, name='addbook'),
        webapp2.Route('/search', handler=SearchHandler, name='search'),
        webapp2.Route('/saml', handler=AuthHandler, name='saml'),
        webapp2.Route('/saml/attrs', handler=AttrsHandler, name='samlattrs'),
	    webapp2.Route('/saml/metadata', handler=MetadataHandler, name='samlmetadata')
    ], config=config, debug=True)
    app = WhiteNoise(app, root='/home/steve/wsl/cs595/BookXchange/static', prefix='static')

    # Set the configuration of the web server
    server = Rocket(interfaces=('0.0.0.0', 5000), method='wsgi',
                    app_info={"wsgi_app": app})

    # Start the Rocket web server
    server.start()

if __name__ == "__main__":
    run_server()