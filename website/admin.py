from flask.ext.login import current_user
from functools import wraps
from website import login_man, db
from website.models import User

def login_required(role):
    """Decorator function to check that the current user is allowed to
    access the page/resource. First, there is a check to see if the current
    user is authenticated, and then the user's role is checked.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated():
              return login_man.unauthorized()
            if current_user.role != role:
                return login_man.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def add_admin(username, password, fullname):
    """Add an admin user to the User table in the database."""
    user = User(username=username, role='admin', fullname=fullname)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
