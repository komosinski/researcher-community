from wtforms import StringField, SubmitField, RadioField,\
    widgets, SelectMultipleField, TextAreaField
from wtforms.fields.core import BooleanField
from wtforms.fields.simple import HiddenField
from wtforms.validators import Length, Optional, StopValidation, DataRequired
from flask_wtf import FlaskForm
import config.models_config as mc
from open_science.models import DeclinedReason
from wtforms.fields.html5 import DecimalRangeField
from open_science import strings as STR

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
                raise StopValidation(
                    'Choose the time needed to prepare the review')

    declined_reason = MultiCheckboxField(label='Declined reason', validators=[
                                         validate_declined_reason, Optional()],
                                         coerce=int)
    other_reason_text = StringField(label='Other reason', validators=[
                                    Length(max=mc.DR_REASON_L), Optional()])
    prepare_time = RadioField(
        validators=[validate_prepare_time, Optional()],
        choices=[(7, '1 week'),
                 (14, '2 weeks'),
                 (21, '3 weeks'),
                 (28, '4 weeks'),
                 (35, '5 weeks'),
                 (42, '6 weeks')])

    submit_accept = SubmitField(label='Accept')
    submit_decline = SubmitField(label='Decline')

    def __init__(self):
        super().__init__()
        self.declined_reason.choices = [
            (r.id-1, r.reason) for r in DeclinedReason.query.all()]


class ReviewEditForm(FlaskForm):

    def validate_no_conflict(form, field):
        if form.submit.data:
            if not field.data:
                raise StopValidation(
                    'You must declare no conflict of interest')

    evaluation_novel = DecimalRangeField(STR.EVALUATION_NOVEL, default=0)
    evaluation_conclusion = DecimalRangeField(STR.EVALUATION_JUSTIFIED,
                                              default=0)
    evaluation_error = DecimalRangeField(
        STR.EVALUATION_NOERRORS, default=0)
    evaluation_organize = DecimalRangeField(
        STR.EVALUATION_WELLPRESENTED, default=0)
    evaluation_accept = BooleanField(
        STR.EVALUATION_ACCEPT,
        default=False)
    confidence = DecimalRangeField('How confident I am', default=0)

    suggestionsField = HiddenField()

    check_no_conflict = BooleanField(
        label='I state that I have no conflict of interest',
        validators=[validate_no_conflict],
        default=False)

    check_anonymous = BooleanField(
        label='I want my review to be anonymous \
            (you will be visible as "ReviewerX")',
        default=False)

    check_hide = BooleanField(
        "Hide review (You can change it whenever you want)", default=False)

    submit = SubmitField(label='Send')
    save = SubmitField(label='Save')

class CommentForm(FlaskForm):
    content = TextAreaField("Add comment",
                            validators=[DataRequired(),
                                        Length(max=mc.COMMENT_TEXT_L)]
                            )
    refObjectType = HiddenField()
    refObjectID = HiddenField()
    comment_ref = HiddenField()
    submit_comment = SubmitField("Publish comment")