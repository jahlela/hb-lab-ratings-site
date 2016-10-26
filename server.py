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


@app.route('/')
def index():
    """Homepage."""
    #a = jsonify([1,3])
    #return a
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)



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

    print "##############################################################"

    current_user = User.query.filter_by(email=username).first()

    
    if not current_user:
        # redirect to /register
        flash("No record found. Please register!")
        return redirect("/register")

    elif current_user and current_user.password == password:
        # store username in Flask session
        session["user_id"] = current_user.user_id
        flash("Successfully logged in!")
        return redirect("/")

    # if username in db and password belongs to same user, redirect to homepage 
    elif current_user.password != password:
        flash("Password does not match. Please try again.")
        return redirect("/")




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5003)
