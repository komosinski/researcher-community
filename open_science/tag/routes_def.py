from open_science.tag.forms import  EditTagForm
from open_science import db
from open_science.models import Tag
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import current_user
from flask import render_template, redirect, url_for, flash, request


def create_tag_page():

    if not current_user.can_create_tag():
        flash('You cannot create a tag', category='error')
        return redirect(url_for('profile_page', user_id=current_user.id))

    form = EditTagForm()
 
    if form.validate_on_submit():

        tag = Tag(
            name = form.name.data,
            description = form.description.data,
            deadline = form.deadline.data,
            creator = current_user.id
        )   
        db.session.add(tag)
        db.session.commit()

        flash('Tag created successfully', category='success')
        return redirect(url_for('profile_page', user_id=current_user.id))
    
    return render_template('tag/create_tag.html',form=form)


def edit_tag_page(tag_id):

    tag = Tag.query.filter(Tag.id == tag_id, Tag.creator == current_user.id).first_or_404()
    
    form = EditTagForm()
    form.submit.label.text = 'Save changes'
    form.previous_name.data = tag.name
    
    if form.validate_on_submit():
     
        tag.name = form.name.data
        tag.description = form.description.data
        db.session.commit()

        flash('Tag edited successfully', category='success')
        return redirect(url_for('profile_page', user_id=current_user.id))
    
    elif request.method == 'GET':
        form.name.data = tag.name
        form.description.data = tag.description
        form.deadline.data = tag.deadline
        

    return render_template('tag/edit_tag.html',form=form, tag_name=tag.name)

def tag_page(tag_id):

    tag = Tag.query.filter(Tag.id == tag_id).first()

    return render_template('tag/tag_page.html',tag=tag)