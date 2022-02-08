from flask_migrate import current
from open_science.user.forms import RegisterForm, LoginForm, RemarksForm, \
    ResendConfirmationForm, AccountRecoveryForm, \
    SetNewPasswordForm
from open_science.user.forms import InviteUserForm, EditProfileForm, \
    EndorsementRequestForm, DeleteProfileForm
from open_science import db
from open_science.tokens import confirm_password_token, \
    confirm_account_recovery_token, confirm_email_change_token, \
    confirm_profile_delete_token
from open_science.models import CalibrationPaper, Notification, PrivilegeSet,\
     User, EndorsementRequestLog, NotificationType
import open_science.email as em
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
from open_science.db_helper import get_hidden_filter
from text_processing.prepocess_text import get_text
import text_processing.similarity_matrix as sm
from open_science import strings as STR
from config.config import Config

def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        ps_standard_user = PrivilegeSet.query.filter(
            PrivilegeSet.id == User.user_types_enum.STANDARD_USER.value)\
                .first()
        print(form.password.data)

        # get the calibration files
        calibration_files = []
        for file in form.calibration_files.data:
            if not file.filename: 
                continue
            
            calibration_paper = CalibrationPaper(
                pdf_url=""
            )

            db.session.add(calibration_paper)
            db.session.flush()

            id = calibration_paper.id

            filename = secure_filename(f"{id}.pdf")
           
            path = os.path.join(Config.ROOTDIR, Config.PDFS_FOLDER_URL, filename)
            url = url_for('static', filename=f"articles/{filename}")

            file.save(path)

            calibration_paper.pdf_url = url
            calibration_paper.preprocessed_text = get_text(path)

            calibration_files.append(calibration_paper)

            sm.update_dictionary(calibration_paper.preprocessed_text)
            sm.update_tfidf_matrix()
            sm.update_similarity_matrix(calibration_paper.preprocessed_text)

        user_to_create = User.query.filter(User.email == form.email.data,
                                           User.registered_on
                                               .is_(None)).first()

        # check if user exists because is co-author of someone's paper
        if user_to_create:
            user_to_create.first_name = form.first_name.data
            user_to_create.second_name = form.second_name.data
            user_to_create.password = form.password.data
            user_to_create.affiliation = form.affiliation.data
            user_to_create.orcid = form.orcid.data
            user_to_create.google_scholar = form.google_scholar.data
            user_to_create.about_me = form.about_me.data
            user_to_create.personal_website = form.personal_website.data
            user_to_create.review_mails_limit = form.review_mails_limit.data
            user_to_create.notifications_frequency = \
                form.notifications_frequency.data
            user_to_create.registered_on = dt.datetime.utcnow()
        else:
            user_to_create = User(first_name=form.first_name.data,
                                  second_name=form.second_name.data,
                                  email=form.email.data,
                                  plain_text_password=form.password.data,
                                  affiliation=form.affiliation.data,
                                  orcid=form.orcid.data,
                                  google_scholar=form.google_scholar.data,
                                  about_me=form.about_me.data,
                                  personal_website=form.personal_website.data,
                                  review_mails_limit=form
                                  .review_mails_limit.data,
                                  notifications_frequency=form.
                                  notifications_frequency.data,
                                  registered_on=dt.datetime.utcnow())
            
        user_to_create.rel_privileges_set = ps_standard_user
        db.session.add(user_to_create)
        db.session.flush()

        user_to_create.rel_calibration_papers = calibration_files

        f = form.profile_image.data
        if f:
            filename = secure_filename(f'{user_to_create.id}.jpg')
            path = os.path.join(Config.ROOTDIR, Config.PROFILE_IMAGE_URL, filename)
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((256, 256))
            img.save(path, format="JPEG", quality=90)
            user_to_create.has_photo = True

        db.session.commit()
        em.insert_email_log(0, None, user_to_create.email,
                            EmailTypeEnum.REGISTRATION_CONFIRM.value)
        em.send_email_confirmation(user_to_create.email)
        flash(STR.EMAIL_CONFIRM_LINK_SENT+user_to_create.email, category='success')
        return redirect(url_for('unconfirmed_email_page'))

    return render_template('user/register.html', form=form)


