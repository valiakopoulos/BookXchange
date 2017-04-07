import os
import mimetypes
import logging
from handlers.base_handler import BaseHandler

class StaticFileHandler(BaseHandler):
    def get(self, directory, file):
        abs_path = os.path.abspath(os.path.join('static', directory, file))
        print(abs_path)
        logging.info(abs_path)
        if os.path.isdir(abs_path) or abs_path.find(os.getcwd()) != 0:
            self.response.set_status(403)
            return
        try:
            f = open(abs_path, 'r')
            self.response.headers.add_header('Content-Type', mimetypes.guess_type(abs_path)[0])
            self.response.out.write(f.read())
            f.close()
        except:
            self.response.set_status(404)