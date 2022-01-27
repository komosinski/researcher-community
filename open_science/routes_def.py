from sqlalchemy.sql.elements import and_
from werkzeug.utils import secure_filename
from open_science import db, app
from open_science.models import Comment, License, Paper, PaperRevision, Review, RevisionChangesComponent, Tag, User, MessageToStaff, VoteComment
from open_science.forms import AdvancedSearchPaperForm, AdvancedSearchUserForm, AdvancedSearchTagForm, ContactStaffForm, FileUploadForm, CommentForm, PaperRevisionUploadForm
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, abort, request
import datetime as dt
import ast
from open_science.search import helpers as search_helper
import json
import functools
from flask_login.config import EXEMPT_METHODS
from open_science.review.helpers import prepare_review_requests,\
     NOT_ENOUGHT_RESEARCHERS_TEXT, transfer_old_reviews
from open_science.db_helper import get_hidden_filter
from open_science.notification.helpers import create_paper_comment_notifications
from text_processing.prepocess_text import get_text
import text_processing.similarity_matrix as sm

# Routes decorator
def researcher_user_required(func):
    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('login_page'))
        elif current_user.privileges_set < User.user_types_enum.RESEARCHER_USER.value:
            flash('You must be a scientist user to access this page',
                  category='warning')
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


def auto_page(name):

    if not name:
        return redirect(url_for('home_page'))

    else:
        try:
            template = render_template(f'pages/{name}.html')
            return template
        except Exception:
            return redirect(url_for('home_page'))


def home_page():
    users_plot_url = app.config['USERS_PLOT_URL']

    return render_template("home_page.html",
                           users_plot_url=users_plot_url)


def file_upload_page():
    licenses = [(license.id, license.license) for license in db.session.query(License).all()]
    tags = [tag.to_dict() for tag in db.session.query(Tag).all()]
    form = FileUploadForm()
    form.license.choices = licenses

    if form.validate_on_submit():
        print(form.data)
        f = form.file.data
        af = form.anonymousFile.data

        if not validatePDF(f.read(16)):
            abort(415)

        f.seek(0, 0)
        title = form.title.data
        description = form.description.data
        coauthors = json.loads(form.coauthors.data)
        tags = json.loads(form.tags.data)
        tags = [Tag.query.get(t['id']) for t in tags]


        users = []
        for author in coauthors:
            user = db.session.query(User).filter(
                User.email == author['authorEmail']).first()
            if not bool(user):  # not exists
                newUser = User(
                    author['authorName'], author['authorLastName'], author['authorEmail'], "somepassword")
                users.append(newUser)
                db.session.add(newUser)
            else:
                users.append(user)

        print(users)

        paper_version = PaperRevision(
            pdf_url="",
            title=title,
            abstract=description,
            publication_date=dt.datetime.utcnow(),
            rel_creators=[current_user] + users,
            rel_related_tags=tags,
            preprocessed_text = ""
        )

        db.session.flush()

        id = paper_version.id

        filename = f"paper_{id}.pdf"
        path = f"open_science/static/articles/{filename}"
        url = url_for('static', filename=f"articles/{filename}")

        f.save(path)

        if af is not None and validatePDF(af.read(16)):
            af.seek(0,0)

            anonymous_filename = f"anonymous_paper_{id}.pdf"
            anon_path = f"open_science/static/articles/{anonymous_filename}"
            anon_url = url_for('static', filename=f"articles/{anonymous_filename}")

            af.save(anon_path)

            paper_version.anonymized_pdf_url = anon_url

        paper_version.pdf_url = url
        paper_version.preprocessed_text = get_text(path)

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
        
        paper.rel_related_versions.append(paper_version)

        db.session.add(paper)
        db.session.commit()
  
        # update matrixes
        sm.update_dictionary()
        sm.update_tfidf_matrix()
        sm.update_similarity_matrix()

        # bin   d old unpublished reviews and unanswered review reqests
        # to nthe ewest paper's revision
        transfer_old_reviews(paper)
        enough_reviews = prepare_review_requests(paper_version)
        if enough_reviews is False:
            flash(NOT_ENOUGHT_RESEARCHERS_TEXT, category='warning')

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}

    return render_template("utils/pdf_send_form.html", form=form, tags=tags)


