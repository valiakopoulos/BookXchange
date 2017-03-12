from google.appengine.ext import ndb
import logging, datetime

class User(ndb.Model):
    email = ndb.StringProperty()
    displayName = ndb.StringProperty()
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()
    lastLogin = ndb.DateTimeProperty(auto_now_add=True)
    isAdmin = ndb.BooleanProperty(default=False)
    isBanned = ndb.BooleanProperty(default=False)
    bannedReason = ndb.StringProperty()
    
    @classmethod
    def login_user(cls, email):
        """
        Gets the user from the datastore, adds the user if not already there.
        We'll use the autoadd for now since that's how most SSO operations work.
        """
        logging.info('Attempting to login with email: ' + email)
        user = User.query().filter(User.email == email).get()
        if user:
            logging.info('Found user!')
            user.lastLogin = datetime.datetime.now()
            return user
        else:
            logging.info('User not found, creating one!')
            newUser = User(email=email)
            return newUser.put()

    @classmethod
    def get_user(cls, email):
        return User.query().filter(User.email == email).get()

"""
from google.cloud import datastore

ds = datastore.Client()

class Users():
    #
    #Users {
    #    email: String
    #    isAdmin: Boolean
    #}
    #

    @classmethod
    def login_user(cls, email):
        # Check that this person exists. If so, return the user. Otherwise create it!
        user = get_user(email)
        if user:
            return user
        else:
            new_user = datastore.Entity(ds.key('Users'))
            new_user.update({
                'email': email,
            })
            ds.put(new_user)
            return new_user


    @classmethod
    def get_user(cls, email):
        query = ds.query(kind='Users')
        query.add_filter('email', '=', email)
        results = list(query.fetch())
        if results:
            return results[0]
        else:
            return None
"""