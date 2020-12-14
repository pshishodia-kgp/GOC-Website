from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField, FieldList,FormField

from wtforms.validators import DataRequired, Length

class ShortlistingRound(FlaskForm):
    company_name = StringField('Company Name')
    content = StringField('Content')
class InterveiwRound(FlaskForm):
    company_name = StringField('Company Name')
    content = StringField('Content')
class BlogForm(FlaskForm):
    id = StringField('BlogID',
                        validators = [DataRequired()])
    title = StringField('Title', validators = [DataRequired()]) 
    content = StringField('Content',
                            validators = [DataRequired()])
    shortlisting_content = StringField('ShortlistingContent')
    shortlisting_rounds = FieldList(FormField(ShortlistingRound) )
    interview_content = StringField('InterveiwContent')
    interview_rounds = FieldList(FormField(InterveiwRound) )    
    tags = FieldList(StringField('Tag',validators = [DataRequired()]),min_entries = 1)
    author = StringField('Author' , validators = [DataRequired(),Length(min=2)]) 
    addTag = SubmitField('Add Another Tag')   
    addShortListing = SubmitField('Add Company for shortlisting rounds')
    addInterview = SubmitField('Add Company for interview rounds')
    submit = SubmitField('Add Blog')
