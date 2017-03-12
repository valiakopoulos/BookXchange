from google.appengine.ext import ndb
from models.user import User
import logging, datetime

class UserReview(ndb.Model):
    reviewee = ndb.KeyProperty(kind=User)
    reviewer = ndb.KeyProperty(kind=User)
    comments = ndb.StringProperty()
    rating = ndb.IntegerProperty()
    datePosted = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def add_review(cls, forUser, byUser, comments, rating):
        new_review = UserReview(forUser=forUser, byUser=byUser, comments=comments, rating=rating)
        return new_review.put()

    @classmethod
    def get_reviews_by_reviewer(cls, reviewer):
        return UserReview.query(UserReview.reviewer == reviewer).fetch()

    @classmethod
    def get_reviews_by_reviewee(cls, reviewee):
        return UserReview.query(UserReview.reviewee == reviewee).fetch()