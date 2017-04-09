from models import _Book, connect
from sqlalchemy import or_
import logging
# Book API Calls - placed here since it has to do with data and will work closely with the database.
from apiclient.discovery import build
service = build('books', 'v1', developerKey='AIzaSyAn733zHPazBuXZ_HRomciIVzgr5pJpcHk')

def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

class Book():

    @classmethod
    def parse_book(cls, data):
        """
        Takes whatever craziness Google gives us and converts it to something reasonable.
        """
        book = data['volumeInfo']
        book['google_id'] = data['id']
        book['selfLink'] = data['selfLink']
        book['authors'] = ', '.join(book['authors'])
        for identifier in book['industryIdentifiers']:
            id_type = identifier['type']
            iden = identifier['identifier']
            book[id_type] = iden
        if 'ISBN_13' not in book:
             book['ISBN_13'] = ''
        if 'ISBN_10' not in book:
             book['ISBN_10'] = ''
        book = convert(book)
        return book

    @classmethod
    def find_book(cls, isbn=None, google_id=None):
        """
        Returns a book by its isbn or google_id
        """
        if isbn is not None:
            # In this case here, we're only returning one book. Search by the ISBN and return the massaged data.
            response = service.volumes().list(source="public", q="isbn:" + isbn).execute()
            if response['totalItems'] == 0:
                return None
            return cls.parse_book(response['items'][0])
        if google_id is not None:
            # Return the book by its Google ID
            try:
                response = service.volumes().get(volumeId=google_id).execute()
            except:
                return None
            return cls.parse_book(response)
        return None

    @classmethod
    def add_book(cls, google_id):
        """
        Adds a book to the database, or checks whether it is already there. 
        In either case, a book_id is returned.
        """
        try:
            db = connect()
            query = db.query(_Book).filter(_Book.google_id == google_id)
            if query.count() > 0:
                result = query.first()
                return result.id
            book = cls.find_book(google_id=google_id)
            if book is None:
                return None
            if 'subtitle' not in book:
                book['subtitle'] = ''
            new_book = _Book(google_id=google_id, google_link=book['selfLink'], title=book['title'], subtitle=book['subtitle'],
                         authors=book['authors'], publisher=book['publisher'],
                         description=book['description'], ISBN_10=book['ISBN_10'], ISBN_13=book['ISBN_13'], pages=book['pageCount'],
                         small_thumbnail=book['imageLinks']['smallThumbnail'], thumbnail=book['imageLinks']['thumbnail']) # published_date=book['publishedDate'],
            db.add(new_book)
            db.commit()
            book_id = new_book.id
            db.close()
            return book_id
        except:
            logging.debug("Something went wrong when inserting the book. :-(")
            db.rollback()
            db.close()
            raise