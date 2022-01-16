from open_science.review.forms import ReviewRequestForm, ReviewEditForm
from open_science import db
from open_science.models import PaperRevision, ReviewRequest, Review
from open_science.models import Suggestion
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request, abort
import json
from open_science.db_helper import get_hidden_filter

import datetime as dt
from open_science.routes_def import check_numeric_args


def review_request_page(request_id):
    # TODO: show paper abstract ...
    if not check_numeric_args(request_id):
        abort(404)

    review_request = ReviewRequest.query.filter(
        ReviewRequest.id == request_id,
        ReviewRequest.requested_user == current_user.id).first_or_404()
    if review_request.decision is not None:
        flash('Review request has been resolved', category='warning')
        return redirect(url_for('profile_page', user_id=current_user.id))

    form = ReviewRequestForm()
    if form.validate_on_submit():
        if form.submit_accept.data:
            review_request.decision = True
            review_request.acceptation_date = dt.datetime.utcnow().date()
            review = Review(creator=current_user.id,
                            related_paper_version=review_request.paper_version)
            review.deadline_date = dt.datetime.utcnow().date() + dt.timedelta(days=int(form.prepare_time.data))
            db.session.add(review)
            flash('Review request accepted', category='success')
        elif form.submit_decline.data:
            review_request.decision = False
            review_request.other_reason_text = form.other_reason_text.data
            review_request.set_reasons(form.declined_reason.data)
            flash('Review request declined', category='success')

        db.session.add(review_request)
        db.session.commit()

        return redirect(url_for('profile_page', user_id=current_user.id))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    paper_version = review_request.rel_related_paper_version

    data = {
        'abstract': paper_version.abstract,
        'pdf_url': paper_version.pdf_url,
        'anonymized_pdf_url': paper_version.anonymized_pdf_url
    }
    return render_template('review/review_request.html', form=form, data=data)


def review_edit_page(review_id):

    if not check_numeric_args(review_id):
        abort(404)

    review = Review.query.filter(Review.id == review_id).first_or_404()

    suggestions = [s.to_dict() for s in review.rel_suggestions]

    previous_reviews = review.get_previous_creator_reviews()

    form = ReviewEditForm()

    if form.validate_on_submit():
        if form.save.data:
            review.evaluation_novel = form.evaluation_novel.data/100
            review.evaluation_conclusion = form.evaluation_conclusion.data/100
            review.evaluation_error = form.evaluation_error.data/100
            review.evaluation_organize = form.evaluation_organize.data/100
            review.evaluation_accept = form.evaluation_accept.data
            review.confidence = form.confidence.data/100

            print(form.suggestionsField.data)
            suggestions = json.loads(form.suggestionsField.data)
            [db.session.delete(suggestion)
             for suggestion in review.rel_suggestions]
            review.rel_suggestions = [Suggestion(
                suggestion=s["suggestion"],
                location=s["location"]
            ) for s in suggestions]

            if review.publication_datetime is not None:
                # TODO: check if suggestions have changed
                review.edit_counter = review.edit_counter + 1

            review.is_anonymous = form.check_anonymous.data
            review.is_hidden = form.check_hide.data

            db.session.commit()
            flash('The review has been saved', category='success')
            return redirect(url_for('profile_page', user_id=current_user.id))
        elif form.submit.data:
            review.evaluation_novel = form.evaluation_novel.data/100
            review.evaluation_conclusion = form.evaluation_conclusion.data/100
            review.evaluation_error = form.evaluation_error.data/100
            review.evaluation_organize = form.evaluation_organize.data/100
            review.evaluation_accept = form.evaluation_accept.data
            review.confidence = form.confidence.data/100
            review.publication_datetime = dt.datetime.utcnow()

            print(form.suggestionsField.data)
            suggestions = json.loads(form.suggestionsField.data)
            [db.session.delete(suggestion)
             for suggestion in review.rel_suggestions]
            review.rel_suggestions = [Suggestion(
                suggestion=s["suggestion"],
                location=s["location"]
            ) for s in suggestions]
            

            if True in form.check_anonymous.data:
                review.is_anonymous = True
            else:
                review.is_anonymous = False
            review.is_hidden = False

            review.publication_datetime = dt.datetime.utcnow()

            review.is_anonymous = form.check_anonymous.data

            db.session.commit()
            flash('The review has been added', category='success')
            return redirect(url_for('profile_page', user_id=current_user.id))

    elif request.method == 'GET':
        form.evaluation_novel.data = int(review.evaluation_novel*100)
        form.evaluation_conclusion.data = int(review.evaluation_conclusion*100)
        form.evaluation_error.data = int(review.evaluation_error*100)
        form.evaluation_organize.data = int(review.evaluation_organize*100)
        form.evaluation_accept.data = review.evaluation_accept
        form.confidence.data = int(review.confidence*100)
        form.check_hide.data = review.is_hidden
        form.check_anonymous.data = review.is_anonymous
    
    data = {
        'is_published': review.is_published(),
        # TODO: change 2nd link to anonymized version
        'paper_url':
            url_for('article', id=review.rel_related_paper_version.parent_paper, version=review.rel_related_paper_version.version,
                    anonymous=False)

            if db.session.query(PaperRevision.anonymized_pdf_url) \
            .filter(PaperRevision.id == review.related_paper_version).scalar()

            else
            url_for('article', id=review.rel_related_paper_version.parent_paper, version=review.rel_related_paper_version.version, anonymous=True)
    }

    return render_template(
        'review/review_edit.html',
        form=form,
        data=data,
        previous_reviews=previous_reviews, suggestions=suggestions)


def review_page(review_id):

    if not check_numeric_args(review_id):
        abort(404)

    review = Review.query.filter(Review.id == review_id, get_hidden_filter(Review)).first()

    if not review:
        flash('Review does not exists', category='error')
        return redirect(url_for('home_page'))
    elif review.is_published() is False:
        flash('Review is not publshed', category='warning')
        return redirect(url_for('home_page'))

    creator = review.rel_creator

    data = {
        'paper_url':
            url_for('article',
                    id=review.rel_related_paper_version.parent_paper,
                    version=review.rel_related_paper_version.version),
        'creator_id':  creator.id,
        'creator_first_name': creator.first_name,
        'creator_second_name': creator.second_name
    }

    return render_template('review/review.html', review=review, data=data)
