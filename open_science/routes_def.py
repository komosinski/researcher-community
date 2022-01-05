import re
from flask_wtf.form import FlaskForm
from sqlalchemy.sql.functions import user
from werkzeug.utils import secure_filename
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
from open_science import db
from open_science.models import Comment, Paper, PaperRevision, Review, User, MessageToStaff, VoteComment
from open_science.forms import AdvancedSearchPaperForm, AdvancedSearchUserForm, AdvancedSearchTagForm, ContactStaffForm
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, redirect, url_for, flash, abort, request
import datetime as dt
import ast
from open_science.search import helpers as search_helper
import json
import functools
from flask_login.config import EXEMPT_METHODS


# Routes decorator
def scientific_user_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('login_page'))
        elif current_user.privileges_set < User.user_types_enum.SCIENTIST_USER.value:
            flash('You must be a scientist user to access this page', category='warning')
            return redirect(url_for('home_page'))
        return func(*args, **kwargs)

    return decorated_view


def check_numeric_args(*argv):
    try:
        for arg in argv:
            arg = int(arg)
    except:
        return False
    return True


def validatePDF(content):
    return content.decode("ascii", "ignore").startswith("%PDF-")


class FileUploadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    file = FileField("File", validators=[FileRequired(), FileAllowed(['pdf'])])
    description = StringField("Abstract", validators=[DataRequired()])
    license = SelectField("License", choices=[('1', "beerware")])
    coauthors = StringField(id="coauthors-input-field")
    submitbtn = SubmitField("Upload")


def home_page():
    return render_template("home_page.html")


def fileUploadPage():
    form = FileUploadForm()

    if form.validate_on_submit():
        print(form.data)
        f = form.file.data

        if not validatePDF(f.read(16)): abort(415)

        f.seek(0, 0)
        title = form.title.data
        description = form.description.data
        coauthors = json.loads(form.coauthors.data)

        users = []
        for author in coauthors:
            user = db.session.query(User).filter(User.email == author['authorEmail']).first()
            if not bool(user):  # not exists
                newUser = User(author['authorName'], author['authorLastName'], author['authorEmail'], "somepassword")
                users.append(newUser)
                db.session.add(newUser)
            else:
                users.append(user)

        print(users)
        filename = secure_filename(f.filename)
        path = f"open_science/static/articles/{filename}"
        url = url_for('static', filename=f"articles/{filename}")

        f.save(path)

        # paper = Paper(
        #     url=url,
        #     title=title,
        #     text="Lorem ipsum tralala",
        #     description=description,
        #     publication_date=dt.datetime.utcnow(),
        #     license="CC-BY-ND 4.0",
        #     rel_creators = [current_user] + users
        # )
        paper = Paper()
        paper_version = PaperRevision(
            pdf_url=url,
            title=title,
            abstract=description,
            publication_date=dt.datetime.utcnow(),
            rel_creators=[current_user] + users
        )
        paper.rel_related_versions.append(paper_version)

        db.session.add(paper)
        db.session.commit()
        # paper.send_review_requests()

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}

    return render_template("utils/pdf_send_form.html", form=form)


# anonym -
def view_article(id):
    # string:   True / False
    anonymous = request.args.get('anonymous')

    article = Paper.query.get(id)
    if not article: abort(404)
    pv = article.get_latest_revision()
    if pv.rel_related_reviews:
        review_scores = [review.review_score for review in pv.rel_related_reviews]
        reviewMean = sum(review_scores) / len(review_scores)
        # review_scores = [review.votes_score*review.weight for review in pv.rel_related_reviews]
        # review_weight_sum = sum([review.weight for review in pv.rel_related_reviews])
        # reviewMean = sum(review_scores)/review_weight_sum
    else:
        reviewMean = 0
    return render_template("article/view.html", article=pv, similar=[pv, pv, pv], score=reviewMean)


