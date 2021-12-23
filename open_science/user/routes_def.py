from open_science.user.forms import RegisterForm, LoginForm, ResendConfirmationForm, AccountRecoveryForm, SetNewPasswordForm
from open_science.user.forms import InviteUserForm, EditProfileForm, ReviewRequestForm
from open_science import db
from open_science.tokens import confirm_password_token, confirm_account_recovery_token, confirm_email_change_token
from open_science.models import Notification, Paper, PrivilegeSet, User, ReviewRequest, Review
import open_science.email as em
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, flash, request
import datetime as dt
from werkzeug.utils import secure_filename
import os
from PIL import Image
from open_science import app


def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        ps_standard_user = PrivilegeSet.query.filter(PrivilegeSet.name=='standard_user').first()

        user_to_create = User(first_name=form.first_name.data,
                              second_name=form.second_name.data,
                              email=form.email.data,
                              plain_text_password=form.password.data,
                              affiliation = form.affiliation.data,
                              orcid = form.orcid.data.upper().replace("-",""),
                              google_scholar = form.google_scholar.data,
                              about_me = form.about_me.data,
                              personal_website = form.personal_website.data,
                              review_mails_limit = form.review_mails_limit.data,
                              notifications_frequency= form.notifications_frequency.data,
                              registered_on = dt.datetime.utcnow())
        user_to_create.rel_privileges_set  = ps_standard_user
        db.session.add(user_to_create)
        db.session.flush()

        f = form.profile_image.data
        if f:
            filename = secure_filename(f'{user_to_create.id}.png')
            path = f"open_science/{app.config['PROFILE_IMAGE_URL']}{filename}"
            img = Image.open(f)
            img = img.resize((256, 256))
            img.save(path, "PNG")
            user_to_create.has_photo =True

        db.session.commit()
        em.send_email_confirmation(user_to_create.email)
        flash(f"'A confirmation email has been sent.", category='success')
        return redirect(url_for('unconfirmed_email_page'))
   
    return render_template('user/register.html', form=form)

def login_page():
    if current_user.is_authenticated: 
        flash('You are already logged in.', category='warning')
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ) and attempted_user.confirmed:
            login_user(attempted_user)
            attempted_user.last_seen = dt.datetime.utcnow()
            db.session.commit()
            flash('Success! You are logged in', category='success')
            return redirect(url_for('home_page'))
        elif not attempted_user:
            flash('Email and password are not match! Please try again', category='error')
        elif not attempted_user.confirmed:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed_email_page'))
        else:
            flash('Email and password are not match! Please try again', category='error')

    return render_template('user/login.html', form=form)

def logout_page():
    current_user.last_seen = dt.datetime.utcnow()
    db.session.commit()
    logout_user()
    flash("You have been logged out!", category='success')
    return redirect(url_for("home_page"))

