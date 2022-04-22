from wtforms.fields.core import SelectField
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Length, DataRequired
import config.models_config as mc
from open_science.models import MessageTopic

class ContactStaffForm(FlaskForm):
    topic = SelectField(label='Topic')
    text = TextAreaField(label='Text', validators=[
                         Length(max=mc.MTS_TEXT_L), DataRequired()])
    submit = SubmitField(label='Send')

    def __init__(self):
        super().__init__()
        self.topic.choices = [
            (t.id, t.topic.lower().capitalize().replace('_', ' ')) for t in MessageTopic.query.all()]