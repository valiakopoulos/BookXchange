from handlers.base_handler import BaseHandler
import logging
import os
from urlparse import urlparse
# SAML stuff
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils

class AuthHandler(BaseHandler):
    def get(self):
        req = self.prepare_saml_request(self.request)
        auth = self.init_saml_auth(req)
        errors = []
        not_auth_warn = False
        success_slo = False
        attributes = False
        paint_logout = False

        print(self.request.GET)
        if 'sso' in self.request.GET:
            return self.redirect(auth.login())
        elif 'sso2' in self.request.GET:
            return_to = '%sattrs/' % self.request.host_url
            return self.redirect(auth.login(return_to))
        elif 'slo' in self.request.GET:
            name_id = None
            session_index = None
            if 'samlNameId' in self.session:
                name_id = self.session['samlNameId']
            if 'samlSessionIndex' in self.session:
                session_index = self.session['samlSessionIndex']
            return self.redirect(auth.logout(name_id=name_id, session_index=session_index))
        elif 'acs' in self.request.GET:
            auth.process_response()
            errors = auth.get_errors()
            not_auth_warn = not auth.is_authenticated()
            if len(errors) == 0:
                print(auth.get_attributes())
                print(auth.get_nameid())
                print(auth.get_session_index())
                self.session['samlUserdata'] = auth.get_attributes()
                self.session['samlNameId'] = auth.get_nameid()
                self.session['samlSessionIndex'] = auth.get_session_index()
                self_url = OneLogin_Saml2_Utils.get_self_url(req)
                if 'RelayState' in self.request.POST and self_url != self.request.POST['RelayState']:
                    return self.redirect(auth.redirect_to(self.request.POST['RelayState']))
        elif 'sls' in self.request.GET:
            ## Not sure this will work
            dscb = lambda: self.session.clear()
            url = auth.process_slo(delete_session_cb=dscb)
            errors = auth.get_errors()
            if len(errors) == 0:
                if url is not None:
                    return self.redirect(url)
                else:
                    success_slo = True

        if 'samlUserdata' in self.session:
            paint_logout = True
            if len(self.session['samlUserdata']) > 0:
                attributes = self.session['samlUserdata'].items()
        print(self.session)
        context = {
            "errors" : errors,
            "not_auth_warn" : not_auth_warn,
            "success_slo" : success_slo,
            "attributes" : attributes,
            "paint_logout" : paint_logout
        }
        template = self.template_env.get_template('index.html')
        self.response.write(template.render(context))
    
    def post(self):
        req = self.prepare_saml_request(self.request)
        print(req)
        auth = self.init_saml_auth(req)
        errors = []
        not_auth_warn = False
        success_slo = False
        attributes = False
        paint_logout = False

        print(self.request.POST)
        if 'sso' in self.request.GET:
            return self.redirect(auth.login())
        elif 'sso2' in self.request.GET:
            return_to = '%sattrs/' % self.request.host_url
            return self.redirect(auth.login(return_to))
        elif 'slo' in self.request.GET:
            name_id = None
            session_index = None
            if 'samlNameId' in self.session:
                name_id = self.session['samlNameId']
            if 'samlSessionIndex' in self.session:
                session_index = self.session['samlSessionIndex']
            return self.redirect(auth.logout(name_id=name_id, session_index=session_index))
        elif 'acs' in self.request.GET:
            auth.process_response()
            errors = auth.get_errors()
            not_auth_warn = not auth.is_authenticated()
            if len(errors) == 0:
                self.session['samlUserdata'] = auth.get_attributes()
                self.session['samlNameId'] = auth.get_nameid()
                self.session['samlSessionIndex'] = auth.get_session_index()
                self_url = OneLogin_Saml2_Utils.get_self_url(req)
                if 'RelayState' in self.request.POST and self_url != self.request.POST['RelayState']:
                    return self.redirect(auth.redirect_to(self.request.POST['RelayState']))
        elif 'sls' in self.request.GET:
            ## Not sure this will work
            dscb = lambda: self.session.clear()
            url = auth.process_slo(delete_session_cb=dscb)
            errors = auth.get_errors()
            if len(errors) == 0:
                if url is not None:
                    return self.redirect(url)
                else:
                    success_slo = True

        if 'samlUserdata' in self.session:
            paint_logout = True
            if len(self.session['samlUserdata']) > 0:
                attributes = self.session['samlUserdata'].items()

        context = {
            "errors" : errors,
            "not_auth_warn" : not_auth_warn,
            "success_slo" : success_slo,
            "attributes" : attributes,
            "paint_logout" : paint_logout
        }
        template = self.template_env.get_template('index.html')
        self.response.write(template.render(context))
        
    def prepare_saml_request(self, request):
        url_data = urlparse(request.url)
        return {
            'https': 'on' if request.scheme == 'https' else 'off',
            'http_host': request.host,
            'server_port': url_data.port,
            'script_name': request.path,
            'get_data': request.GET.copy(),
            'post_data': request.POST.copy(),
            'query_string': request.query_string
        }
    
    def init_saml_auth(self, request):
        auth = OneLogin_Saml2_Auth(request, custom_base_path=os.path.join(os.getcwd(), 'saml'))
        return auth