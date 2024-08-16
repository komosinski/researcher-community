from flask_wtf import FlaskForm
from wtforms.fields.simple import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length
import config.models_config as mc

class CommentForm(FlaskForm):
    content = TextAreaField("Add comment",
                            validators=[DataRequired(),
                                        Length(max=mc.COMMENT_TEXT_L)]
                            )
    refObjectType = HiddenField()
    refObjectID = HiddenField()
    comment_ref = HiddenField()
    submit_comment = SubmitField("Publish comment")