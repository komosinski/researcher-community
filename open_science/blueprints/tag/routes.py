from unittest import result
from open_science.blueprints.tag.forms import EditTagForm
from open_science import db
from open_science.models import Tag, AssociationTagUser, User
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request, abort
from open_science.utils import check_numeric_args, researcher_user_required
import datetime as dt
from flask_login import login_required
from open_science.blueprints.tag import bp
from open_science.blueprints.tag.forms import EditTagMembersForm
import json
from open_science import strings as STR
from flask import Markup

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
        try:
            tag = Tag(
                name=Markup.escape(form.name.data),
                description=Markup.escape(form.description.data),
                deadline=form.deadline.data,
                creator=current_user.id,
                creation_date=dt.datetime.utcnow().date()
            )
            # create association with tag's creator
            association_tag_user = AssociationTagUser(can_appoint=True, can_edit=True)
            association_tag_user.appointer_id = current_user.id
            association_tag_user.rel_user = current_user
            association_tag_user.rel_tag = tag

            db.session.add(tag)
            db.session.commit()
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('user.profile_page', user_id=current_user.id))

        flash('Tag created successfully', category='success')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    return render_template('tag/create_tag.html', form=form)


@bp.route('/edit/<tag_id>', methods=['GET', 'POST'])
@login_required
def edit_tag_page(tag_id):

    if not check_numeric_args(tag_id):
        abort(404)

    tag = Tag.query.filter(Tag.id == tag_id).first_or_404()

    assoc_user_tag = AssociationTagUser.query.filter(AssociationTagUser.tag_id==tag_id, AssociationTagUser.user_id==current_user.id).first_or_404()
    if assoc_user_tag.can_edit == False:
        flash(STR.CANT_EDIT_TAG ,category='error')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    form = EditTagForm()
    form.submit.label.text = 'Save changes'
    form.previous_name.data = tag.name

    if form.validate_on_submit():

        try:
            tag.name = Markup.escape(form.name.data)
            tag.description = Markup.escape(form.description.data)
            db.session.commit()
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('user.profile_page', user_id=current_user.id))

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


@bp.route('/edit/<tag_id>/members', methods=['GET', 'POST'])
@login_required
def edit_tag_members_page(tag_id):

    assoc_user_tag = AssociationTagUser.query.filter(AssociationTagUser.user_id == current_user.id, AssociationTagUser.tag_id==tag_id).first_or_404()
    if assoc_user_tag.can_appoint == False:
        flash(STR.CANT_EDIT_TAG ,category='error')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    form = EditTagMembersForm()
    form.can_appoint = assoc_user_tag.can_appoint
    form.can_edit = assoc_user_tag.can_edit

    tag = Tag.query.filter(Tag.id == tag_id).first()
    
    if not tag:
        flash('Tag does not exist', category='error')
        return redirect(url_for('main.home_page'))

    if form.validate_on_submit():
        try:
            # List of object literals with keys: id(int), can_appoint(boolean), can_edit(boolean)
            members = json.loads(form.members.data)

            if assoc_user_tag.can_appoint:
                associations = tag.assoc_users_with_this_tag
                for assoc in associations:
                    if assoc.user_id!=tag.creator:
                        result = filter(lambda members : members['user_id'] == assoc.user_id, members)
                        member = next(result, False)
                        if member and assoc.appointer_id in [tag.creator, current_user.id]:
                            # Update memeber
                            assoc.can_appoint = member['can_appoint']
                            if assoc_user_tag.can_edit:
                                assoc.can_edit = member['can_edit']
                            members.remove(member)
                        # Only tag's creator can delete members
                        elif tag.creator == current_user.id:
                        # Delete member
                            db.session.delete(assoc)  

            # Add members
            for member in members:
                # Check if association already exists
                if not any(assoc.user_id == member['user_id'] for assoc in associations):

                    user = User.query.filter(User.id == member['user_id']).first()
                    if user:
                        association = AssociationTagUser(can_appoint = member['can_appoint'],
                                                         appointer_id = current_user.id)
                        if assoc_user_tag.can_edit:
                            association.can_edit = member['can_edit']
                        association.rel_user = user
                        association.rel_tag = tag
                        db.session.add(association)

            db.session.commit()
        except Exception as e:
             print(e)
             flash(STR.STH_WENT_WRONG, category='error')
             return redirect(url_for('user.profile_page', user_id=current_user.id))
   
        return redirect(url_for('user.profile_page', user_id=current_user.id))
    else:
        tag_members = [dict(assoc.rel_user.to_dict(), can_appoint=assoc.can_appoint, can_edit=assoc.can_edit, appointer_id=assoc.appointer_id) for assoc in tag.assoc_users_with_this_tag]
        return render_template('tag/edit_members.html', tag=tag, form=form, tag_members=tag_members)

