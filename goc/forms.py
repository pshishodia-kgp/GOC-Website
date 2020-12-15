from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField, FieldList,FormField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length,ValidationError

class ShortlistingRound(FlaskForm):
    company_name = StringField('Company Name',validators = [DataRequired()])
    content = StringField('Content',validators = [DataRequired()],widget = TextArea())
class InterviewRound(FlaskForm):
    company_name = StringField('Company Name',validators = [DataRequired()])
    content = StringField('Content',validators = [DataRequired()],widget = TextArea())
class Shortlisting(FlaskForm):
    shortlisting_content = StringField('ShortlistingContent',validators = [DataRequired()],widget = TextArea())
    shortlisting_rounds = FieldList(FormField(ShortlistingRound) ,min_entries=1)
class Interview(FlaskForm):
    interview_content = StringField('InterviewContent',widget = TextArea())
    interview_rounds = FieldList(FormField(InterviewRound) )  
class BlogForm(FlaskForm):        
    title = StringField('Title', validators = [DataRequired()]) 
    content = StringField('Content',
                            validators = [DataRequired()],widget = TextArea())    
    shortlisting = FormField(Shortlisting)
    interview = FormField(Interview)      
    tags = FieldList(StringField('Tag',validators = [DataRequired()]),min_entries = 1)
    author = StringField('Author' , validators = [DataRequired(),Length(min=2)]) 
    addTag = SubmitField('Add Another Tag')   
    addShortListing = SubmitField('Add Company for shortlisting rounds')
    addInterview = SubmitField('Add Company for interview rounds')
    isSelected = SubmitField('Were You Shortlisted')
    submit = SubmitField('Add Blog')
    

