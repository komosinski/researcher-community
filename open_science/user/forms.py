from wtforms.fields.core import SelectField
from wtforms.fields.simple import TextAreaField
from open_science.models import User, Tag
from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import Length, EqualTo, Email, DataRequired, Optional, ValidationError
import re
import open_science.config.models_config as mc
import open_science.email as em
from config import Config
from flask_login import current_user
from wtforms.fields.html5 import DateField


def validate_password(form, password):
        if not re.search("[a-z]", password.data):
            raise ValidationError('The password must contain at least one lowercase character')
        elif not re.search("[A-Z]", password.data):
            raise ValidationError('The password must contain at least one uppercase character')
        elif not re.search("[0-9]", password.data):
            raise ValidationError('The password must contain at least one digit')
        elif not re.search("[^A-Za-z0-9]", password.data):
            raise ValidationError('The password must contain at least one special character')

def validate_password_with_userdata(form, password):
        if form.first_name.data.lower() in password.data.lower():
            raise ValidationError('The password can not contain your first name')
        elif form.second_name.data.lower() in password.data.lower():
            raise ValidationError('The password can not contain your second name')
        elif form.email.data.lower().split("@")[0] in password.data.lower():
            raise ValidationError('The password can not contain your email address')

def validate_email(self, email):
    user_with_email_address = User.query.filter_by(email=email.data).first()
    if user_with_email_address:
        raise ValidationError('That email address is already in use, please use a different email address')


def validate_orcid(self, orcid):
    correct = False
    if re.search(r"^[0-9]{16}$", orcid.data):
        correct = True
    elif re.search(r"^[0-9]{15}X$", orcid.data.upper()):
        correct = True
    elif re.search(r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$", orcid.data):
        correct = True
    elif re.search(r"^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}X$", orcid.data.upper()):
        correct = True
    
    if not correct:
        raise ValidationError('Invalid ORCID iD')
            
def validate_google_scholar(self, google_scholar):
    if "scholar" not in google_scholar.data.lower():
            raise ValidationError('Invalid google scholar link')

class RegisterForm(FlaskForm):

    first_name = StringField(label='First Name', validators=[Length(min=2, max=mc.USER_FIRST_NAME_L), DataRequired()])
    second_name = StringField(label='Second Name', validators=[Length(min=2, max=mc.USER_SECOND_NAME_L), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired(),validate_email])
    password = PasswordField(label='Password', validators=[Length(min=8, max=32), DataRequired(),validate_password,validate_password_with_userdata])
    password_confirm = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])

    affiliation = StringField(label='Affiliation(Optional)', validators=[Length(max=mc.USER_AFFILIATION_L),Optional()])
    orcid = StringField(label='ORCID(Optional)', validators=[Length(min=mc.USER_ORCID_L, max=19),Optional(),validate_orcid])
    google_scholar  = StringField(label='Google scholar(Optional)', validators=[Length(max=mc.USER_GOOGLE_SCHOLAR_L),Optional(),validate_google_scholar])
    about_me = TextAreaField(label='About me(Optional)', validators=[Length(max=mc.USER_ABOUT_ME_L),Optional()])
    personal_website = StringField(label='Personal website(Optional)', validators=[Length(max=mc.USER_PERSONAL_WEBSITE_L),Optional()])
    review_mails_limit = SelectField(choices=[1,2,3,4,0])
    notifications_frequency = SelectField(choices=[(1,'1 day'),(3,'3 days'),(7,'1 week'),(14,'2 weeks'),(30,'1 month'),(0,'Never')])
    profile_image = FileField(label='Profile image',validators=[Optional(),FileAllowed(['jpg', 'png'], 'Images only!')])
    
    recaptcha = RecaptchaField()
    
    submit = SubmitField(label='Create Account')

class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField(label='Sign in')

class ResendConfirmationForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email address')
        elif user.confirmed:
            raise ValidationError('Email address is already confirmed')

    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Resend confirmation email')

class AccountRecoveryForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email address')
        if user.confirmed == False:
            raise ValidationError('Email address is not confirmed')
 
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Send recovery email')


class SetNewPasswordForm(FlaskForm):
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Invalid email address')
 
    password = PasswordField(label='Password', validators=[Length(min=8, max=32), DataRequired(),validate_password])
    password_confirm = PasswordField(label='Confirm Password', validators=[EqualTo('password'), DataRequired()])

    submit = SubmitField(label='Set password')


class EditProfileForm(FlaskForm):
    def validate_email(form, field):
        if field.data != current_user.email:
            emails_limit = Config.CHANGE_MAIL_ML - em.get_emails_cout_last_days(current_user.id,'email_change',30)
            if emails_limit > 0 :
                user_with_email_address = User.query.filter_by(email=field.data).first()
                if user_with_email_address:
                    if user_with_email_address.id != current_user.id:
                        raise ValidationError('That email address is already in use, please use a different email address') 
            else: 
                raise ValidationError('Monthly limit for email change has been exceeded')
     
    first_name = StringField(label='First Name', validators=[Length(min=2, max=mc.USER_FIRST_NAME_L), DataRequired()])
    second_name = StringField(label='Second Name', validators=[Length(min=2, max=mc.USER_SECOND_NAME_L), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    affiliation = StringField(label='Affiliation (Optional)', validators=[Length(max=mc.USER_AFFILIATION_L),Optional()])
    orcid = StringField(label='ORCID (Optional)', validators=[Length(min=mc.USER_ORCID_L, max=19),Optional(),validate_orcid])
    google_scholar  = StringField(label='Google scholar (Optional)', validators=[Length(max=mc.USER_GOOGLE_SCHOLAR_L),Optional(),validate_google_scholar])
    about_me = TextAreaField(label='About me (Optional)', validators=[Length(max=mc.USER_ABOUT_ME_L),Optional()])
    personal_website = StringField(label='Personal website (Optional)', validators=[Length(max=mc.USER_PERSONAL_WEBSITE_L),Optional()])
    review_mails_limit = SelectField(choices=[1,2,3,4,0])
    notifications_frequency = SelectField(choices=[(1,'1 day'),(3,'3 days'),(7,'1 week'),(14,'2 weeks'),(30,'1 month'),(0,'Never')])
    profile_image = FileField(label='Profile image',validators=[Optional(),FileAllowed(['jpg', 'png'], 'Images only!')])


    submit = SubmitField(label='Save changes')

class InviteUserForm(FlaskForm):
    email = StringField(label='E-mail', validators=[Email(),DataRequired()])
    submit = SubmitField(label='Send an invitation')
  
class EndorsementRequestForm(FlaskForm):

    submit_accept = SubmitField(label='Accept')
    submit_decline = SubmitField(label='Decline')


def validate_tag_name(self, name):
    if not name.data.isalnum():
        raise ValidationError('Only letters and numbers without spaces')
    
    tag = Tag.query.filter(Tag.name == name.data.upper()).first()
    if tag is not None:
        raise ValidationError('This tag already exists')
    
        
class CreateTagForm(FlaskForm):
        
    name = StringField(label='Name', validators=[Length(max=mc.TAG_NAME_L), validate_tag_name,DataRequired()])
    description = TextAreaField(label='Description', validators=[Length(max=mc.TAG_DESCRIPTION_L),DataRequired()])
    deadline = DateField(label='Deadline (Optional)',format='%Y-%m-%d',validators=[Optional()])

    submit = SubmitField(label='Create tag')


class EditTagForm(FlaskForm):

    name = StringField(label='Name', validators=[Length(max=mc.TAG_NAME_L),validate_tag_name, DataRequired()])
    description = TextAreaField(label='Description', validators=[Length(max=mc.TAG_DESCRIPTION_L),DataRequired()])

    submit = SubmitField(label='Save changes')