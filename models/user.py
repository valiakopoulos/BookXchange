from models import _User, connect, _BookListing, _Transaction, _UserReview
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import logging, datetime

class User():
    
    @classmethod
    def login_user(cls, email, username, firstName, lastName):
        """
        Gets the user from the datastore, adds the user if not already there.
        We'll use the autoadd for now since that's how most SSO operations work.
        """
        db = connect()
        try:
            #logging.info('Attempting to login with email: ' + email)
            result = db.query(_User).filter(_User.email == email).one()
            result.last_login = datetime.datetime.now()
            db.commit()
            db.close()
            return True
        except NoResultFound:
            logging.info('User not found, creating one!')
            db.add(_User(email=email, username=username, first_name=firstName, last_name=lastName, last_login=datetime.datetime.now()))
            db.commit()
            db.close()
            return True
        except MultipleResultsFound:
            logging.debug('Multiple accounts found for this email, this shouldn\' happen.... :-(')
            db.rollback()
            db.close()
            return False
        except:
            logging.debug('A different error occured than was expected.... What to do?')
            db.rollback()
            db.close()
            raise

    @classmethod
    def get_user(cls, email=None, id=None):
        """
        Returns a dictionary of the user data. Must provide either an email or an id.
        """
        db = connect()
        try:
            #logging.info('Attempting to get the user via the email ' + str(email) + ' or the id ' + str(id) + '.')
            query = db.query(_User)
            if email is not None:
                query = query.filter(_User.email == email)
            elif id is not None:
                query = query.filter(_User.id == id)
            else:
                raise AttributeError('You must supply an email or user_id (from the database) in order to get the user.')
            user = query.one().__dict__
            user['sold'] = db.query(_Transaction).filter(_Transaction.seller_id==user['id']).count()
            user['purchased'] = db.query(_Transaction).filter(_Transaction.buyer_id==user['id']).count()
            user['listed_for_sale'] = db.query(_BookListing).filter(_BookListing.user_id==user['id']).filter(_BookListing.listing_type=='For Sale').filter(_BookListing.active=='1').count()
            user['listed_for_purchase'] = db.query(_BookListing).filter(_BookListing.user_id==user['id']).filter(_BookListing.listing_type=='Wanted').filter(_BookListing.active=='1').count()
            user['reviews'] = db.query(_UserReview.rating,
                                       _UserReview.comments,
                                       _UserReview.date_posted,
                                       _User.first_name,
                                       _User.last_name,
                                       _User.email,
                                       _User.username,
                                       _User.id).join(_User, _User.id==_UserReview.reviewer_id).filter(_UserReview.reviewee_id==user['id']).all()
            db.close()
            #print(user)
            return user
        except NoResultFound:
            logging.info('User not found.')
            db.close()
            return None
        except MultipleResultsFound:
            logging.debug('Multiple accounts found for this email, this shouldn\' happen.... :-(')
            db.rollback()
            db.close()
            return False
        except:
            logging.debug('A different error occured than was expected.... What to do?')
            db.rollback()
            db.close()
            raise
        return None

    @classmethod
    def change_admin(cls, user_id):
        try:
            db = connect()
            result = db.query(_User).filter(_User.id==user_id).one()
            if result.is_admin == 1:
                result.is_admin = 0
            else:
                result.is_admin = 1
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise
        return user_id

    @classmethod
    def ban_user(cls, user_id):
        try:
            db = connect()
            result = db.query(_User).filter(_User.id==user_id).one()
            result.is_banned = 1
            db.commit()
            for listing in db.query(_BookListing).filter(_BookListing.user_id==user_id).all():
                listing.active = 0
            db.commit()
            db.close()
        except:
            db.rollback()
            db.close()
            raise