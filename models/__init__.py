import os

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Using automap_base should create classes for us on the fly from the table definitions
Base = automap_base()
# Get the database URI set in app.yaml
# mysql+pymysql://root:hamlgroup@127.0.0.1:3306/bookxchange
engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
# Generate the classes!
Base.prepare(engine, reflect=True)

_Book = Base.classes.book
_BookListing = Base.classes.book_listing
_Transaction = Base.classes.transaction
_User = Base.classes.user
_UserReview = Base.classes.user_review

Session = sessionmaker(engine)
db = Session()
db.flush()