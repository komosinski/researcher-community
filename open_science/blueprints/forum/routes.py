from flask import session, render_template, request, redirect, url_for, Markup, flash
import datetime as dt
from open_science.blueprints.forum import bp
from open_science.blueprints.forum.forms import CommentForm
from open_science.models import ForumTopic, Comment, User
from flask_login import current_user
from open_science import strings as STR
from open_science import db
from open_science.utils import build_comment_tree, time_ago


@bp.route('/forum')
def forum():
    forum_topics = db.session.query(ForumTopic).all()
    return render_template('forum/forum.html', forum_topics=forum_topics, current_user=current_user)

@bp.route('/forum_topic/<int:id>/', methods=['GET', 'POST'])
def show_forum_topic(id):
    forum_topic = ForumTopic.query.filter(ForumTopic.id == id).first()
    commentForm = CommentForm(refObject="forum", refObjectID=forum_topic.id)
    creator = User.query.get(forum_topic.creator_id)

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
            # [1:] perform action of cutting prefix c from id of comment taken from user interface
            ref_comment := Comment.query.get(commentForm.comment_ref.data[1:])) is not None:
                print(commentForm.comment_ref.data)
                comment.comment_ref = ref_comment.id

            print(current_user.privileges_set)
            print(current_user.rel_privileges_set)

            if current_user.rel_created_comments:
                current_user.rel_created_comments.append(comment)
            else:
                current_user.rel_created_comments = [comment]

            if forum_topic.rel_comments:
                forum_topic.rel_comments.append(comment)
            else:
                forum_topic.rel_comments = [comment]

            db.session.commit()

        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')

        return redirect(url_for("forum.show_forum_topic", id=id))

    comments = build_comment_tree(forum_topic.rel_comments)
    return render_template('forum/forum_thread.html',
                           forum_topic=forum_topic,
                           comments=comments,
                           form=commentForm,
                           user_liked_comments=user_liked_comments,
                           user_disliked_comments=user_disliked_comments,
                           time_ago=time_ago,
                           creator=creator)

@bp.route('/add_forum_topic', methods=['POST'])
def add_forum_topic():
    title = request.form['title']
    content = request.form['content']
    forum_topic = ForumTopic(title=title, content=content, creator_id=current_user.id, date_created=dt.datetime.now())
    db.session.add(forum_topic)
    db.session.commit()
    return redirect(url_for('forum.forum'))
