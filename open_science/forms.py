from flask_wtf.file import FileAllowed, FileRequired
from wtforms.fields.core import SelectField, BooleanField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,\
     FormField, FieldList
from wtforms.fields.simple import FileField, HiddenField
from wtforms.validators import Length, DataRequired, Optional, StopValidation
import config.models_config as mc
from open_science.models import MessageTopic, Suggestion
from open_science import strings as STR

def validate_review(form, field):
    if form.review_declaration.data:
        if not field.data:
            raise StopValidation("You need to provide a confidence level \
                if you want your paper reviewed")


class TemplateReviewAnswer(FlaskForm):
    answer = TextAreaField(label='Your answer',
                           validators=[Optional(),
                                       Length(max=mc.S_SUGGESTION_L)])
    suggestion_id = HiddenField()
    


class PaperRevisionUploadForm(FlaskForm):
    # TODO: add valid max version from config
    file = FileField("Paper PDF", validators=[FileRequired(),
                                              FileAllowed(['pdf'])])
    anonymousFile = FileField("Anonymous version (optional)",
                              validators=[FileAllowed(['pdf'])])

    anonymity_declaration = \
        BooleanField("I certify that this version is anonymized")
    review_declaration = BooleanField("I would like this paper reviewed")

    confidence_level = \
        SelectField("Choose review confidence level:",
                    choices=[(2, 'low'), (3, 'medium'), (4, 'high')],
                    validators=[validate_review, Optional()])

    changes = HiddenField()

    suggestion_answers = FieldList(FormField(TemplateReviewAnswer),
                                   min_entries=0,
                                   validators=[Optional()])

    submitbtn = SubmitField("Upload")


class CommentForm(FlaskForm):
    content = TextAreaField("Add comment",
                            validators=[DataRequired(),
                                        Length(max=mc.COMMENT_TEXT_L)]
                            )
    refObjectType = HiddenField()
    refObjectID = HiddenField()
    comment_ref = HiddenField()
    submit_comment = SubmitField("Publish comment")


class FileUploadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    file = FileField("Paper PDF",
                     validators=[FileRequired(), FileAllowed(['pdf'])])
    anonymousFile = FileField("Anonymous version (optional)",
                              validators=[FileAllowed(['pdf'])])
    description = TextAreaField("Abstract", validators=[DataRequired()])
    changes = TextAreaField("Changes since last version")
    license = SelectField("License", coerce=int)

    rights_declaration = \
        BooleanField(STR.DECLARATION_RIGHTS, validators=[DataRequired()])
    authors_declaration = BooleanField(STR.DECLARATION_AUTHORS,
                                       validators=[DataRequired()])
    interest_conflict_declaration = BooleanField(STR.DECLARATION_NO_INTEREST_CONFLICT,
                                                 validators=[DataRequired()])
    anonymity_declaration = BooleanField(STR.DECLARATION_ANONYMITY)
    review_declaration = BooleanField(STR.DECLARATION_REVIEW)

    confidence_level = SelectField("Choose review confidence level:", choices=[(2, 'low'), (3, 'medium'), (4, 'high')], validators=[validate_review, Optional()])

    coauthors = HiddenField(id="coauthors-input-field")
    tags = HiddenField(id="tags-input-field")

    submitbtn = SubmitField("Upload")

    # c = HiddenField()


class AdvancedSearchPaperForm(FlaskForm):
    title = StringField(label='Title', validators=[Length(max=63), Optional()])
    author = StringField(label='Author', validators=[
                         Length(max=63), Optional()])
    text = StringField(label='Text', validators=[Length(max=63), Optional()])
    tag = StringField(label='Tag', validators=[Length(max=63), Optional()])

    per_page = SelectField(label='Rows per page', choices=[
                           (10, '10'), (30, '30'), (50, '50'), (100, '100')])
    show_all = BooleanField(label='Show all revisions?')

    submit_paper = SubmitField(label='Search for papers')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AdvancedSearchPaperForm, self).__init__(*args, **kwargs)


class AdvancedSearchUserForm(FlaskForm):
    first_name = StringField(label='First name', validators=[
                             Length(max=63), Optional()])
    second_name = StringField(label='Second name', validators=[
                              Length(max=63), Optional()])
    affiliation = StringField(label='Affiliation', validators=[
                              Length(max=127), Optional()])
    orcid = StringField(label='ORCID', validators=[Length(max=19), Optional()])
    tag = StringField(label='Tag', validators=[Length(max=63), Optional()])

    per_page = SelectField(label='Rows per page', choices=[
                           (10, '10'), (30, '30'), (50, '50'), (100, '100')])

    submit_user = SubmitField(label='Search for users')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AdvancedSearchUserForm, self).__init__(*args, **kwargs)


class AdvancedSearchTagForm(FlaskForm):
    name = StringField(label='Name', validators=[Length(max=63), Optional()])
    description = StringField(label='Description', validators=[
                              Length(max=63), Optional()])

    per_page = SelectField(label='Rows per page', choices=[
                           (10, '10'), (30, '30'), (50, '50'), (100, '100')])

    submit_tag = SubmitField(label='Search for tags')

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AdvancedSearchTagForm, self).__init__(*args, **kwargs)


class ContactStaffForm(FlaskForm):
    topic = SelectField(label='Topic')
    text = TextAreaField(label='Text', validators=[
                         Length(max=mc.MTS_TEXT_L), DataRequired()])
    submit = SubmitField(label='Send')

    def __init__(self):
        super().__init__()
        self.topic.choices = [
            (t.id, t.topic.lower().capitalize().replace('_', ' ')) for t in MessageTopic.query.all()]