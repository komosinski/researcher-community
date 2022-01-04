from open_science.user.forms import RegisterForm, LoginForm, ResendConfirmationForm, AccountRecoveryForm, SetNewPasswordForm
from open_science.user.forms import InviteUserForm, EditProfileForm , EndorsementRequestForm
from open_science import db
from open_science.tokens import confirm_password_token, confirm_account_recovery_token, confirm_email_change_token
from open_science.models import Notification, Paper, PrivilegeSet, User, Tag, Review, EndorsementRequestLog
import open_science.email as em
from flask.helpers import url_for
from flask.templating import render_template
from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, flash, request
from flask import abort
import datetime as dt
from werkzeug.utils import secure_filename
import os
from PIL import Image
from open_science import app
from open_science.routes_def import check_numeric_args
from open_science.enums import EmailTypeEnum, NotificationTypeEnum

def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        ps_standard_user = PrivilegeSet.query.filter(PrivilegeSet.id==User.user_types_enum.STANDARD_USER.value).first()
        print(form.password.data)
        user_to_create = User(first_name=form.first_name.data,
                              second_name=form.second_name.data,
                              email=form.email.data,
                              plain_text_password=form.password.data,
                              affiliation = form.affiliation.data,
                              orcid = form.orcid.data,
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
        emails_limit = app.config['CONFIRM_REGISTRATION_ML'] - em.get_emails_count_to_address_last_days(form.email.data,EmailTypeEnum.REGISTRATION_CONFIRM.value,1)
        if emails_limit>0:
            em.insert_email_log(0,None,form.email.data, EmailTypeEnum.REGISTRATION_CONFIRM.value)
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
    # TODO: limit reviews to submitted reviews
    data = {
        'articles_num' : len(user.rel_created_paper_versions),
        'reputation' : user.reputation,
        'comments_num' : len(user.rel_created_comments),
        'reviews_num' : user.get_reviews_count()
    }

    return render_template('user/user_profile.html', user=user,data=data)

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
      
        emails_limit = app.config['INVITE_USER_ML'] - em.get_emails_cout_last_days(current_user.id, EmailTypeEnum.USER_INVITE.value, 1)
     
        email = form.email.data
                                
        if emails_limit>0:
            
            if not bool(db.session.query(User.id).filter(User.email==email).first()):
                if em.get_emails_count_to_address_last_days(email,EmailTypeEnum.USER_INVITE.value,30)==0:
                    em.insert_email_log(current_user.id,None,email,EmailTypeEnum.USER_INVITE.value)
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


def notifications_page(page,unread):
    if not check_numeric_args(page):
        abort(404)
    page = int(page)

    if unread =='False':
        notifications = current_user.rel_notifications.order_by(Notification.datetime.desc()).paginate(page=page, per_page=20)
    else:
        notifications = current_user.rel_notifications.filter(Notification.was_seen==False).order_by(Notification.datetime.desc()).paginate(page=page, per_page=20)

    if not notifications:
        flash('You don\'t have any notifications', category='success')
        return redirect(url_for('profile_page', user_id=current_user.id))

    return render_template('notification/notifications_page.html',page=page,unread=unread,results=notifications)

def update_notification_and_redirect():

    notification_id = int(request.args.get('notification_id'))
    url = request.args.get('url')

    notification = Notification.query.filter(Notification.id == notification_id).first()
  
    if current_user.id != notification.user_id:
        abort(404)
    
    notification.was_seen = True
    db.session.commit()

    return redirect(url)


def request_endorsement(endorser_id):
    if not check_numeric_args(endorser_id):
        abort(404)

    if current_user.can_request_endorsement(endorser_id):
        endorsement_log = EndorsementRequestLog(user_id=current_user.id, endorser_id=endorser_id, date = dt.datetime.utcnow().date())

        notification = Notification(endorser_id,dt.datetime.utcnow(),'Endorsement request',NotificationTypeEnum.ENDORSEMENT_REQUEST.value)
        db.session.add(notification)
        db.session.flush()
        db.session.refresh(notification)
        notification.action_url = url_for('confirm_endorsement_page',notification_id=notification.id, user_id=current_user.id, endorser_id=endorser_id)
        
        db.session.add(endorsement_log)
        db.session.commit()
        flash('The Endorsement request was successfully sent', category='success')
        return redirect(url_for('profile_page', user_id=endorser_id))
    else:
        flash('You cannot send your endorsement request', category='error')
        return redirect(url_for('profile_page', user_id=endorser_id))




def confirm_endorsement_page(notification_id, user_id, endorser_id):
    if not check_numeric_args(user_id,endorser_id):
        abort(404)

    notification_id = int(notification_id)
    user_id = int(user_id)
    endorser_id = int(endorser_id)

    form = EndorsementRequestForm()
    user = User.query.filter(User.id == user_id).first()
    endorsement_log = EndorsementRequestLog.query.filter(EndorsementRequestLog.user_id == user_id, EndorsementRequestLog.endorser_id == endorser_id).first()
    notification = Notification.query.filter(Notification.id == notification_id).first()

    if not notification:
        flash('Endorsement request not exists', category='error')
        return redirect(url_for('notifications_page', page=1, unread=False))

    if not user or current_user.id != endorser_id or not endorsement_log:
        flash('Endorsement request not exists', category='error')
        return redirect(url_for('notifications_page', page=1, unread=False))

    if endorsement_log.considered == True:
        flash('Endorsement request has been already considered', category='warning')
        return redirect(url_for('notifications_page', page=1, unread=False))

    if form.validate_on_submit():
        if form.submit_accept.data:
            endorsement_log.decision = True
            endorsement_log.considered = True
            db.session.commit()
            if user.obtained_required_endorsement():
                user.rel_privileges_set = PrivilegeSet.query.filter(PrivilegeSet.id == User.user_types_enum.SCIENTIST_USER.value).first()
                db.session.add(user)
              
        elif form.submit_decline.data:
            endorsement_log.decision = False
            endorsement_log.considered = True
            db.session.add(endorsement_log)
           
        db.session.delete(notification)
        db.session.commit()

        flash('The form has been completed', category='success')
        return redirect(url_for('notifications_page', page=1, unread=False))

    return render_template('user/endorsement_request.html', form=form, user=user)
