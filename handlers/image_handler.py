from handlers.base_handler import BaseHandler
from models.user import User
from models.book_listing import BookListing
import logging

# Thanks Google!
# https://cloud.google.com/appengine/docs/standard/python/images/usingimages
# The below handler is copied from the Google docs above, we will need to modify it
# when we use the Book API.

class ImageHandler(BaseHandler):
    def get(self):
        greeting_key = ndb.Key(urlsafe=self.request.get('img_id'))
        greeting = greeting_key.get()
        if greeting.avatar:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(greeting.avatar)
        else:
            self.response.out.write('No image')