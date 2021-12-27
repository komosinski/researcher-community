from open_science.review.forms import ReviewRequestForm, ReviewEditForm
from open_science import db
from open_science.models import  ReviewRequest, Review
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request
from flask import abort
import datetime as dt
from open_science.routes_def import check_numeric_args


def review_request_page(request_id):
    # TODO: show paper abstract ...
    if not check_numeric_args(request_id):
        abort(404)

    review_request = ReviewRequest.query.filter(ReviewRequest.id == request_id, ReviewRequest.requested_user == current_user.id).first_or_404()
    if review_request.decision is not None:
        flash(f'Review request has been resolved',category='warning')
        return redirect(url_for('profile_page', user_id=current_user.id))

    form = ReviewRequestForm()
    if form.validate_on_submit():
        if form.submit_accept.data:
            review_request.decision = True
            review_request.acceptation_date = dt.date.utctoday()
            review = Review(creator = current_user.id, related_paper_version=review_request.paper_version)
            review.deadline_date = dt.datetime.utcnow().date() + dt.timedelta(days = int(form.prepare_time.data))
            db.session.add(review)
            flash(f'Review request accepted',category='success')
        elif form.submit_decline.data:
            review_request.decision = False
            review_request.other_reason = form.other_reason.data
            review_request.set_reasons(form.declined_reason.data)
            flash(f'Review request declined',category='warning')

        db.session.add(review_request)
        db.session.commit()
        
        return redirect(url_for('profile_page', user_id=current_user.id))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/review_request.html',form=form)

# TODO: complete this page
def review_edit_page(review_id):

    form = ReviewEditForm()

    return render_template('review/review_edit.html', form=form)