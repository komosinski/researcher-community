from flask_login import login_required
from open_science import limiter
from flask import request
from open_science.blueprints.action import bp
from sqlalchemy.sql.elements import and_
from open_science import db
from open_science.models import Comment, \
    PaperRevision, RedFlagComment, RedFlagPaperRevision, RedFlagUser, \
    User, VoteComment
from flask_login import current_user
from flask import abort, request
import json


@bp.route('/paper/<id>/flag', methods=['POST'])
@limiter.limit("5 per day")
@login_required
def article_flag(id):
    try:
        paper = PaperRevision.query.get(id)

        flag = RedFlagPaperRevision()
        flag.rel_creator = current_user

        if paper.rel_red_flags_received:
            paper.rel_red_flags_received.append(flag)
        else:
            paper.rel_red_flags_received = [flag]

        db.session.commit()

        print(f"Paper {id} flagged successfuly")

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}

    except Exception as e:
        print(e)
        abort(400)


@bp.route('/comment/<id>/flag', methods=['POST'])
@limiter.limit("5 per day")
@login_required
def comment_flag(id):
    try:
        comment = Comment.query.get(id)

        flag = RedFlagComment()
        flag.rel_creator = current_user

        if comment.rel_red_flags_received:
            comment.rel_red_flags_received.append(flag)
        else:
            comment.rel_red_flags_received = [flag]

        db.session.commit()

        print(f"Comment {id} flagged successfuly")

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}

    except Exception as e:
        print(e)
        abort(400)


@bp.route('/user/<id>/flag', methods=['POST'])
@limiter.limit("5 per day")
@login_required
def user_flag(id):
    try:
        user = User.query.get(id)

        if user == current_user:
            abort(400)

        flag = RedFlagUser()
        flag.rel_creator = current_user

        if user.rel_red_flags_received:
            user.rel_red_flags_received.append(flag)
        else:
            user.rel_red_flags_received = [flag]

        db.session.commit()

        print(f"User {id} flagged successfuly")

        return json.dumps({'success': True}), 201, {'ContentType': 'application/json'}

    except Exception as e:
        print(e)
        abort(400)


@bp.route('/action/like', methods=['POST'])
def addLike():
    likeType = request.json.get('type')
    aid = request.json.get('article_id')
    action = request.json.get('action')

    print(request.json)

    if None in [likeType, aid, action]:
        abort(400)

    comment = db.session.query(Comment).get(aid)

    if comment is None:
        abort(400)

    if likeType == 'comment' and action != 'like_clear' and action != 'dislike_clear':
        like = VoteComment()
        like.rel_to_comment = comment

    if action == 'like_clear':
        delete_unnecessary_comment_vote_record(True, comment)
        new_score = change_comment_vote_score(True, comment)
        db.session.commit()
        return json.dumps({'success': True, 'new_value': new_score}), 201, {'ContentType': 'application/json'}

    elif action == 'dislike_clear':
        delete_unnecessary_comment_vote_record(False, comment)
        new_score = change_comment_vote_score(False, comment)
        db.session.commit()
        return json.dumps({'success': True, 'new_value': new_score}), 201, {'ContentType': 'application/json'}

    elif action == 'up':
        like.is_up = True

    elif action == 'down':
        like.is_up = False
    else:
        abort(400)

    like.rel_creator = current_user
    db.session.commit()
    new_score = db.session.query(Comment).get(aid).votes_score
    return json.dumps({'success': True, 'new_value': new_score}), 201, {'ContentType': 'application/json'}


def delete_unnecessary_comment_vote_record(vote_was_up, comment):
    record_to_delete = db.session.query(VoteComment).filter(
        and_(VoteComment.creator == current_user.id, VoteComment.is_up == vote_was_up,
             VoteComment.to_comment == comment.id)).first()
    db.session.delete(record_to_delete)


def change_comment_vote_score(vote_was_up, comment):
    if vote_was_up is True:
        comment.votes_score -= 1
    if vote_was_up is False:
        comment.votes_score += 1
    return comment.votes_score

@bp.route('/action/verify_liked', methods=['POST'])
def verify_like():
    try:
        user_id = int(request.json.get('userID'))
        comment_id = int(request.json.get('commentID'))

        print(
            f"user_id = {user_id}\ncurrent_user.id = {current_user.id}\ncomment.rel_creator.id = {Comment.query.get(comment_id).rel_creator.id}")

        if Comment.query.get(comment_id).rel_creator == current_user:
            print("fired")
            return json.dumps({'result': True}), 200, {'ContentType': 'application/json'}
    except ValueError:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}

    if VoteComment.query.where(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id,
                                    VoteComment.is_up == True)).first() is not None:
        return json.dumps({'result': True}), 200, {'ContentType': 'application/json'}

    if VoteComment.query.where(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id,
                                    VoteComment.is_up == False)).first() is not None:
        return json.dumps({'result': 'clear'}), 200, {'ContentType': 'application/json'}

    else:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}


@bp.route('/action/verify_disliked', methods=['POST'])
def verify_dislike():
    try:
        user_id = int(request.json.get('userID'))
        comment_id = int(request.json.get('commentID'))

        print(
            f"user_id = {user_id}\ncurrent_user.id = {current_user.id}\ncomment.rel_creator.id = {Comment.query.get(comment_id).rel_creator.id}")

        if Comment.query.get(comment_id).rel_creator == current_user:
            print("fired")
            return json.dumps({'result': True}), 200, {'ContentType': 'application/json'}
    except ValueError:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}

    if VoteComment.query.where(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id,
                                    VoteComment.is_up == False)).first() is not None:
        return json.dumps({'result': True}), 200, {'ContentType': 'application/json'}

    if VoteComment.query.where(and_(VoteComment.creator == user_id, VoteComment.to_comment == comment_id,
                                    VoteComment.is_up == True)).first() is not None:
        return json.dumps({'result': 'clear'}), 200, {'ContentType': 'application/json'}

    else:
        return json.dumps({'result': False}), 200, {'ContentType': 'application/json'}


@bp.route('/action/delete-like', methods=['POST'])
def like_delete():
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
