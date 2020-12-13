from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField, FieldList,FormField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class ShortlistingRound:
    company_name = StringField('Company Name',
                                 validators = [DataRequired(),Length(min=2)])
    content = StringField('Content',
                                 validators = [DataRequired(),Length(min=2)])
class InterveiwRound:
    company_name = StringField('Company Name',
                                 validators = [DataRequired(),Length(min=2)])
    content = StringField('Content',
                                 validators = [DataRequired(),Length(min=2)])
class BlogForm(FlaskForm):
    id = IntegerField('BlogID',
                        validators = [DataRequired()])
    content = StringField('Content',
                            validators = [DataRequired()])
    shortlisting_content = StringField('ShortlistingContent')
    shortlisting_rounds = FieldList(FormField(ShortlistingRound),min_entries = 1 )
    interveiw_content = StringField('InterveiwContent')
    interveiw_rounds = FieldList(FormField(InterveiwRound),min_entries = 1 )
    published_at = DateTimeLocalField('Published At',format = '%d/%m/%y',
                                      validators = [DataRequired()])
    tags = FieldList(StringField('Tag',validators = [DataRequired()]),min_entries = 1)
    author = StringField('Author' , validators = [DataRequired(),Length(min=2)])    
    submit = SubmitField('Add Blog')