def like():
    likeType = request.json.get('type')
    aid = request.json.get('article-id')
    action = request.json.get('action')

    if None in [likeType, aid, action]: abort(400)

    if likeType == 'comment':
        like = VoteComment()

        comment = db.session.query(Comment).get(aid)

        if comment is None:
            abort(400)
        else:
            like.rel_to_comment = comment

    else:
        abort(400)

    if action == 'up':
        like.is_up = True
    elif action == 'down':
        like.is_up = False
    else:
        abort(400)

    like.rel_creator = current_user

    db.session.commit()

    return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}


def search_papers_page():
    search_text = request.args.get('search_text')
    search_like = "%{}%".format(search_text)
    search_option = request.args.get('search_option', 'title')
    rows_per_page = request.args.get('rows_per_page', 5, type=int)
    page_num = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by')

    order = search_helper.get_paper_order(order_by)
    paper_revisions = search_helper.get_papers_basic_search(search_like, search_option, order, page_num, rows_per_page)

    if not paper_revisions:
        flash('No results found!', category='warning')
        return redirect(url_for('home_page'))

    return render_template("search/search_paper_result_list.html", papers=paper_revisions)


def advanced_search_page():
    paper_form = AdvancedSearchPaperForm(request.args)
    user_form = AdvancedSearchUserForm(request.args)
    tag_form = AdvancedSearchTagForm(request.args)

    # TODO Add error validation messages
    if paper_form.submit_paper.data and paper_form.validate():
        search_data = paper_form.data
        return redirect(url_for('advanced_search_papers_page', page=1, search_data=search_data, order_by='newest'))
    elif user_form.submit_user.data and user_form.validate():
        search_data = user_form.data
        return redirect(url_for('advanced_search_users_page', page=1, search_data=search_data, order_by='score'))
    elif tag_form.submit_tag.data and tag_form.validate():
        search_data = tag_form.data
        return redirect(url_for('advanced_search_tags_page', page=1, search_data=search_data, order_by='newest'))

    return render_template('/search/advanced_search.html', paper_form=paper_form, user_form=user_form,
                           tag_form=tag_form)


def advanced_search_papers_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if isinstance(page, str):
        page = int(page)

    papers = []
    order = search_helper.get_paper_order(order_by)
    papers = search_helper.get_papers_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_paper.html', page=page, papers=papers, search_data=search_data,
                           order_by=order_by)


def advanced_search_users_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    page = int(page)

    users = []
    order = search_helper.get_user_order(order_by)
    users = search_helper.get_users_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_user.html', page=page, users=users, search_data=search_data,
                           order_by=order_by)


def advanced_search_tags_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    page = int(page)

    tags = []
    order = search_helper.get_tag_order(order_by)
    tags = search_helper.get_tags_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_tag.html', page=page, tags=tags, search_data=search_data,
                           order_by=order_by)


def reviews_list_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    page = int(page)
    user_id = int(search_data['user_id'])
    reviews = []
    order = Review.publication_datetime.desc()
    reviews = Review.query.filter(Review.creator == user_id,
                                  Review.is_hidden == False, Review.is_anonymous == False,
                                  Review.publication_datetime != None).order_by(order).paginate(page=page, per_page=30)

    if reviews.pages == 0:
        return redirect(url_for('profile_page', user_id=user_id))

    return render_template('search/review_result_list.html', page=page, reviews=reviews, search_data=search_data,
                           order_by=order_by)


def faq_page():
    # TODO: implement search etc
    return render_template('help/faq.html')


def help_page():
    # TODO: implement search etc
    return render_template('help/help.html')


def contact_staff_page():
    form = ContactStaffForm()

    if form.validate_on_submit():
        mssg = MessageToStaff(sender=current_user.id, topic=form.topic.data, text=form.text.data,
                              date=dt.datetime.utcnow())
        db.session.add(mssg)
        db.session.commit()
        flash(f'Message has been send', category='success')
        return redirect(url_for('help_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('help/contact_staff.html', form=form)
