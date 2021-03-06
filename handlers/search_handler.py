from handlers.base_handler import BaseHandler
from models.user import User
from models.book import Book
from models.book_listing import BookListing
import logging
from apiclient.discovery import build

service = build('books', 'v1', developerKey='AIzaSyAn733zHPazBuXZ_HRomciIVzgr5pJpcHk')

class SearchHandler(BaseHandler):
    def get(self):
        # No default GET method for the search page, redirect to home.
        # We could change this to show a more detailed search page if we wanted to.
        return self.redirect('/')

    def post(self):
        email = self.session.get('email')
        user = User.get_user(email)
        post_values = dict(self.request.POST)
        filters = {}
        for k in post_values:
            if post_values[k] != '':
                filters[k] = post_values[k]
        print(filters)
        if user['is_banned']:
            self.redirect('/')
        listings = BookListing.search_listings(self.request.get('search'), filters)
        context = {
            'title': "Book Xchange",
            'user': user,
            'books': listings,
            'search': self.request.get('search'),
            'filters': filters
        }
        template = self.template_env.get_template('search.html')
        self.response.write(template.render(context))