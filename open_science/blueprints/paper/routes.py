from flask import current_app as app, jsonify
from flask_login import login_required
from flask import render_template
from flask import request, Markup
import os
from sqlalchemy.sql.elements import and_
from config.config import Config
from open_science import db
from open_science.models import CalibrationPaper, Comment, License, \
    Paper, PaperRevision, RevisionChangesComponent, Tag, \
    User, Suggestion
from open_science.blueprints.paper.forms import  \
    FileUploadForm, CommentForm, PaperRevisionUploadForm
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, abort, request
import datetime as dt
import json
from open_science.blueprints.review.helpers import prepare_review_requests,\
      transfer_old_reviews
from open_science.blueprints.notification.helpers import create_paper_comment_notifications
from text_processing.prepocess_text import get_text
import text_processing.similarity_matrix as sm
from open_science import strings as STR
from open_science.utils import check_numeric_args, researcher_user_required, build_comment_tree
from open_science.blueprints.paper import bp


def validatePDF(content):
    return content.decode("ascii", "ignore").startswith("%PDF-")


@bp.route('/paper/<id>/', methods=['GET', 'POST'])
def article(id):

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
        try:
            comment = Comment(
                text=Markup.escape(commentForm.content.data),
                votes_score = 0,
                red_flags_count = 0,
                level = 1,
                date = dt.datetime.utcnow(),
                creator_role = current_user.privileges_set
            )

            if commentForm.comment_ref.data and (ref_comment := Comment.query.get(commentForm.comment_ref.data[1:])) is not None:  # [1:] removes the 'c' prefix from the comment id received from user interface
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
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')

        return redirect(url_for("paper.article", id=id, version=pv.version))

    # similar papers  
    try:
        similar_papers = pv.get_similar_revisions()
        similar_papers = list(filter(lambda p: type(p) != CalibrationPaper and p.parent_paper != pv.parent_paper, similar_papers))
    except Exception as ex:
        similar_papers = []
        print(ex)

    comments = build_comment_tree(pv.rel_related_comments)
    return render_template("article/view.html",
                           article=pv, similar=similar_papers[:3],
                           form=commentForm,
                           user_liked_comments=user_liked_comments,
                           user_disliked_comments=user_disliked_comments,
                           comments=comments)


@bp.route('/paper/anon/<id>')
def anonymous_article_page(id):
    if not check_numeric_args(id):
        abort(404)

    version = request.args.get('version')

    article = Paper.query.get(id)
    if not article:
        abort(404)
    if version is None:
        return redirect(url_for('paper.article', id=id))
    else:
        pv = PaperRevision.query.filter(and_(PaperRevision.parent_paper == id,
                                             PaperRevision.version == version,
                                             PaperRevision.anonymized_pdf_url!=None)).first()
    if not pv:
        return redirect(url_for("paper.article", id=id, version=version))

    return render_template("article/anonymous_view.html", article=pv)


@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
@researcher_user_required
def upload_file_page():
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

        if form.review_declaration.data is True:
            chosen_confidence_level = form.confidence_level.data
        else:
            chosen_confidence_level = 0

        paper_version = PaperRevision(
            pdf_url="",
            title=title,
            abstract=description,
            publication_date=dt.datetime.utcnow(),
            rel_creators=[current_user] + users,
            rel_related_tags=tags,
            preprocessed_text="",
            confidence_level=chosen_confidence_level,
            conflicts_of_interest=form.conflicts_of_interest.data
        )
        db.session.flush()

        id = paper_version.id

        filename = f"paper_{id}.pdf"
        path = os.path.join(Config.ROOTDIR, app.config['PDFS_DIR_PATH'], filename)
        url = url_for('static', filename=f"articles/{filename}")

        f.save(path)

        if af is not None and validatePDF(af.read(16)):
            af.seek(0, 0)

            anonymous_filename = f"anonymous_paper_{id}.pdf"
            anon_path = os.path.join(Config.ROOTDIR, app.config['PDFS_DIR_PATH'], anonymous_filename)
            anon_url = url_for('static', filename=f"articles/{anonymous_filename}")

            af.save(anon_path)

            paper_version.anonymized_pdf_url = anon_url

        paper_version.pdf_url = url
        try:
            paper_version.preprocessed_text = get_text(path)
        except Exception as ex:
            print(ex)
            flash(STR.PAPER_WORD_COUNT_ERROR, category='error')
            return redirect(url_for('main.home_page'))

        paper = Paper()
        
        paper.rel_related_versions.append(paper_version)

        db.session.add(paper)
        db.session.commit()
  
        if app.config['TEXT_PROCESSING_UPDATE_FILES_ON_UPLOAD'] is True:
            # update matrixes
            sm.update_dictionary(paper_version.preprocessed_text)
            sm.update_tfidf_matrix()
            sm.update_similarity_matrix(paper_version.preprocessed_text)
    
        return redirect(url_for('paper.article', id=paper.id))

    return render_template("utils/pdf_send_form.html", form=form, tags=tags)


