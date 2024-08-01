from flask import session, render_template, request, redirect, url_for, Markup, flash
import datetime as dt
from open_science.blueprints.forum import bp
from open_science.blueprints.forum.forms import CommentForm
from open_science.models import Thread, Comment
from flask_login import current_user
from open_science import strings as STR
from open_science import db
from open_science.utils import build_comment_tree


@bp.route('/forum')
def forum():
    threads = db.session.query(Thread).all()
    return render_template('forum/forum.html', threads=threads)

@bp.route('/thread/<int:id>/', methods=['GET', 'POST'])
def show_thread(id):


    thread = Thread.query.filter(Thread.id == id).first()
    commentForm = CommentForm(refObject="forum", refObjectID=thread.id)

    user_liked_comments = [vote.rel_to_comment for vote in current_user.rel_comment_votes_created if vote.is_up] if current_user.is_authenticated else []
    user_disliked_comments = [vote.rel_to_comment for vote in current_user.rel_comment_votes_created if not vote.is_up] if current_user.is_authenticated else []

    if commentForm.validate_on_submit():
        try:
            comment = Comment(
                text=Markup.escape(commentForm.content.data),
                votes_score=0,
                red_flags_count=0,
                level=1,
                date=dt.datetime.utcnow(),
                creator_role=current_user.privileges_set
            )

            if commentForm.comment_ref.data and (
            ref_comment := Comment.query.get(commentForm.comment_ref.data)) is not None:
                print(commentForm.comment_ref.data)
                comment.comment_ref = ref_comment.id

            print(current_user.privileges_set)
            print(current_user.rel_privileges_set)

            if current_user.rel_created_comments:
                current_user.rel_created_comments.append(comment)
            else:
                current_user.rel_created_comments = [comment]

            if thread.rel_comments:
                thread.rel_comments.append(comment)
            else:
                thread.rel_comments = [comment]

            db.session.commit()

        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')

        return redirect(url_for("forum.show_thread", id=id))

    comments = build_comment_tree(thread.rel_comments)
    return render_template('forum/forum_thread.html',
                           thread=thread,
                           comments=comments,
                           form=commentForm,
                           user_liked_comments=user_liked_comments,
                           user_disliked_comments=user_disliked_comments)

@bp.route('/add_thread', methods=['POST'])
def add_thread():
    title = request.form['title']
    content = request.form['content']
    new_thread = Thread(title=title, content=content, creator_id=current_user.id)
    db.session.add(new_thread)
    db.session.commit()
    return redirect(url_for('forum.forum'))
