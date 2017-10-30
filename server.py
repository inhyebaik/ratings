"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from model import User, Rating, Movie, connect_to_db, db


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

    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register')
def register_form():
    """Prompts user to register/sign in"""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Adds new user to DB"""
    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter(User.email == email).count() != 0:
        db_user = User.query.filter(User.email == email).one()
        if db_user.password == password:
            session['user_id'] = db_user.user_id
            flash("You have successfully logged in!")
            return redirect('/')
        else:
            flash("Wrong credentials, try again")
            return redirect('/register')
    else:
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You're now added as a new user! Welcome!")
        db_user = User.query.filter(User.email == email).one()
        session['user_id'] = db_user.user_id
        return redirect('/')


@app.route('/logout')
def log_out():
    """Logs a user out"""
    session['user_id'] = None
    flash("You have successfully logged out!")

    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)



    app.run(port=5000, host='0.0.0.0')
