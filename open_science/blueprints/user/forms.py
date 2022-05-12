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
import open_science.myemail as em
from config.config import Config
from flask_login import current_user
from open_science.enums import EmailTypeEnum
from open_science import strings as STR



# protect against creating multiple researcher accounts with same email
def was_email_used_in_site(email):
    confirm_emails_count = em.get_emails_count_to_address_last_days(
                    email,
                    EmailTypeEnum.REGISTRATION_CONFIRM.value
                )
    if confirm_emails_count > 0:
        return True
    return False


def validate_orcid(self, orcid):
    correct = False
    if re.search(r"^[0-9]{16}$", orcid.data):
        correct = True
    elif re.search(r"^[0-9]{15}X$", orcid.data.upper()):
        correct = True
    elif re.search(r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$", orcid.data):
        correct = True
    elif re.search(r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}X$",
                   orcid.data.upper()):
        correct = True

    if not correct:
        raise ValidationError('Invalid ORCID iD')
  

class EditProfileForm(FlaskForm):
    def validate_email(form, field):
        if field.data != current_user.email:
            emails_limit = Config.CHANGE_MAIL_ML - \
                em.get_emails_cout_last_days(
                    current_user.id, EmailTypeEnum.EMAIL_CHANGE.value, 30)
            if emails_limit > 0:
                user_with_email_address = User.query.filter_by(
                    email=field.data).first()
                if user_with_email_address:
                    if user_with_email_address.id != current_user.id:
                        raise ValidationError(
                            'This email address is already in use, please use a different email address.')
                else:
                    if was_email_used_in_site(field.data):
                        raise ValidationError(
                              'This email address has already \
                                  been used for user registration')
            else:
                raise ValidationError(
                    'Monthly limit for email change has been exceeded.')

    first_name = StringField(label='First name', validators=[
                             Length(min=2,
                                    max=mc.USER_FIRST_NAME_L),
                             DataRequired()])
    second_name = StringField(label='Last name', validators=[
                              Length(min=2, max=mc.USER_SECOND_NAME_L),
                              DataRequired()])

    affiliation = StringField(label='Affiliation (Optional)', validators=[
                            Length(max=mc.USER_AFFILIATION_L), Optional()])

    orcid = StringField(label='ORCID (Optional)', validators=[Length(
        min=mc.USER_ORCID_L, max=19), Optional(), validate_orcid])

    google_scholar = StringField(label='Google scholar ID (Optional)', validators=[
                                 Length(max=mc.USER_GOOGLE_SCHOLAR_L),
                                 Optional()])

    about_me = TextAreaField(label='About me (Optional)', validators=[
                             Length(max=mc.USER_ABOUT_ME_L), Optional()])

    personal_website = StringField(label='Personal website (Optional)',
                                   validators=[
                                               Length(max=mc.USER_PERSONAL_WEBSITE_L),
                                               Optional()])

    review_mails_limit = SelectField(label='Limit on the number of review requests', choices=[(1, '1'),
                                              (2, '2'),
                                              (3, '3'),
                                              (4, '4'),
                                              (0, 'I don\'t want to participate in peer review')])

    notifications_frequency = SelectField(label='Frequency of notifications', choices=[(
        1, '1 day'), (3, '3 days'), (7, '1 week'),
        (14, '2 weeks'), (30, '1 month'), (0, 'Never')])

    profile_image = FileField(label='Profile image (Optional)', validators=[
                              Optional(), FileAllowed(['jpg', 'png'],
                                                      'Images only!')])

    calibration_files = MultipleFileField(label="Upload papers (PDF files) representative to your area of expertise (Optional)",
                                          validators=[FileAllowed('pdf')])


    email = StringField(label='Email address', validators=[
                        Email(), DataRequired()])

    submit = SubmitField(label='Save changes')


class InviteUserForm(FlaskForm):
    email = StringField(label='Email', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Send an invitation')


class EndorsementRequestForm(FlaskForm):

    submit_accept = SubmitField(label='Accept')
    submit_decline = SubmitField(label='Decline')



class RemarksForm(FlaskForm):

    remarks = TextAreaField(validators=[Length(max=mc.USER_REMARKS_L),
                                        Optional()])
    submit = SubmitField(label='Save remarks')
