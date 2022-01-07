from wtforms import StringField, SubmitField, RadioField, widgets, SelectMultipleField, TextAreaField, FieldList, TextField, FormField
from wtforms.fields.simple import HiddenField
from wtforms.validators import Length, Optional, StopValidation, DataRequired
from flask_wtf import FlaskForm
import open_science.config.models_config as mc
from open_science.models import DeclinedReason, Suggestion
from wtforms.fields.html5 import DecimalRangeField

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class CheckboxTableField(SelectMultipleField):
    widget = widgets.TableWidget(with_table_tag=False)
    option_widget = widgets.CheckboxInput()


class ReviewRequestForm(FlaskForm):

    def validate_declined_reason(form, field):
        if form.submit_decline.data:
            if not field.data:
                raise StopValidation('Choose the reason(s) for rejection')

    def validate_prepare_time(form, field):
        if form.submit_accept.data:
            if not field.data:
                raise StopValidation('Choose the time needed to prepare the review')

              
    declined_reason = MultiCheckboxField(label='Declined reason', validators=[validate_declined_reason,Optional()], coerce=int)
    other_reason_text = StringField(label='Other reason', validators=[Length(max=mc.DR_REASON_L),Optional()])
    prepare_time = RadioField(validators=[validate_prepare_time,Optional()], choices=[(7,'1 week'),(14,'2 weeks'),(21,'3 weeks'),(28,'4 weeks')])
    submit_accept = SubmitField(label='Accept')
    submit_decline = SubmitField(label='Decline')

    def __init__(self):
        super().__init__()
        self.declined_reason.choices = [(r.id-1, r.reason) for r in DeclinedReason.query.all()]




class ReviewEditForm(FlaskForm):
    
    def validate_text(form, field):
        if form.submit.data:
            if not field.data:
                raise StopValidation('Review text cannot be empty')

    def validate_no_conflict(form, field):
        if form.submit.data:
            if not field.data:
                raise StopValidation('You must declare no conflict of interest')

    evaluation_novel =  DecimalRangeField('Novel and substantial compared to previous papers by the author(s) and the existing literature', default=0)
    evaluation_conclusion = DecimalRangeField('Claims and conclusions reasonable and justified', default=0)
    evaluation_error = DecimalRangeField(' Free of essential and technical errors', default=0)
    evaluation_organize = DecimalRangeField('Well organized, well presented, readable', default=0)
    confidence = DecimalRangeField('How confident I am', default=0)

    suggestionsField = HiddenField()

    check_no_conflict = CheckboxTableField(label='I state that I have no conflict of interest',choices=[(True,'')],validators=[validate_no_conflict,Optional()],coerce=bool)
    check_anonymous = CheckboxTableField(label='I want my review to be anonymous (you will be visible as "ReviewerX")', choices=[(True,'')],validators=[Optional()],coerce=bool)

    submit = SubmitField(label='Send')
    save = SubmitField(label='Save')