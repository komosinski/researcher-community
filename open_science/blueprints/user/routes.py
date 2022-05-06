from flask_migrate import current
from open_science.blueprints.user.forms import  RemarksForm
from open_science.blueprints.user.forms import InviteUserForm, EditProfileForm, \
    EndorsementRequestForm
from open_science import db
from open_science.models import CalibrationPaper, Notification,\
     User, EndorsementRequestLog, NotificationType
import open_science.email as em
from flask_login import logout_user, current_user
from flask import render_template, redirect, url_for, flash, request
from flask import abort
import datetime as dt
from werkzeug.utils import secure_filename
import os
from PIL import Image
from flask import current_app as app
from open_science.utils import check_numeric_args, researcher_user_required
from open_science.enums import EmailTypeEnum, NotificationTypeEnum
from open_science.blueprints.database.db_helper import get_hidden_filter
from text_processing.prepocess_text import get_text
import text_processing.similarity_matrix as sm
from open_science import strings as STR
from config.config import Config
from flask_login import login_required, fresh_login_required
from open_science.blueprints.user import bp


@bp.route('/user/<user_id>', methods=['GET', 'POST'])
def profile_page(user_id):

    if not check_numeric_args(user_id):
        abort(404)

    user = User.query.filter(User.id == user_id,
                             get_hidden_filter(User)).first()

    if not user or user.confirmed is False or user.is_deleted is True:
        flash(STR.USER_NOT_EXISTS, category='error')
        return redirect(url_for('main.home_page'))

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



@bp.route('/user/edit_profile', methods=['GET', 'POST'])
@fresh_login_required
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
        current_user.notifications_frequency = form.notifications_frequency.data


        if current_user.is_researcher():

            current_user.review_mails_limit = form.review_mails_limit.data
            
            # get the calibration files
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
            
                path = os.path.join(Config.ROOTDIR, Config.PDFS_DIR_PATH, filename)
                url = url_for('static', filename=f"articles/{filename}")

                file.save(path)

                calibration_paper.pdf_url = url
                calibration_paper.preprocessed_text = get_text(path)

                current_user.rel_calibration_papers.append(calibration_paper)

                sm.update_dictionary(calibration_paper.preprocessed_text)
                sm.update_tfidf_matrix()
                sm.update_similarity_matrix(calibration_paper.preprocessed_text)


        f = form.profile_image.data
        if f:
            filename = secure_filename(f'{current_user.id}.jpg')
            path = os.path.join(Config.ROOTDIR, Config.PROFILE_IMAGES_DIR_PATH, filename)
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
            return redirect(url_for('main.home_page'))

        return redirect(url_for('user.profile_page', user_id=current_user.get_id()))

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


@bp.route('/user/invite', methods=['GET', 'POST'])
@login_required
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
                    return redirect(url_for('user.profile_page', user_id=current_user.get_id()))
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


@bp.route('/endorsement/request/<endorser_id>')
@login_required
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
        notification.action_url = url_for('user.confirm_endorsement_page',
                                          notification_id=notification.id,
                                          user_id=current_user.id,
                                          endorser_id=endorser_id)

        db.session.add(endorsement_log)
        db.session.commit()
        flash(STR.ENDORSEMENT_REQUEST_SENT,
              category='success')
        return redirect(url_for('user.profile_page', user_id=endorser_id))
    else:
        flash(STR.CANT_REQUEST_ENDORSEMENT, category='error')
        return redirect(url_for('user.profile_page', user_id=endorser_id))



@bp.route('/endorsement/confirm/<notification_id>/<user_id>/<endorser_id>',
           methods=['GET', 'POST'])
@login_required
@researcher_user_required
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
        return redirect(url_for('notification.notifications_page', page=1, unread='False'))

    if not user or current_user.id != endorser_id or not endorsement_log:
        flash(STR.ENDORSEMENT_REQUEST_NOT_EXISTS, category='error')
        return redirect(url_for('notification.notifications_page', page=1, unread='False'))

    if endorsement_log.considered is True:
        flash(STR.ENDORSEMENT_REQUEST_ALREADY_CONSIDERED, category='warning')
        return redirect(url_for('notification.notifications_page', page=1, unread='False'))

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
        return redirect(url_for('notification.notifications_page', page=1, unread='False'))

    return render_template('user/endorsement_request.html', form=form, user=user)

