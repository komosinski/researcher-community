
from flask_login import current_user
from flask import  redirect, url_for, flash, request
import functools
from flask_login.config import EXEMPT_METHODS
from open_science import strings as STR
from open_science.models import User


def check_numeric_args(*argv):
    try:
        for arg in argv:
            arg = int(arg)
    except:
        return False
    return True


def admin_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('auth.login_page'))
        elif current_user.privileges_set < User.user_types_enum.ADMIN.value:
            flash(STR.ADMIN_ROLE_REQUIRED,
                  category='error')
            return redirect(url_for('main.home_page'))
        return func(*args, **kwargs)

    return decorated_view


def researcher_user_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('auth.login_page'))
        elif current_user.privileges_set < User.user_types_enum.RESEARCHER_USER.value:
            flash(STR.RESEARCHER_ROLE_REQUIRED,
                  category='warning')
            return redirect(url_for('main.home_page'))
        return func(*args, **kwargs)

    return decorated_view