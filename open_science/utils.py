from datetime import datetime

from flask_login import current_user
from flask import redirect, url_for, flash, request
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


def build_comment_tree(comments):
    comment_dict = {comment.id: comment for comment in comments}
    root_comments = []

    for comment in comments:
        comment.children = []

    for comment in comments:
        if comment.comment_ref:
            parent = comment_dict.get(comment.comment_ref)
            if parent:
                parent.children.append(comment)
        else:
            root_comments.append(comment)

    for comment in comment_dict.values():
        comment.children.sort(key=lambda x: x.date)

    root_comments.sort(key=lambda x: x.date)

    return root_comments


def time_ago(dt, default="just now"):
    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:
        if period >= 1:
            period = int(period)
            return f"{period} {singular if period == 1 else plural} ago"

    return default
