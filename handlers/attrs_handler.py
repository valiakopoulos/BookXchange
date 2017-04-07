from handlers.base_handler import BaseHandler
import logging
import os
from urlparse import urlparse
# SAML stuff
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

class AttrsHandler(BaseHandler):
    def get(self):
        paint_logout = False
        attributes = False

        if 'samlUserdata' in self.session:
            paint_logout = True
            if len(self.session['samlUserdata']) > 0:
                attributes = self.session['samlUserdata'].items()
        context = {
            "paint_logout" : paint_logout,
            "attributes" : attributes
        }
        print(self.session)
        template = self.template_env.get_template('attrs.html')
        self.response.write(template.render(context))
        
    def prepare_saml_request(self, request):
        url_data = urlparse(request.url)
        return {
            'https': 'on' if request.scheme == 'https' else 'off',
            'http_host': request.host,
            'server_port': url_data.port,
            'script_name': request.path,
            'get_data': request.GET,
            'post_data': request.POST,
            'query_string': request.query_string
        }
    
    def init_saml_auth(self, request):
        auth = OneLogin_Saml2_Auth(request, custom_base_path=os.path.join(os.getcwd(), 'saml'))
        return auth