def login_page():
    if current_user.is_authenticated:
        flash(STR.ALREADY_LOGGED, category='warning')
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ) and attempted_user.confirmed \
                and attempted_user.is_deleted is not True:
            login_user(attempted_user)
            attempted_user.last_seen = dt.datetime.utcnow()
            db.session.commit()
            flash(STR.LOGIN_SUCCESS, category='success')
            next_dest = request.args.get('next')
            if next_dest:
                return redirect(next_dest)
            return redirect(url_for('home_page'))
        elif not attempted_user:
            flash(STR.EMAIL_PASSWORD_NOT_MATCH,
                  category='error')
        elif not attempted_user.confirmed:
            flash(STR.CONFIRM_YOUR_ACCOUNT, category='warning')
            return redirect(url_for('unconfirmed_email_page'))
        elif attempted_user.is_deleted is True:
            flash(STR.PROFILE_IS_DELETED, category='error')
        else:
            flash(STR.EMAIL_PASSWORD_NOT_MATCH,
                  category='error')

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
    except Exception:
        flash(STR.INVALID_CONFIRM_LINK,
              category='error')
        return redirect(url_for('home_page'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash(STR.ACCOUNT_ALREADY_CONFIRMED, category='success')
        return redirect(url_for('login_page'))
    else:
        user.confirmed = True
        user.confirmed_on = dt.datetime.now()
        user.try_endorse_with_email()
        db.session.add(user)
        db.session.commit()
        flash(STR.ACCOUNT_CONFIRMED, category='success')
    return redirect(url_for('home_page'))


def unconfirmed_email_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = ResendConfirmationForm()
    if form.validate_on_submit():
        emails_count = em.get_emails_count_to_address_last_days(form.email.data,
                                                                EmailTypeEnum.REGISTRATION_CONFIRM.value,
                                                                1)
        emails_limit = app.config['CONFIRM_REGISTRATION_ML'] - emails_count
        if emails_limit > 0:
            em.insert_email_log(0, None, form.email.data,
                                EmailTypeEnum.REGISTRATION_CONFIRM.value)
            em.send_email_confirmation(form.email.data)
            flash(STR.EMAIL_CONFIRM_EMAIL_SENT, 'success')
            return redirect(url_for('home_page'))
        else:
            flash(
                STR.ACC_CONFIRM_DAILY_LIMIT_EXC,
                'error')
    return render_template('user/unconfirmed.html', form=form)


def account_recovery_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = AccountRecoveryForm()
    if form.validate_on_submit():
        em.send_account_recovery(form.email.data)
        flash(STR.EMAIL_RECOVERY_SENT, category='success')
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/account_recovery.html', form=form)


def set_password_page(token):
    try:
        email = confirm_account_recovery_token(token)
    except Exception:
        flash(STR.INVALID_REVOVERY_LINK,
              category='error')
        return redirect(url_for('home_page'))

    form = SetNewPasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
            user.password = form.password.data
            db.session.commit()
            flash(STR.PASSWORD_CHANGED_SUCCESSFULLY,
                  category='success')
            return redirect(url_for('login_page'))
        except Exception:
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('home_page'))

    return render_template('user/set_password.html', form=form)


def profile_page(user_id):

    if not check_numeric_args(user_id):
        abort(404)

    user = User.query.filter(User.id == user_id,
                             get_hidden_filter(User)).first()

    if not user or user.confirmed is False or user.is_deleted is True:
        flash(STR.USER_NOT_EXISTS, category='error')
        return redirect(url_for('home_page'))

    data = {
        'articles_num': len(user.rel_created_paper_revisions),
        'reputation': user.reputation,
        'comments_num': len(user.rel_created_comments),
        'reviews_num': user.get_reviews_count()
    }
    remarks_form = RemarksForm()

    if remarks_form.validate_on_submit():
        user.remarks = remarks_form.remarks.data
        db.session.commit()
        flash(STR.REMARKS_SAVED, category='success')
        return render_template('user/user_profile.html',
                               user=user, data=data, remarks_form=remarks_form)
    elif request.method == 'GET':
        remarks_form.remarks.data = user.remarks

    return render_template('user/user_profile.html',
                           user=user, data=data, remarks_form=remarks_form)


def edit_profile_page():
    form = EditProfileForm(review_mails_limit=current_user.review_mails_limit,
                           notifications_frequency=current_user.notifications_frequency)

    email_change = False

    if form.validate_on_submit():
        flash_message = STR.EDIT_PROFILE_CHANGES_SAVED
        current_user.first_name = form.first_name.data
        current_user.second_name = form.second_name.data

        if current_user.email != form.email.data:
            current_user.new_email = form.email.data
            # check if any other account wanted to set this email
            other_accounts = User.query.filter(User.id != current_user.get_id(),
                                               User.new_email == form.email.data).all()
            for account in other_accounts:
                account.new_email = None
                db.session.add(account)

            email_change = True
            em.send_email_change_confirmation(form.email.data)
            flash_message += STR.EMAIL_CONFIRM_LINK_SENT + form.email.data

        current_user.affiliation = form.affiliation.data
        current_user.orcid = form.orcid.data
        current_user.google_scholar = form.google_scholar.data
        current_user.about_me = form.about_me.data
        current_user.personal_website = form.personal_website.data
        current_user.review_mails_limit = form.review_mails_limit.data
        current_user.notifications_frequency = form.notifications_frequency.data

        f = form.profile_image.data
        if f:
            filename = secure_filename(f'{current_user.id}.jpg')
            path = os.path.join(Config.ROOTDIR, Config.PROFILE_IMAGE_URL, filename)
            if current_user.has_photo:
                os.remove(path)

            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((256, 256))
            img.save(path, format="JPEG", quality=90)

            current_user.has_photo = True

        db.session.commit()

        flash(flash_message, category='success')

        if email_change:
            logout_user()
            return redirect(url_for('home_page'))

        return redirect(url_for('profile_page', user_id=current_user.get_id()))

    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.second_name.data = current_user.second_name
        form.email.data = current_user.email
        form.affiliation.data = current_user.affiliation
        form.orcid.data = current_user.orcid
        form.google_scholar.data = current_user.google_scholar
        form.about_me.data = current_user.about_me
        form.personal_website.data = current_user.personal_website

    return render_template('user/edit_profile.html', form=form)


def change_password_page():
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(
                id=current_user.get_id()).first_or_404()
            user.password = form.password.data
            db.session.commit()
            flash(STR.PASSWORD_CHANGED,
                  category='success')
            return redirect(url_for('edit_profile_page'))
        except Exception:
            flash('Something went wrong.', category='error')
            return redirect(url_for('home_page'))

    return render_template('user/set_password.html', form=form)


def confirm_email_change(token):
    try:
        new_email = confirm_email_change_token(token)
    except Exception:
        flash(STR.INVALID_CONFIRM_LINK, category='error')
        return redirect(url_for('home_page'))
    user = User.query.filter_by(new_email=new_email).first_or_404()
    if user.email == user.new_email:
        return redirect(url_for('login_page'))
    else:
        logout_user()
        user.email = user.new_email
        user.new_email = None
        user.try_endorse_with_email()
        db.session.add(user)
        db.session.commit()
        flash(STR.EMAIL_CHANGED, category='success')

    return redirect(url_for('login_page'))


def invite_user_page():
    form = InviteUserForm()

    if form.validate_on_submit():

        emails_limit = app.config['INVITE_USER_ML'] - em.get_emails_cout_last_days(current_user.id,
                                                                                   EmailTypeEnum.USER_INVITE.value, 1)

        email = form.email.data

        if emails_limit > 0:

            if not bool(db.session.query(User.id).filter(User.email == email).first()):
                if em.get_emails_count_to_address_last_days(email, EmailTypeEnum.USER_INVITE.value, 30) == 0:
                    em.insert_email_log(
                        current_user.id,
                        None,
                        email,
                        EmailTypeEnum.USER_INVITE.value)
                    em.send_invite(email, current_user.first_name,
                                   current_user.second_name)

                    flash(STR.EMAIL_INVITATION_SENT,
                          category='success')
                    return redirect(url_for('profile_page', user_id=current_user.get_id()))
                else:
                    flash(
                        STR.INVITATION_EMAIL_ALREADY_SENT, category='warning')
            else:
                flash(STR.USER_ALREADY_EXISTS, category='warning')

        else:
            flash(STR.INVITATION_DAILY_LIMIT_EXC, category='error')

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/invite_user.html', form=form)


def request_endorsement(endorser_id):
    if not check_numeric_args(endorser_id):
        abort(404)

    if current_user.can_request_endorsement(endorser_id):
        endorsement_log = EndorsementRequestLog(user_id=current_user.id, endorser_id=endorser_id,
                                                date=dt.datetime.utcnow().date())

        type_endorsment_request = NotificationType.query.get(
            NotificationTypeEnum.ENDORSEMENT_REQUEST.value)

        notification = Notification(
            datetime=dt.datetime.utcnow(),
            title=Notification.prepare_title(type_endorsment_request),
            text='Endorsement request'
        )
        notification.rel_user = User.query.get(endorser_id)
        notification.rel_notification_type = type_endorsment_request
        db.session.add(notification)
        db.session.flush()
        db.session.refresh(notification)
        notification.action_url = url_for('confirm_endorsement_page',
                                          notification_id=notification.id,
                                          user_id=current_user.id,
                                          endorser_id=endorser_id)

        db.session.add(endorsement_log)
        db.session.commit()
        flash(STR.ENDORSEMENT_REQUEST_SENT,
              category='success')
        return redirect(url_for('profile_page', user_id=endorser_id))
    else:
        flash(STR.CANT_REQUEST_ENDORSEMENT, category='error')
        return redirect(url_for('profile_page', user_id=endorser_id))


def confirm_endorsement_page(notification_id, user_id, endorser_id):
    if not check_numeric_args(notification_id, user_id, endorser_id):
        abort(404)

    notification_id = int(notification_id)
    user_id = int(user_id)
    endorser_id = int(endorser_id)

    form = EndorsementRequestForm()
    user = User.query.filter(User.id == user_id).first()
    endorsement_log = EndorsementRequestLog.query.filter(EndorsementRequestLog.user_id == user_id,
                                                         EndorsementRequestLog.endorser_id == endorser_id).first()
    notification = Notification.query.filter(
        Notification.id == notification_id).first()

    if not notification:
        flash(STR.ENDORSEMENT_REQUEST_NOT_EXISTS, category='error')
        return redirect(url_for('notifications_page', page=1, unread='False'))

    if not user or current_user.id != endorser_id or not endorsement_log:
        flash(STR.ENDORSEMENT_REQUEST_NOT_EXISTS, category='error')
        return redirect(url_for('notifications_page', page=1, unread='False'))

    if endorsement_log.considered is True:
        flash(STR.ENDORSEMENT_REQUEST_ALREADY_CONSIDERED, category='warning')
        return redirect(url_for('notifications_page', page=1, unread='False'))

    if form.validate_on_submit():
        if form.submit_accept.data:
            endorsement_log.decision = True
            endorsement_log.considered = True
            db.session.commit()
            if user.obtained_required_endorsement():
                user.endorse()

        elif form.submit_decline.data:
            endorsement_log.decision = False
            endorsement_log.considered = True
            db.session.add(endorsement_log)

        db.session.delete(notification)
        db.session.commit()

        flash(STR.ENDORSEMENT_REQUEST_FORM_COMPLETED, category='success')
        return redirect(url_for('notifications_page', page=1, unread='False'))

    return render_template('user/endorsement_request.html', form=form, user=user)


def delete_profile_page():

    form = DeleteProfileForm()

    if form.validate_on_submit():

        current_user.new_email = 'DELETE_PROFILE_ATTEMPT'
        db.session.commit()
        em.send_profile_delete(current_user.email)

        flash(STR.EMAIL_DELETE_ACCOUNT_SENT, category='success')
        return redirect(url_for('profile_page', user_id=current_user.id))

    return render_template('user/delete_profile.html', form=form)


def confirm_profile_delete(token):
    try:
        email = confirm_profile_delete_token(token)
    except Exception:
        flash(STR.INVALID_CONFIRM_LINK, category='error')
        return redirect(url_for('home_page'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.email == current_user.email and user.new_email == 'DELETE_PROFILE_ATTEMPT':

        current_user.delete_profile()
        logout_user()
        flash(STR.ACCOUNT_DELETED_SUCCESSFULLY, category='success')
        return redirect(url_for('home_page'))

    else:
        flash(STR.INVALID_CONFIRM_LINK, category='error')
        return redirect(url_for('home_page'))
