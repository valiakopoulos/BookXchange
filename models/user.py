from models import _User, db

import logging, datetime

class User():
    
    @classmethod
    def login_user(cls, email, username, firstName, lastName):
        """
        Gets the user from the datastore, adds the user if not already there.
        We'll use the autoadd for now since that's how most SSO operations work.
        """
        logging.info('Attempting to login with email: ')
        logging.info(email)

        rows = db.query(_User).filter(_User.email == email).count()
        if rows > 0:
            logging.info('Found user!')
            #user.lastLogin = datetime.datetime.now()
            return True
        else:
            logging.info('User not found, creating one!')
            db.add(_User(email=email, username=username, first_name=firstName, last_name=lastName))
            db.commit()
            return True
           

    @classmethod
    def get_user(cls, email):
        return db.query(_User).filter(_User.email == email).first()