@bp.route('/article/<id>/add_revision', methods=['GET', 'POST'])
@login_required
@researcher_user_required
def upload_new_revision(id):
    parent_paper = Paper.query.get(id)
    previous_version = parent_paper.get_latest_revision()

    if current_user not in previous_version.rel_creators:
        abort(401)
    
    # to prepare fields to answer review suggestions:
    reviews = previous_version.get_published_reviews_list()
    suggestions = []
    for review in reviews:
        for suggestion in review.rel_suggestions:
            suggestions.append(suggestion)

    form = PaperRevisionUploadForm(suggestion_answers=[{} for i in range(len(suggestions))])

    if parent_paper is None:
        abort(404)

    # to prepare fields to answer review suggestions:
    for i, suggestion in enumerate(suggestions):
        form.suggestion_answers[i].answer.description = suggestion.suggestion
        form.suggestion_answers[i].suggestion_id.data = suggestion.id


    if form.validate_on_submit():
        try:
            f = form.file.data
            af = form.anonymousFile.data

            if not validatePDF(f.read(16)):
                abort(415)

            f.seek(0, 0)
            title = previous_version.title
            description = previous_version.abstract
            authors = previous_version.rel_creators
            tags = previous_version.rel_related_tags

            
            if form.review_declaration.data is True:
                chosen_confidence_level = form.confidence_level.data
            else:
                chosen_confidence_level = 0


            new_version = PaperRevision(
                pdf_url="",
                title=title,
                abstract=description,
                publication_date=dt.datetime.utcnow(),
                rel_creators=authors,
                rel_related_tags=tags,
                preprocessed_text="",
                version=int(previous_version.version) + 1,
                confidence_level=chosen_confidence_level
            )

            db.session.flush()

            vid = new_version.id

            filename = f"paper_{vid}.pdf"
            path = os.path.join(Config.ROOTDIR, app.config['PDFS_DIR_PATH'], filename)
            url = url_for('static', filename=f"articles/{filename}")

            f.save(path)

            if af is not None and validatePDF(af.read(16)):
                af.seek(0, 0)

                anonymous_filename = f"anonymous_paper_{id}.pdf"
                anon_path = os.path.join(Config.ROOTDIR, app.config['PDFS_DIR_PATH'], anonymous_filename)
                anon_url = url_for('static', filename=f"articles/{anonymous_filename}")

                af.save(anon_path)

                new_version.anonymized_pdf_url = anon_url

            new_version.pdf_url = url
            try:
                new_version.preprocessed_text = get_text(path)
            except Exception as ex:
                print(ex)
                flash(STR.PAPER_WORD_COUNT_ERROR, category='error')
                return redirect(url_for('main.home_page'))

            changes = [RevisionChangesComponent(
                change_description=change['suggestion'],
                location=change['location']
            ) for change in json.loads(form.changes.data)]

            # add answers to review suggestions
            for i, suggestion in enumerate(suggestions):
                if form.suggestion_answers[i].answer.data:
                    review_answer = RevisionChangesComponent(
                        change_description=form.suggestion_answers[i].answer.data,
                        rel_review_suggestion=suggestion
                    )
                    changes.append(review_answer)

            new_version.rel_changes = changes

            if parent_paper.rel_related_versions:
                parent_paper.rel_related_versions.append(new_version)
            else:
                # should never fire, but miracles do sometimes happen, soo...
                parent_paper.rel_related_versions = [new_version]
            
            db.session.commit()

            # bind old unpublished reviews and unanswered review reqests
            # to the newest paper's revision
            transfer_old_reviews(parent_paper)

        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('main.home_page'))

        # return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}
        return redirect(url_for('paper.article', id=new_version.parent_paper))

    return render_template("utils/revisionUploadForm.html", form=form, paperID=parent_paper.id)


@bp.route('/paper/<id>/changes/<version>')
def revision_changes_page(id, version):
    if check_numeric_args(id, version) is False:
        abort(404)

    paper_revision = PaperRevision.query\
        .filter(PaperRevision.parent_paper == int(id),
                PaperRevision.version == int(version)).first()

    previous_revision = PaperRevision.query\
        .filter(PaperRevision.parent_paper == int(id),
                PaperRevision.version == int(version)-1).first()

    if not paper_revision or not previous_revision:
        abort(404)
    
    return render_template('article/revision_changes.html',
                           paper_revision=paper_revision,
                           previous_revision=previous_revision)


@bp.route('/review/edit/add-suggestion', methods=['POST'])
@login_required
@researcher_user_required
def add_suggestion():
    data = request.get_json()
    new_suggestion = Suggestion(
        suggestion=data['suggestion'],
        location=data['location'],
        review=data.get('review')
    )
    db.session.add(new_suggestion)
    db.session.commit()
    return jsonify({
        'message': 'Suggestion added successfully',
        'id': new_suggestion.id
    }), 201

@bp.route('/review/get-suggestions/<int:review_id>', methods=['GET'])
def get_suggestions(review_id):
    suggestions = Suggestion.query.filter_by(review=review_id).all()
    results = [
        {
            'id': suggestion.id,
            'suggestion': suggestion.suggestion,
            'location': suggestion.location,
            'review': suggestion.review
        } for suggestion in suggestions
    ]

    return jsonify(results)

@bp.route('/review/delete-suggestion/<int:id>', methods=['DELETE'])
@login_required
@researcher_user_required
def delete_suggestion(id):
    suggestion = Suggestion.query.get(id)
    if not suggestion:
        return jsonify({'message': 'Suggestion not found'}), 404

    db.session.delete(suggestion)
    db.session.commit()
    return jsonify({'message': 'Suggestion deleted successfully'}), 200

