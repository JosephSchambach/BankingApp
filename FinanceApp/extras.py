from flask import render_template, session, redirect
from functools import wraps

# require a user login
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# return an error message
def error(message, code):
    return render_template("error.html", message=message, code=code)

# define us dollars
def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"