def upload_revision(id):
    parent_paper = Paper.query.get(id)
    previous_version = parent_paper.get_latest_revision()

    if current_user not in previous_version.rel_creators:
        abort(401)
    
    form = PaperRevisionUploadForm()

    if parent_paper is None:
        abort(404)

    if form.validate_on_submit():
        print(form.data)
        f = form.file.data
        af = form.anonymousFile.data

        if not validatePDF(f.read(16)):
            abort(415)

        f.seek(0, 0)
        title = previous_version.title
        description = previous_version.abstract
        authors = previous_version.rel_creators
        tags = previous_version.rel_related_tags

        # TODO: add changes
        new_version = PaperRevision(
            pdf_url="",
            title=title,
            abstract=description,
            publication_date=dt.datetime.utcnow(),
            rel_creators=authors,
            rel_related_tags=tags,
            preprocessed_text = "",
            version = int(previous_version.version) + 1
        )

        db.session.flush()

        vid = new_version.id

        filename = f"paper_{vid}.pdf"
        path = f"open_science/static/articles/{filename}"
        url = url_for('static', filename=f"articles/{filename}")

        f.save(path)

        if af is not None and validatePDF(af.read(16)):
            af.seek(0,0)

            anonymous_filename = f"anonymous_paper_{id}.pdf"
            anon_path = f"open_science/static/articles/{anonymous_filename}"
            anon_url = url_for('static', filename=f"articles/{anonymous_filename}")

            af.save(anon_path)

            new_version.anonymized_pdf_url = anon_url

        new_version.pdf_url = url
        new_version.preprocessed_text = get_text(path)

        changes = [RevisionChangesComponent(
            change_description = change['suggestion'],
            location = change['location']
        ) for change in json.loads(form.changes.data)]

        new_version.rel_changes = changes

        if parent_paper.rel_related_versions:
            parent_paper.rel_related_versions.append(new_version)
        else:
            # should never fire, but miracles do sometimes happen, soo...
            parent_paper.rel_related_versions = [new_version]
        
        db.session.commit()

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}

    return render_template("utils/revisionUploadForm.html", form=form, paperID=parent_paper.id)


def view_article(id):

    if not check_numeric_args(id):
        abort(404)

    version = request.args.get('version')
    print(version)
    # commentForm = CommentForm(refObject="paper")

    article = Paper.query.get(id)
    if not article:
        abort(404)
    if version is None:
        pv = article.get_latest_revision()
    else:
        pv = PaperRevision.query.filter(and_(PaperRevision.parent_paper == id, PaperRevision.version == version)).first_or_404()
    commentForm = CommentForm(refObject="paper", refObjectID = pv.id)

    # current_user.is_authenticated()
    user_liked_comments = [vote.rel_to_comment for vote in current_user.rel_comment_votes_created if vote.is_up] if current_user.is_authenticated else []
    user_disliked_comments = [vote.rel_to_comment for vote in current_user.rel_comment_votes_created if not vote.is_up] if current_user.is_authenticated else []

    if commentForm.validate_on_submit():
        comment = Comment(
            text=commentForm.content.data,
            votes_score = 0,
            red_flags_count = 0,
            level = 1,
            date = dt.datetime.utcnow(),
            creator_role = current_user.privileges_set
        )

        if commentForm.comment_ref.data and (ref_comment := Comment.query.get(commentForm.comment_ref.data[1:])) is not None:
            print(commentForm.comment_ref.data)
            comment.comment_ref = ref_comment.id

        print(current_user.privileges_set)
        print(current_user.rel_privileges_set)

        if current_user.rel_created_comments:
            current_user.rel_created_comments.append(comment)
        else: current_user.rel_created_comments = [comment]

        if pv.rel_related_comments:
            pv.rel_related_comments.append(comment)
        else:
            pv.rel_related_comments = [comment]

        db.session.commit()
        create_paper_comment_notifications(pv, comment, current_user.id)

        return redirect(url_for("article", id=id, version=pv.version))

    # similar papers
    similar_papaers = pv.get_similar_revisions()
 
    return render_template("article/view.html",
                           article=pv, similar=similar_papaers[:3],
                           form=commentForm,
                           user_liked_comments=user_liked_comments,
                           user_disliked_comments=user_disliked_comments)


