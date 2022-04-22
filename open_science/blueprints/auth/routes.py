from open_science.blueprints.auth.forms import RegisterForm, LoginForm, \
    ResendConfirmationForm, AccountRecoveryForm, \
    SetNewPasswordForm
from open_science.blueprints.auth.forms import DeleteProfileForm
from open_science import db
from open_science.tokens import confirm_password_token, \
    confirm_account_recovery_token, confirm_email_change_token, \
    confirm_profile_delete_token
from open_science.models import PrivilegeSet,\
     User
import open_science.email as em
from flask_login import login_user, logout_user, current_user
from flask import render_template, redirect, url_for, flash, request
import datetime as dt
from flask import current_app as app
from open_science.enums import EmailTypeEnum
from open_science import strings as STR
from open_science import limiter
from flask_login import login_required, fresh_login_required
from open_science.blueprints.auth import bp


@bp.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per second")
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        ps_standard_user = PrivilegeSet.query.filter(
            PrivilegeSet.id == User.user_types_enum.STANDARD_USER.value)\
                .first()
        print(form.password.data)

        user_to_create = User.query.filter(User.email == form.email.data,
                                           User.registered_on
                                               .is_(None)).first()

        # check if user exists because is co-author of someone's paper
        if user_to_create:
            user_to_create.first_name = form.first_name.data
            user_to_create.second_name = form.second_name.data
            user_to_create.password = form.password.data
            user_to_create.review_mails_limit = form.review_mails_limit.data
            user_to_create.notifications_frequency = \
                form.notifications_frequency.data
            user_to_create.registered_on = dt.datetime.utcnow()
        else:
            user_to_create = User(first_name=form.first_name.data,
                                  second_name=form.second_name.data,
                                  email=form.email.data,
                                  plain_text_password=form.password.data,
                                  review_mails_limit=form
                                  .review_mails_limit.data,
                                  notifications_frequency=form.
                                  notifications_frequency.data,
                                  registered_on=dt.datetime.utcnow())
            
        user_to_create.rel_privileges_set = ps_standard_user
        db.session.add(user_to_create)
        db.session.commit()
        em.insert_email_log(0, None, user_to_create.email,
                            EmailTypeEnum.REGISTRATION_CONFIRM.value)
        em.send_email_confirmation(user_to_create.email)
        flash(STR.EMAIL_CONFIRM_LINK_SENT+user_to_create.email, category='success')
        return redirect(url_for('auth.unconfirmed_email_page'))

    return render_template('user/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("3 per second")
def login_page():
    if current_user.is_authenticated:
        flash(STR.ALREADY_LOGGED, category='warning')
        return redirect(url_for('main.home_page'))
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
            return redirect(url_for('main.home_page'))
        elif not attempted_user:
            flash(STR.EMAIL_PASSWORD_NOT_MATCH,
                  category='error')
        elif not attempted_user.confirmed:
            flash(STR.CONFIRM_YOUR_ACCOUNT, category='warning')
            return redirect(url_for('auth.unconfirmed_email_page'))
        elif attempted_user.is_deleted is True:
            flash(STR.PROFILE_IS_DELETED, category='error')
        else:
            flash(STR.EMAIL_PASSWORD_NOT_MATCH,
                  category='error')

    return render_template('user/login.html', form=form)


@bp.route('/logout')
@login_required
def logout_page():
    current_user.last_seen = dt.datetime.utcnow()
    db.session.commit()
    logout_user()
    flash("You have been logged out!", category='success')
    return redirect(url_for("main.home_page"))


@bp.route('/confirm-email/<token>')
def confirm_email(token):
    try:
        email = confirm_password_token(token)
    except Exception:
        flash(STR.INVALID_CONFIRM_LINK,
              category='error')
        return redirect(url_for('main.home_page'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash(STR.ACCOUNT_ALREADY_CONFIRMED, category='success')
        return redirect(url_for('auth.login_page'))
    else:
        user.confirmed = True
        user.confirmed_on = dt.datetime.now()
        user.try_endorse_with_email()
        db.session.add(user)
        db.session.commit()
        flash(STR.ACCOUNT_CONFIRMED, category='success')
    return redirect(url_for('main.home_page'))


@bp.route('/user/unconfirmed', methods=['GET', 'POST'])
def unconfirmed_email_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

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
            return redirect(url_for('main.home_page'))
        else:
            flash(
                STR.ACC_CONFIRM_DAILY_LIMIT_EXC,
                'error')
    return render_template('user/unconfirmed.html', form=form)


@bp.route('/user/account-recovery', methods=['GET', 'POST'])
@limiter.limit("2 per second")
def account_recovery_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))

    form = AccountRecoveryForm()
    if form.validate_on_submit():
        em.send_account_recovery(form.email.data)
        flash(STR.EMAIL_RECOVERY_SENT, category='success')
        return redirect(url_for('main.home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'{err_msg}', category='error')

    return render_template('user/account_recovery.html', form=form)


@bp.route('/user/set-password/<token>', methods=['GET', 'POST'])
def set_password_page(token):
    try:
        email = confirm_account_recovery_token(token)
    except Exception:
        flash(STR.INVALID_REVOVERY_LINK,
              category='error')
        return redirect(url_for('main.home_page'))

    form = SetNewPasswordForm()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=email).first_or_404()
            user.password = form.password.data
            db.session.commit()
            flash(STR.PASSWORD_CHANGED_SUCCESSFULLY,
                  category='success')
            return redirect(url_for('auth.login_page'))
        except Exception:
            flash(STR.STH_WENT_WRONG, category='error')
            return redirect(url_for('main.home_page'))

    return render_template('user/set_password.html', form=form)

@bp.route('/user/change_password', methods=['GET', 'POST'])
@fresh_login_required
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
            return redirect(url_for('user.edit_profile_page'))
        except Exception:
            flash('Something went wrong.', category='error')
            return redirect(url_for('main.home_page'))

    return render_template('user/set_password.html', form=form)


@bp.route('/email_change_confirmation/<token>', methods=['GET', 'POST'])
def confirm_email_change(token):
    try:
        new_email = confirm_email_change_token(token)
    except Exception:
        flash(STR.INVALID_CONFIRM_LINK, category='error')
        return redirect(url_for('main.home_page'))
    user = User.query.filter_by(new_email=new_email).first_or_404()
    if user.email == user.new_email:
        return redirect(url_for('auth.login_page'))
    else:
        logout_user()
        user.email = user.new_email
        user.new_email = None
        user.try_endorse_with_email()
        db.session.add(user)
        db.session.commit()
        flash(STR.EMAIL_CHANGED, category='success')

    return redirect(url_for('auth.login_page'))



@bp.route('/user/delete_profile', methods=['GET', 'POST'])
@fresh_login_required
def delete_profile_page():

    form = DeleteProfileForm()

    if form.validate_on_submit():

        current_user.new_email = 'DELETE_PROFILE_ATTEMPT'
        db.session.commit()
        em.send_profile_delete(current_user.email)

        flash(STR.EMAIL_DELETE_ACCOUNT_SENT, category='success')
        return redirect(url_for('user.profile_page', user_id=current_user.id))

    return render_template('user/delete_profile.html', form=form)


@bp.route('/user/delete_profile/confirm/<token>')
@fresh_login_required
def confirm_profile_delete(token):
    try:
        email = confirm_profile_delete_token(token)
    except Exception:
        flash(STR.INVALID_CONFIRM_LINK, category='error')
        return redirect(url_for('main.home_page'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.email == current_user.email and user.new_email == 'DELETE_PROFILE_ATTEMPT':

        current_user.delete_profile()
        logout_user()
        flash(STR.ACCOUNT_DELETED_SUCCESSFULLY, category='success')
        return redirect(url_for('main.home_page'))

    else:
        flash(STR.INVALID_CONFIRM_LINK, category='error')
        return redirect(url_for('main.home_page'))
