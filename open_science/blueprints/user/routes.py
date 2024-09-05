from flask_migrate import current
from sqlalchemy.orm import joinedload

from open_science.blueprints.user.forms import  RemarksForm
from open_science.blueprints.user.forms import InviteUserForm, EditProfileForm, \
    EndorsementRequestForm
from open_science import db
from open_science.models import CalibrationPaper, Notification, \
    User, EndorsementRequestLog, NotificationType, UserBadge
import open_science.myemail as em
from flask_login import logout_user, current_user
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask import abort
from flask import Markup
import datetime as dt
from werkzeug.utils import secure_filename
import os
from PIL import Image, ImageOps
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
from config import models_config as mc

@bp.route('/user/<user_id>', methods=['GET', 'POST'])
def profile_page(user_id):

    if not check_numeric_args(user_id):
        abort(404)

    user = User.query.filter(User.id == user_id,
                             get_hidden_filter(User)).first()
    user_badges = UserBadge.query.options(joinedload(UserBadge.badge)).filter_by(user_id=user_id).all()
    badges = [user_badge.badge for user_badge in user_badges]
    hasUserCalibrationPapers = len(user.rel_calibration_papers) > 0

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
                               user=user, data=data, remarks_form=remarks_form,
                               hasUserCalibrationPapers=hasUserCalibrationPapers, badges=badges)
    elif request.method == 'GET':
        remarks_form.remarks.data = user.remarks

    return render_template('user/user_profile.html',
                           user=user, data=data, remarks_form=remarks_form,
                           hasUserCalibrationPapers=hasUserCalibrationPapers, badges=badges)


@bp.route('/user/upload_avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['avatar']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(f'{current_user.id}.jpg')
        path = os.path.join(Config.ROOTDIR, Config.PROFILE_IMAGES_DIR_PATH, filename)

        try:
            if current_user.has_photo:
                os.remove(path)

            img = Image.open(file)
            img = img.convert('RGB')

            img = scale_image(img, 256)
            img.save(path, format="JPEG", quality=90)

            current_user.has_photo = True
            db.session.commit()

            return jsonify({'message': 'Avatar uploaded successfully'}), 200
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error uploading avatar'}), 500
    else:
        return jsonify({'error': 'File type not allowed'}), 400


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Scale the image to fit within max_size while maintaining aspect ratio.
#Also crops the image to a square if it's not already square.
def scale_image(img, max_size):
    img = ImageOps.fit(img, (min(img.size), min(img.size)), Image.LANCZOS)

    if max(img.size) > max_size:
        scale = max_size / max(img.size)
        new_size = tuple(int(dim * scale) for dim in img.size)
        img = img.resize(new_size, Image.LANCZOS)

    return img
@bp.route('/user/edit_profile', methods=['GET', 'POST'])
@fresh_login_required
def edit_profile_page():
    form = EditProfileForm(review_mails_limit=current_user.review_mails_limit,
                           notifications_frequency=current_user.notifications_frequency)

    email_change = False

    if form.validate_on_submit():
        flash_message = STR.EDIT_PROFILE_CHANGES_SAVED
        try:

            current_user.first_name = Markup.escape(form.first_name.data)
            current_user.second_name = Markup.escape(form.second_name.data)
            
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

            db.session.commit()
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('main.home_page'))

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


@bp.route('/user/edit_calibration_files', methods=['GET', 'POST'])
@login_required
@researcher_user_required
def edit_calibration_files():
        calibration_papers = CalibrationPaper.query.filter(CalibrationPaper.author==current_user.id).order_by(CalibrationPaper.id.desc()).all()
        return render_template('user/edit_calibration_files.html', calibration_papers=calibration_papers)


@bp.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@bp.route('/user/upload_calibration_file', methods=['POST'])
@login_required
@researcher_user_required
def upload_calibration_file():
    uploaded_file = request.files['file']
    base_filename = secure_filename(uploaded_file.filename)
    if base_filename != '':
        file_ext = os.path.splitext(base_filename)[1]
        if file_ext != '.pdf':
            return "Invalid file format", 400
        try:
            calibration_paper = CalibrationPaper(
            pdf_url=""
            )
            db.session.add(calibration_paper)
            db.session.flush()
            id = calibration_paper.id
            new_filename = secure_filename(f"{id}.pdf")
            path = os.path.join(Config.ROOTDIR, Config.PDFS_DIR_PATH, new_filename)
            url = url_for('static', filename=f"articles/{new_filename}")
            uploaded_file.save(path)
            calibration_paper.pdf_url = url
            
            try:
                calibration_paper.preprocessed_text = get_text(path)
            except Exception as ex:
                print(ex)
                flash(STR.PAPER_WORD_COUNT_ERROR, category='error')
                return redirect(url_for('main.home_page'))
            
            calibration_paper.description = f'{base_filename} | {calibration_paper.preprocessed_text[:200]}'[:mc.CP_DESCRIPTION_L]
            current_user.rel_calibration_papers.append(calibration_paper)
            db.session.commit()
            if app.config['TEXT_PROCESSING_UPDATE_FILES_ON_UPLOAD'] is True:
                sm.update_dictionary(calibration_paper.preprocessed_text)
                sm.update_tfidf_matrix()
                sm.update_similarity_matrix(calibration_paper.preprocessed_text)
        except Exception as err:
            print(err)
            return "Error", 400
    return '', 204
 

@bp.route('/user/delete_calibration_paper/<paper_id>', methods=['GET', 'POST'])
@login_required
def delete_calibration_paper(paper_id):
    if not check_numeric_args(paper_id):
        abort(404)
    calibration_paper = CalibrationPaper.query.filter(CalibrationPaper.author==current_user.id, CalibrationPaper.id==int(paper_id)).first()
    if calibration_paper is None:
        flash(STR.CP_NOT_EXISTS, category='error')
    else:
        # TODO: check if calibration paper can be deleted
        try:
            path = os.path.join(Config.ROOTDIR, Config.PDFS_DIR_PATH, calibration_paper.pdf_url.split('/')[-1])
            os.remove(path)
            db.session.delete(calibration_paper)
            db.session.commit()
            flash(STR.CP_DELETE_SUCCESS, category='success')
        except Exception as err:
            print(f'Error during calibration paper deletion: {err}')
            flash(STR.CP_DELETE_FAILED, category='error')
  
    return redirect(url_for('user.edit_calibration_files'))

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
        try:
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
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('main.home_page'))

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
        try:
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
        except Exception as e:
            print(e)
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('main.home_page'))
            
        flash(STR.ENDORSEMENT_REQUEST_FORM_COMPLETED, category='success')
        return redirect(url_for('notification.notifications_page', page=1, unread='False'))

    return render_template('user/endorsement_request.html', form=form, user=user)


@bp.route('/user/account_settings')
@login_required
def account_settings():
    return render_template('user/account_settings.html')
