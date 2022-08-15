from open_science.blueprints.tag.forms import EditTagForm
from open_science import db
from open_science.models import Tag
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request, abort
from open_science.utils import check_numeric_args, researcher_user_required
import datetime as dt
from flask_login import login_required
from open_science.blueprints.tag import bp


def check_numeric_args(*argv):
    try:
        for arg in argv:
            arg = int(arg)
    except:
        return False
    return True
    

@bp.route('/create', methods=['GET', 'POST'])
@bp.route('/tag/create', methods=['GET', 'POST'])
@login_required
def create_tag_page():

    if current_user.can_create_tag() is False:
        flash('You cannot create a tag', category='error')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    form = EditTagForm()

    if form.validate_on_submit():

        tag = Tag(
            name=form.name.data,
            description=form.description.data,
            deadline=form.deadline.data,
            creator=current_user.id,
            creation_date=dt.datetime.utcnow().date(),
            can_share = True,
            can_edit = True
        )
        db.session.add(tag)
        db.session.commit()

        flash('Tag created successfully', category='success')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    return render_template('tag/create_tag.html', form=form)


@bp.route('/edit/<tag_id>', methods=['GET', 'POST'])
@login_required
def edit_tag_page(tag_id):

    if not check_numeric_args(tag_id):
        abort(404)

    tag = Tag.query.filter(Tag.id == tag_id, Tag.creator ==
                           current_user.id).first_or_404()

    form = EditTagForm()
    form.submit.label.text = 'Save changes'
    form.previous_name.data = tag.name

    if form.validate_on_submit():

        tag.name = form.name.data
        tag.description = form.description.data
        db.session.commit()

        flash('Tag edited successfully', category='success')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    elif request.method == 'GET':
        form.name.data = tag.name
        form.description.data = tag.description
        form.deadline.data = tag.deadline

    return render_template('tag/edit_tag.html', form=form, tag_name=tag.name)

@bp.route('/<tag_name>')
def tag_page(tag_name):

    tag = Tag.query.filter(Tag.name == tag_name).first()
    if not tag:
        flash('Tag with that name does not exist', category='error')
        return redirect(
            url_for('search.advanced_search_tags_page',
                    page=1,
                    search_data={'name': ''},
                    order_by='newest'))

    return render_template('tag/tag_page.html', tag=tag)


@bp.route('/edit/<tag_id>/members')
@login_required
def edit_tag_members_page(tag_id):
    tag = Tag.query.filter(Tag.id == tag_id).first()
    if not tag:
        flash('Tag does not exist', category='error')
        return redirect(url_for('main.home_page'))
    for x in tag.rel_users_with_this_tag:
        print(x)

    return render_template('tag/edit_members.html', tag=tag)