def confirm_email(token):
    try:
        email = confirm_password_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', category='error')
        return redirect(url_for('home_page'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', category='success')
        return redirect(url_for('login_page'))
    else:
        user.confirmed = True
        user.confirmed_on = dt.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account.', category='success')
    return redirect(url_for('home_page'))

def unconfirmed_email_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = ResendConfirmationForm()
    if form.validate_on_submit():
        emails_limit = app.config['CONFIRM_REGISTRATION_ML'] - em.get_emails_count_to_address_last_days(form.email.data,'registration_confirm',1)
        if emails_limit>0:
            em.insert_email_log(0,None,form.email.data,'registration_confirm')
            em.send_email_confirmation(form.email.data)
            flash('A new confirmation email has been sent.', 'success')
            return redirect(url_for('home_page'))
        else:
            flash('Daily limit for account confirmation emails has been exceeded. Check your SPAM folder or try again tomorrow.', 'error')
    return render_template('user/unconfirmed.html',form=form)

def account_recovery_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = AccountRecoveryForm()
    if form.validate_on_submit():
        em.send_account_recovery(form.email.data)
        flash(f"'A account recovery email has been sent.", category='success')
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/account_recovery.html',form=form)

def set_password_page(token):
    try:
        email = confirm_account_recovery_token(token)
    except:
        flash('The account recovery link is invalid or has expired.', category='error')
        return redirect(url_for('home_page'))
    
    form = SetNewPasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
            user.password = form.password.data
            db.session.commit()
            flash('Your password has been successfully changed.', category='success')
            return redirect(url_for('login_page'))
        except:
            flash('Something went wrong.', category='error')
            return redirect(url_for('home_page'))

    return render_template('user/set_password.html',form=form)
   
def profile_page(user_id):

    user = User.query.filter_by(id=user_id).first()
   
    if not user or not user.confirmed:
        flash('User does not exists', category='error')
        return redirect(url_for('home_page'))

    content = {
        'articles_num' : len(user.rel_created_papers),
        'votes_score' : user.votes_score,
        'comments_num' : len(user.rel_created_comments),
        'reviews_num' : len(user.rel_created_reviews)
    }

    return render_template('user/user_profile.html', user=user,content=content)

def edit_profile_page():
    form = EditProfileForm( review_mails_limit = current_user.review_mails_limit,notifications_frequency = current_user.notifications_frequency)
    if form.validate_on_submit():
        flash_message = 'Your changes have been saved.'
        current_user.first_name = form.first_name.data
        current_user.second_name = form.second_name.data
    
        if current_user.email != form.email.data:
            current_user.new_email = form.email.data
            #check if any other account wanted to set this email
            other_accounts = User.query.filter(User.id!=current_user.get_id(),User.new_email==form.email.data).all()
            for account in other_accounts:      
                account.new_email = None
                db.session.add(account)
                
            em.send_email_change_confirmation(form.email.data)
            flash_message+=' A confirmation link has been send to your email address: '+form.email.data
  
        current_user.affiliation = form.affiliation.data
        current_user.orcid = form.orcid.data
        current_user.google_scholar = form.google_scholar.data
        current_user.about_me = form.about_me.data
        current_user.personal_website = form.personal_website.data
        current_user.review_mails_limit = form.review_mails_limit.data
        current_user.notifications_frequency = form.notifications_frequency.data

        f = form.profile_image.data
        if f:
            filename = secure_filename(f'{current_user.id}.png')
            path = f"open_science/{app.config['PROFILE_IMAGE_URL']}{filename}"
            if current_user.has_photo:
                os.remove(path)

            img = Image.open(f)
            img = img.resize((256, 256))
            img.save(path, "PNG")
          
            current_user.has_photo =True

        db.session.commit()
        flash(flash_message,category='success')
        return redirect(url_for('profile_page',user_id = current_user.get_id()))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name 
        form.second_name.data = current_user.second_name 
        form.email.data = current_user.email  
        form.affiliation.data = current_user.affiliation 
        form.orcid.data = current_user.orcid 
        form.google_scholar.data = current_user.google_scholar 
        form.about_me.data = current_user.about_me 
        form.personal_website.data = current_user.personal_website 
       
    return render_template('user/edit_profile.html',form=form)


def change_password_page():
    
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(id=current_user.get_id()).first_or_404()
            user.password = form.password.data
            db.session.commit()
            flash('Your password has been successfully changed.', category='success')
            return redirect(url_for('edit_profile_page'))
        except:
            flash('Something went wrong.', category='error')
            return redirect(url_for('home_page'))

    return render_template('user/set_password.html',form=form)

def confirm_email_change(token):
    try:
        new_email = confirm_email_change_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', category='error')
        return redirect(url_for('home_page'))
    user = User.query.filter_by(new_email=new_email).first_or_404()
    if user.email == user.new_email:
        return redirect(url_for('login_page'))
    else:
        logout_user() 
        user.email = user.new_email
        user.new_email = None
        db.session.add(user)
        db.session.commit()
        flash('You have changed your email address', category='success')
    
    return redirect(url_for('login_page'))

def invite_user_page():

    form = InviteUserForm()

    if form.validate_on_submit():
      
        emails_limit = CONFIG['INVITE_USER_ML'] - em.get_emails_cout_last_days(current_user.id,'user_invite',1)
     
        email = form.email.data
                                
        if emails_limit>0:
            
            if not bool(db.session.query(User.id).filter(User.email==email).first()):
                if em.get_emails_count_to_address_last_days(email,'user_invite',30)==0:
                    em.insert_email_log(current_user.id,None,email,'user_invite')
                    em.send_invite(email,current_user.first_name, current_user.second_name)

                    flash(f'An invitation email has been sent', category='success')
                    return redirect(url_for('profile_page',user_id = current_user.get_id()))
                else:
                    flash(f'An invitation email to this person has already been sent',category='warning')
            else:
                flash(f'User with this e-mail already exists',category='warning')
    
        else:
            flash(f'Daily limit for invitations has been exceeded',category='error')


    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/invite_user.html', form=form)

def review_request_page(request_id):
    # TODO: show paper abstract ...

    review_request = ReviewRequest.query.filter(ReviewRequest.id == request_id, ReviewRequest.requested_user == current_user.id).first_or_404()
    if review_request.acceptation_date is not None or review_request.declined_reason is not None:
        flash(f'Review request has been resolved',category='warning')
        return redirect(url_for('profile_page', user_id=current_user.id))

    form = ReviewRequestForm()
    if form.validate_on_submit():
        if form.submit_accept.data:
            review_request.decision = True
            review_request.acceptation_date = dt.date.utctoday()
            review = Review(creator = current_user.id, related_paper_version=review_request.paper_version)
            review.deadline_date = dt.datetime.utcnow().date() + dt.timedelta(days = int(form.prepare_time.data))
            db.session.add(review)
            flash(f'Review request accepted',category='success')
        elif form.submit_decline.data:
            review_request.decision = False
            review_request.declined_reason = form.declined_reason.data
            flash(f'Review request declined',category='warning')

        db.session.add(review_request)
        db.session.commit()
        
        return redirect(url_for('profile_page', user_id=current_user.id))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/review_request.html',form=form)

def notifications_page(page,unread):
    page = int(page)

    if unread =='False':
        notifications = current_user.rel_notifications.order_by(Notification.datetime.desc()).paginate(page=page, per_page=20)
    else:
        notifications = current_user.rel_notifications.filter(Notification.was_seen==False).order_by(Notification.datetime.desc()).paginate(page=page, per_page=20)

    if not notifications:
        flash('You don\'t have any notifications', category='success')
        return redirect(url_for('profile_page', user_id=current_user.id))

    return render_template('notification/notifications_page.html',page=page,unread=unread,results=notifications)

def user_papers_data():
   
   #TODO: Use current_user.id() to get only user's papers

    query = Paper.query

    # search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Paper.title.like(f'%{search}%')
        ))
    total_filtered = query.count()

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in ['title', 'votes_score']:
            col_name = 'title'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Paper, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    if order:
        query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    # response
    return {
        'data': [paper.to_dict() for paper in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Paper.query.count(),
        'draw': request.args.get('draw', type=int),
    }


