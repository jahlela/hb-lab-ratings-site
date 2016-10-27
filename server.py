"""Movie Ratings."""

from jinja2 import StrictUndefined
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import func

from flask import Flask, jsonify, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Movie, Rating
# Please don't import session from db -- it may be confused with Flask session


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.before_request
def before_request():
    """ Default session["logged_in"] to false if next endpoint is not /login"""

    if "logged_in" not in session and request.endpoint != 'login':
        session["logged_in"] = False


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", 
                            users=users)


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", 
                            movies=movies)


@app.route("/register", methods=["GET"])
def register_form():
    """Register users."""

    return render_template("register_form.html") 



@app.route("/register", methods=["POST"])
def register_new_user():
    """Add new users."""
    
    username = request.form['username']
    password = request.form['password']

    user_in_db = db.session.query(User).filter(User.email==username).all()

    # if username (email) is in not in database, add them 
    if not user_in_db:
        # add to db

        new_user = User(email=username, password=password)
        db.session.add(new_user)
        db.session.commit()

    # redirect to homepage
    return redirect("/")

@app.route("/login", methods=['POST'])
def user_login():
    """User login"""

    username = request.form['username']
    password = request.form['password']

    if "user_id" not in session:
        session["user_id"] = {}

    current_user = User.query.filter_by(email=username).first()

    # check login credentials against database, and route user accordingly
    if not current_user:
        # redirect to /register
        flash("No record found. Please register!")
        return redirect("/register")

    elif current_user and current_user.password == password:
        # store username in Flask session
        session["user_id"] = current_user.user_id
        session["logged_in"] = True
        flash("Successfully logged in!")
        return redirect("/")

    # if username in db and password belongs to same user, redirect to homepage 
    elif current_user.password != password:
        flash("Password does not match. Please try again.")
        return redirect("/")

@app.route('/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    session['user_id'] = None
    session['logged_in'] = False

    # if 'username'

    flash("Successfully logged out!")
    return redirect("/")

@app.route('/users/<user_id>', methods=["GET"])
def user_details(user_id):

    # get user object from database with their user_id
    user = User.query.get(user_id)

    return render_template('/user_details.html',
                            user=user)


@app.route('/movies/<movie_id>', methods=["GET"])
def movie_details(movie_id):

    # get movie object from database with its movie_id
    movie = Movie.query.get(movie_id)
    print movie
    return render_template('/movie_details.html',
                            movie=movie)





@app.route('/add_rating', methods=["POST"])
def add_rating():

    #new score --- get from the form using request.args.get('score')

    # movie_id   
    # user_id    from session key --> email, get user object and ask for id attr

    # if new_score:
    #     new_rating = Rating(user_id=user_id, movie_id=movie_id, score=new_score)
    #     new_rating.score = new_score
    #     db.session.commit()
    # else:





    rating_query = Rating.query.filter(Rating.user_id == user_id, 
                                       Rating.movie_id == movie_id)









if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5003)
