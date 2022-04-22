from wtforms.fields.simple import TextAreaField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired, Optional, ValidationError
import config.models_config as mc
from wtforms.fields.html5 import DateTimeLocalField
import string
from open_science.models import Tag

class EditTagForm(FlaskForm):

    def validate_tag_name(form, name):

        for char in name.data:
            if char in string.whitespace:
                raise ValidationError("Name can not contains whitespaces")

        if form.previous_name.data is None \
                or form.previous_name.data != name.data.upper():
            tag = Tag.query.filter(Tag.name == name.data.upper()).first()
            if tag is not None:
                raise ValidationError('This tag already exists')

    name = StringField(label='Name', validators=[Length(
        max=mc.TAG_NAME_L), validate_tag_name, DataRequired()])
    description = TextAreaField(label='Description', validators=[
                                Length(max=mc.TAG_DESCRIPTION_L),
                                DataRequired()])
    deadline = DateTimeLocalField(
        label='Deadline (Optional)',
        format='%Y-%m-%dT%H:%M',
        validators=[Optional()])

    previous_name = StringField()

    submit = SubmitField(label='Create tag')
