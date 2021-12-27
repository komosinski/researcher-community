from wtforms import StringField, SubmitField, RadioField, widgets, SelectMultipleField, TextAreaField
from wtforms.validators import Length, Optional, StopValidation,  DataRequired
from flask_wtf import FlaskForm
import open_science.config.models_config as mc
from open_science.models import DeclinedReason
from wtforms.fields.html5 import DecimalRangeField

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
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
    other_reason = StringField(label='Other reason', validators=[Length(max=mc.DR_REASON_L),Optional()])
    prepare_time = RadioField(validators=[validate_prepare_time,Optional()], choices=[(7,'1 week'),(14,'2 weeks'),(21,'3 weeks'),(28,'4 weeks')])
    submit_accept = SubmitField(label='Accept')
    submit_decline = SubmitField(label='Decline')

    def __init__(self):
        super().__init__()
        self.declined_reason.choices = [(r.id, r.reason) for r in DeclinedReason.query.all()]

class ReviewEditForm(FlaskForm):
    
    def validate_text(form, field):
        if form.submit.data:
            if not field.data:
                raise StopValidation('Review text cannot be empty')

    text = TextAreaField(label='Your review', validators=[Length(max=mc.REVIEW_TEXT_L),validate_text, Optional()])
    
    confidence = DecimalRangeField('How confident I am', default=0)

    submit = SubmitField(label='Send')
    save = SubmitField(label='Save')