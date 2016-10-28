"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

import correlation 

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
           """Provide helpful representation when printed."""

           return "<User user_id=%s email=%s>" % (self.user_id,
                                                  self.email)

    # There is a relationship defined between User and Rating in Rating.
    # Backref to Rating is "ratings"

class Movie(db.Model):
    """Movie and its info"""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True) 
    imdb_url = db.Column(db.String(75), nullable=False)

    # There is a relationship defined between Movie and Rating in Rating.
    # Backref to Rating is "ratings"

class Rating(db.Model):
    """Ratings for each movie"""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
    # Define relationship to user
    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
        return s % (self.rating_id, self.movie_id, self.user_id,
                    self.score)
##############################################################################
# Predictions Logic
 
# def predict_rating(user, movie):
#     """Predict a user's rating of a movie."""

#     other_ratings = movie.ratings
#     other_users = [ r.user for r in other_ratings ]

#     similarities = [
#         (user.similarity(other_user), other_user)
#         for other_user in other_users
#     ]

#     similarities.sort(reverse=True)
#     sim, best_match_user = similarities[0]

#     for rating in other_ratings:
#         if rating.user_id == best_match_user.user_id
#            return rating.score * sim

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
