from handlers.base_handler import BaseHandler
import logging
import os
from urlparse import urlparse
# SAML stuff
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

class MetadataHandler(BaseHandler):
    def get(self):
        req = self.prepare_saml_request(self.request)
        auth = self.init_saml_auth(req)
        settings = auth.get_settings()
        metadata = settings.get_sp_metadata()
        errors = settings.validate_metadata(metadata)

        if len(errors) == 0:
            self.response.headers['Content-Type'] = "text/xml; charset=utf-8"
            #resp = make_response(metadata, 200)
            #resp.headers['Content-Type'] = 'text/xml'
            self.response.write(metadata)
        else:
            #resp = make_response(', '.join(errors), 500)
            self.response.write(', '.join(errors))
        print(self.session)
        return
        
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