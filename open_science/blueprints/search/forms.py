from wtforms.fields.core import SelectField, BooleanField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Optional


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
    second_name = StringField(label='Last name', validators=[
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
