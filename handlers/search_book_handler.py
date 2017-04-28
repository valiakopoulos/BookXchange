from handlers.base_handler import BaseHandler
from models.book import Book
import logging

class SearchBookHandler(BaseHandler):
    def get(self):
        # No default GET method for the search page, redirect to home.
        # We could change this to show a more detailed search page if we wanted to.
        return self.redirect('/')

    def post(self):
        isbn = str(self.request.get('isbn'))
        context = {
            'books': Book.find_book(term=isbn)
        }
        if context['books'] is None:
            self.response.set_status(500)
            return
        print(context)
        template = self.template_env.get_template('search_book.html')
        self.response.write(template.render(context))