from open_science import db
from open_science.models import Notification
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request
from flask import abort
from open_science.routes_def import check_numeric_args


def notifications_page(page, unread):
    if not check_numeric_args(page):
        abort(404)
    page = int(page)

    if unread == 'False':
        notifications = current_user \
                        .rel_notifications \
                        .order_by(Notification.datetime.desc()) \
                        .paginate(page=page, per_page=20)
    else:
        notifications = current_user \
                        .rel_notifications \
                        .filter(Notification.was_seen.is_(False)) \
                        .order_by(Notification.datetime.desc()) \
                        .paginate(page=page, per_page=20)

    if not notifications:
        flash('You don\'t have any notifications', category='success')
        return redirect(url_for('profile_page', user_id=current_user.id))

    return render_template('notification/notifications_page.html',
                           page=page, unread=unread, results=notifications)


def update_notification_and_redirect():
    notification_id = int(request.args.get('notification_id'))
    url = request.args.get('url')

    notification = Notification.query.filter(
        Notification.id == notification_id).first()

    if current_user.id != notification.user:
        abort(404)

    notification.was_seen = True
    db.session.commit()

    return redirect(url)
