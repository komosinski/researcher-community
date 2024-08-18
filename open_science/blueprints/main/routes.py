import json
import os
from collections import OrderedDict

import pandas as pd
from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from sklearn.decomposition import PCA

from open_science.blueprints.main import bp
from flask import current_app as app
from open_science import strings as STR
from open_science.utils import admin_required
from open_science.blueprints.main.forms import ContactStaffForm
from open_science.models import MessageToStaff, User
from flask_login import current_user, logout_user
from flask import render_template, redirect, url_for, flash
import datetime as dt
from open_science import db
from flask import request
# TODO fix circular import schedule
#import open_science.schedule.schedule as schedule
from os.path import exists

from text_processing.search_engine import get_similar_users_to_user


@bp.before_app_request
def before_req():
    # MAINTENANCE_MODE
    if app.config['MAINTENANCE_MODE'] is True \
        and request.endpoint != 'admin.index' \
            and request.endpoint != 'main.disable_maintenance_mode':
        return render_template("maintenance.html")
    # READOLNY MODE
    if app.config['READONLY_MODE'] is True \
        and current_user.is_authenticated is True\
            and current_user.privileges_set < User.user_types_enum.ADMIN.value:
        logout_user()
        flash(STR.READOLNY_LOGOUT_INFO, category='warning')
        return redirect(url_for("main.home_page"))


@bp.route("/")
def home_page():
    users_plot_url = app.config['USERS_PLOT_2D_FILE_PATH']
    if app.config['HOME_PAGE_FLASH_TEST_VERSION_MSG']:
        flash(STR.FLASH_TEST_VERSION, category='warning')
    return render_template("home_page.html",
                           users_plot_url=users_plot_url)




@bp.route('/about')
def about_page():
    return render_template('about.html')


@bp.route('/privacy')
def privacy_page():
    return render_template('privacy.html')


@bp.route('/enable_maintenance')
@login_required
@admin_required
def enable_maintenance_mode():
    app.config.update(MAINTENANCE_MODE=True)
    return redirect(url_for('main.home_page'))


@bp.route('/disable_maintenance')
@login_required
@admin_required
def disable_maintenance_mode():
    app.config.update(MAINTENANCE_MODE=False)
    return redirect(url_for('main.home_page'))


@bp.route('/enable_readonly')
@login_required
@admin_required
def enable_readonly_mode():
    app.config.update(READONLY_MODE=True)
    return redirect(url_for('main.home_page'))


@bp.route('/disable_readonly')
@login_required
@admin_required
def disable_readonly_mode():
    app.config.update(READONLY_MODE=False)
    return redirect(url_for('main.home_page'))


@bp.route('/page/')
@bp.route('/page/<name>')
def auto_page(name=None):
    if not name:
        return redirect(url_for('main.home_page'))
    else:
        try:
            template = render_template(f'pages/{name}.html')
            return template
        except Exception:
            return redirect(url_for('main.home_page'))


@bp.route('/contribute')
def contribute_page():
    return render_template('help/contribute.html')


@bp.route('/help')
def help_page():
    return render_template('help/help.html')


@bp.route('/help/contact', methods=['GET', 'POST'])
@login_required
def contact_staff_page():
    form = ContactStaffForm()

    if form.validate_on_submit():
        try:
            mssg = MessageToStaff(sender=current_user.id, topic=form.topic.data, text=form.text.data,
                                date=dt.datetime.utcnow())
            db.session.add(mssg)
            db.session.commit()
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('main.home_page'))

        flash('Message has been sent', category='success')
        return redirect(url_for('main.help_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('help/contact_staff.html', form=form)


@bp.route("/plot3D")
def users_plot_3d():
    user_id = request.args.get('id', type=int)
    if user_id is None:
        return "Error: No id provided", 400
    if exists(app.config['USERS_PLOT_3D_FILE_PATH']):
        users_plot_url_3d = os.path.join(app.config['ROOTDIR'], app.config['USERS_PLOT_3D_FILE_PATH'])
        with open(users_plot_url_3d, 'r') as f:
            data = [json.loads(line) for line in f]
        return render_template("users_plot.html", user_id=user_id, data=data)
    else:
        return redirect(url_for('main.home_page'))


# TODO fix circular import schedule
# @bp.route('/admin/force_daily_jobs')
# @login_required
# @admin_required
# def force_daily_jobs():
#     schedule.daily_jobs()
#     flash('Daily jobs have been performed', category='success')
#     return redirect(url_for('main.home_page'))

# TODO fix circular import schedule
# @bp.route('/admin/start_scheduler')
# def start_scheduler():
#     schedule.run_scheduler()
#     return redirect(url_for('main.home_page'))

