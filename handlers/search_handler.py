from handlers.base_handler import BaseHandler
from models.user import User
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
        logging.info(user)
        books = BookListing.search(self.request.get('search'))
        # Find a book with Google Books API
        response = service.volumes().list(source="public", q="isbn:0133594149").execute()
        for book in response.get('items', []):
            logging.info('Title: ' + str(book['volumeInfo']['title']) + ', Authors: ' + str(book['volumeInfo']['authors']))
        print(books)
        context = {
            'title': "Book Xchange",
            'user': user,
            'books': books
        }
        print(context)
        template = self.template_env.get_template('search.html')
        self.response.write(template.render(context))