def anonymous_article_page(id):

    if not check_numeric_args(id):
        abort(404)

    version = request.args.get('version')

    article = Paper.query.get(id)
    if not article:
        abort(404)
    if version is None:
        return redirect(url_for('article', id=id))
    else:
        pv = PaperRevision.query.filter(and_(PaperRevision.parent_paper == id,
                                             PaperRevision.version == version,
                                             PaperRevision.anonymized_pdf_url!=None)).first()
    if not pv:
        return redirect(url_for("article", id=id, version=version))

    return render_template("article/anonymous_view.html", article=pv)



def like():
    # print(request.json)
    # print(request.content)
    # print(request.data)
    likeType = request.json.get('type')
    aid = request.json.get('article_id')
    action = request.json.get('action')
    
    print(request.json)

    if None in [likeType, aid, action]:
        abort(400)

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
        # removing all dislikes by this user
        VoteComment.query.filter(and_(VoteComment.creator == current_user.id, VoteComment.is_up == False)).delete()
    elif action == 'down':
        like.is_up = False
        # removing all likes by this user
        VoteComment.query.filter(and_(VoteComment.creator == current_user.id, VoteComment.is_up == True)).delete()
    else:
        abort(400)

    like.rel_creator = current_user

    db.session.commit()

    new_score = comment = db.session.query(Comment).get(aid).votes_score

    return json.dumps({'success': True, 'new_value': new_score}), 201, {'ContentType': 'application/json'}


def verify_user_liked():
    try:
        user_id = int(request.json.get('userID'))
        comment_id = int(request.json.get('commentID'))
    except ValueError:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}

    if VoteComment.query.where(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id, VoteComment.is_up == True)).first() is not None:
        return json.dumps({'result': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}

def verify_user_disliked():
    try:
        user_id = int(request.json.get('userID'))
        comment_id = int(request.json.get('commentID'))
    except ValueError:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}

    if VoteComment.query.where(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id, VoteComment.is_up == False)).first() is not None:
        return json.dumps({'result': True}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}

def delete_like():
    try:
        user_id = int(request.json.get('userID'))
        comment_id = int(request.json.get('commentID'))
    except ValueError:
        abort(400)

    try:
        VoteComment.query.filter(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id)).delete()
        db.session.commit()
    except Exception:
        # probably should be something else here
        abort(400)

    return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}


def search_papers_page():
    search_text = request.args.get('search_text')
    search_like = "%{}%".format(search_text)
    search_option = request.args.get('search_option', 'title')
    rows_per_page = request.args.get('rows_per_page', 5, type=int)
    page_num = request.args.get('page', 1, type=int)
    order_by = request.args.get('order_by')

    order = search_helper.get_paper_order(order_by)
    paper_revisions = search_helper.get_papers_basic_search(
        search_like, search_option, order, page_num, rows_per_page)

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

    if not check_numeric_args(page):
        abort(404)

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

    if not check_numeric_args(page):
        abort(404)

    page = int(page)

    users = []
    order = search_helper.get_user_order(order_by)
    users = search_helper.get_users_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_user.html', page=page, users=users, search_data=search_data,
                           order_by=order_by)


def advanced_search_tags_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if not check_numeric_args(page):
        abort(404)

    page = int(page)

    tags = []
    order = search_helper.get_tag_order(order_by)
    tags = search_helper.get_tags_advanced_search(page, search_data, order)

    return render_template('search/advanced_search_tag.html', page=page, tags=tags, search_data=search_data,
                           order_by=order_by)


def reviews_list_page(page, search_data, order_by):
    if isinstance(search_data, str):
        search_data = ast.literal_eval(search_data)

    if not check_numeric_args(page):
        abort(404)

    page = int(page)
    user_id = int(search_data['user_id'])
    reviews = []
    order = Review.publication_datetime.desc()
    reviews = Review.query.filter(Review.creator == user_id,
                                  get_hidden_filter(Review),
                                  Review.is_anonymous == False,
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

import open_science.schedule.schedule as sch
def test_text_preprocessing():
    sch.daily_jobs()
    return 'test'


def about_page():
    return render_template('about.html')


def privacy_page():
    return render_template('privacy.html')


def forum_page():
    return render_template('forum.html')

