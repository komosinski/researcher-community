from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextAreaField
from open_science.models import User
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, \
    SubmitField, BooleanField, MultipleFileField
from wtforms.validators import Length, EqualTo, Email,\
    DataRequired, Optional, ValidationError
import re
import config.models_config as mc
import open_science.email as em
from config.config import Config
from flask_login import current_user
from open_science.enums import EmailTypeEnum
from open_science import strings as STR


def validate_password(form, password):
    if not re.search("[a-z]", password.data):
        raise ValidationError(
            'The password must contain at least one lowercase character.')
    elif not re.search("[A-Z]", password.data):
        raise ValidationError(
            'The password must contain at least one uppercase character.')
    elif not re.search("[0-9]", password.data):
        raise ValidationError('The password must contain at least one digit.')
    elif not re.search("[^A-Za-z0-9]", password.data):
        raise ValidationError(
            'The password must contain at least one special character.')


def validate_password_with_userdata(form, password):
    if form.first_name.data.lower() in password.data.lower():
        raise ValidationError('The password can not contain your first name.')
    elif form.second_name.data.lower() in password.data.lower():
        raise ValidationError('The password can not contain your second name.')
    elif form.email.data.lower().split("@")[0] in password.data.lower():
        raise ValidationError(
            'The password can not contain your email address.')


# protect against creating multiple researcher accounts with same email
def was_email_used_in_site(email):
    confirm_emails_count = em.get_emails_count_to_address_last_days(
                    email,
                    EmailTypeEnum.REGISTRATION_CONFIRM.value
                )
    if confirm_emails_count > 0:
        return True
    return False


def validate_register_email(self, email):
    user_with_email_address = User.query.filter_by(email=email.data).first()
    if user_with_email_address \
       and user_with_email_address.registered_on:
        raise ValidationError(
            'That email address is already in use, \
            please use a different email address')

    if was_email_used_in_site(email.data):
        raise ValidationError(
            'You cannot use the same email \
                address for registration again.')


class RegisterForm(FlaskForm):
    first_name = StringField(label='First name', validators=[
                             Length(min=2,
                                    max=mc.USER_FIRST_NAME_L),
                             DataRequired()])
    second_name = StringField(label='Last name', validators=[
                              Length(min=2, max=mc.USER_SECOND_NAME_L),
                              DataRequired()])

    email = StringField(label='Email address', validators=[
                        Email(), DataRequired(), validate_register_email])
    password = PasswordField(label='Password', validators=[Length(
        min=8, max=32), DataRequired(), validate_password,
        validate_password_with_userdata])
    password_confirm = PasswordField(label='Confirm password', validators=[
                                     EqualTo('password'), DataRequired()])

    review_mails_limit = SelectField(label='Limit on the number of review requests', choices=[(1, '1'),
                                              (2, '2'),
                                              (3, '3'),
                                              (4, '4'),
                                              (0, 'I don\'t want to participate in peer review')])

    notifications_frequency = SelectField(label='Frequency of notifications', choices=[(
        1, '1 day'), (3, '3 days'), (7, '1 week'),
        (14, '2 weeks'), (30, '1 month'), (0, 'Never')])

    recaptcha = RecaptchaField()

    submit = SubmitField(label='Create account')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Sign in')


class ResendConfirmationForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email address.')
        elif user.confirmed:
            raise ValidationError('This email address is already confirmed.')

    email = StringField(label='Email address', validators=[
                        Email(), DataRequired()])
    submit = SubmitField(label='Resend confirmation email')


class AccountRecoveryForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email address.')
        if user.confirmed is False:
            raise ValidationError('This email address is not confirmed.')

    email = StringField(label='Email address', validators=[
                        Email(), DataRequired()])
    submit = SubmitField(label='Send recovery email')


class SetNewPasswordForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email address.')

    password = PasswordField(label='Password', validators=[Length(
        min=8, max=32), DataRequired(), validate_password])
    password_confirm = PasswordField(label='Confirm password', validators=[
                                     EqualTo('password'), DataRequired()])

    submit = SubmitField(label='Set password')


class DeleteProfileForm(FlaskForm):

    def validate_read_information(form, field):
        if form.submit.data:
            if not field.data:
                raise ValidationError('You must acknowledge the consequences.')

    check_read = BooleanField(STR.CHECK_READ_BEFORE_PROFILE_DELETE,
                              validators=[
                                validate_read_information], default=False)

    submit = SubmitField(label='Send an account deletion email')

