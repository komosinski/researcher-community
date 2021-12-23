from wtforms.fields.core import SelectField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional
import open_science.config.models_config as mc


class AdvancedSearchPaperForm(FlaskForm):
     #TODO: #Posiuu complete this form
    search_text = StringField(label='Search text', validators=[Length(max=63),Optional()])
    title = StringField(label='Title', validators=[Length(max=63),Optional()])
    description =  StringField(label='Abstract', validators=[Length(max=63),Optional()])
    author =  StringField(label='Author', validators=[Length(max=63),Optional()])
    text =  StringField(label='Text', validators=[Length(max=63),Optional()])
    per_page = SelectField(label='Rows per page', choices=[(10,'10'),(30,'30'),(50,'50'),(100,'100')])

    submit_paper = SubmitField(label='Search for papers')  
    
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AdvancedSearchPaperForm, self).__init__(*args, **kwargs)


class AdvancedSearchUserForm(FlaskForm):
     #TODO: #Posiuu complete this form
    search_text = StringField(label='Search text', validators=[Length(max=63),Optional()])
    orcid = StringField(label='ORCID(Optional)', validators=[Length(max=19),Optional()])
    submit_user = SubmitField(label='Search for users')  
    per_page = SelectField(label='Rows per page', choices=[(10,'10'),(30,'30'),(50,'50'),(100,'100')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AdvancedSearchUserForm, self).__init__(*args, **kwargs)
    
class AdvancedSearchTagForm(FlaskForm):
     #TODO: #Posiuu complete this form
    search_text = StringField(label='Search text', validators=[Length(max=63),Optional()])
    submit_tag = SubmitField(label='Search for tags')  
    per_page = SelectField(label='Rows per page', choices=[(10,'10'),(30,'30'),(50,'50'),(100,'100')])

    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(AdvancedSearchTagForm, self).__init__(*args, **kwargs)
    
class ContactStaffForm(FlaskForm):
     topic = SelectField(label='Topic', choices=[('Endorsement','Endorsement'),('Technical issues','Technical issues, corrections'),('Other','Other')])
     text = TextAreaField(label='Text', validators=[Length(max=mc.MTS_TEXT_L),DataRequired()])
     submit = SubmitField(label='Send')