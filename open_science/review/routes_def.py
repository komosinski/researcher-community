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

    review = Review.query.filter(Review.id == review_id).first_or_404()

    form = ReviewEditForm()

    if form.validate_on_submit():
        if form.save.data:
            review.evaluation_novel = form.evaluation_novel.data/100
            review.evaluation_conclusion = form.evaluation_conclusion.data/100
            review.evaluation_error = form.evaluation_error.data/100
            review.evaluation_organize = form.evaluation_organize.data/100
            review.confidence = form.confidence.data/100
            review.text = form.text.data
            if review.publication_datetime != None:
                review.edit_counter = review.edit_counter + 1
            if True in form.check_anonymous.data:
                review.is_anonymous = True
            else:
                review.is_anonymous = False

            db.session.commit()
            flash('The review has been saved', category='success')
            return redirect(url_for('profile_page', user_id=current_user.id))
        elif form.submit.data:
            review.evaluation_novel = form.evaluation_novel.data/100
            review.evaluation_conclusion = form.evaluation_conclusion.data/100
            review.evaluation_error = form.evaluation_error.data/100
            review.evaluation_organize = form.evaluation_organize.data/100
            review.confidence = form.confidence.data/100
            review.text = form.text.data
            review.publication_datetime = dt.datetime.utcnow()
            if True in form.check_anonymous.data:
                review.is_anonymous = True
            else:
                review.is_anonymous = False

            db.session.commit()
            flash('The review has been added', category='success')
            return redirect(url_for('profile_page', user_id=current_user.id))

            

    elif request.method == 'GET':
        form.evaluation_novel.data = int(review.evaluation_novel*100)
        form.evaluation_conclusion.data = int(review.evaluation_conclusion*100)
        form.evaluation_error.data = int(review.evaluation_error*100)
        form.evaluation_organize.data = int(review.evaluation_organize*100)
        form.confidence.data = int(review.confidence*100)
        form.text.data = review.text

    return render_template('review/review_edit.html', form=form)