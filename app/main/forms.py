from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DateField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional
from app.models import JobPosting, Resume, CoverLetter
from app import db


class JobPostingForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    location_city = StringField('City')
    location_state = StringField('State')
    updated = DateField('Date (MM-DD-YYYY)', format="%m-%d-%Y", validators=[DataRequired()])
    status = BooleanField('Applied')
    resume = FileField(
        'Resume upload (<1MB)',
        validators=[FileAllowed(upload_set=['docx', 'doc', 'pdf'], message='docx, doc, and pdf files only.')]
    )
    cover_letter = FileField(
        'Cover letter upload (<1MB)',
        validators=[FileAllowed(upload_set=['docx', 'doc', 'pdf'], message='docx, doc, and pdf files only.')]
    )
    submit = SubmitField('Add new posting')


class EditPostingForm(FlaskForm):
    company = StringField('Company', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    location_city = StringField('City')
    location_state = StringField('State')
    status = BooleanField('Applied')
    submit = SubmitField('Add new posting')


class ResumeForm(FlaskForm):
    resume = FileField(
        'Resume upload (<1MB)',
        validators=[FileAllowed(upload_set=['docx', 'doc', 'pdf'], message='docx, doc, and pdf files only.')]
    )
    submit = SubmitField('Submit')


class CoverLetterForm(FlaskForm):
    cover_letter = FileField(
        'Cover letter upload (<1MB)',
        validators=[FileAllowed(upload_set=['docx', 'doc', 'pdf'], message='docx, doc, and pdf files only.')]
    )
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search the database',
                         validators=[DataRequired(), Length(max=100, message='Max length exceeded')])
    category = SelectField('Search in:',
                           # validators=[DataRequired()],
                           # coerce=JobPosting,
                           choices=[('company', 'Company'), ('position', 'Position'),
                                    ('resume', 'Resume'), ('cover_letter', 'Cover Letter')],
                           )
    submit = SubmitField('Search')

    def filter_query(self):
        queries_dict = {
            'company': JobPosting.query.filter(JobPosting.company.ilike(f'%{self.search.data}%')),
            'position': JobPosting.query.filter(JobPosting.position.ilike(f'%{self.search.data}%')),
            'resume': Resume.query.filter(Resume.name.ilike(f'%{self.search.data}%')),
            'cover_letter': CoverLetter.query.filter(CoverLetter.name.ilike(f'%{self.search.data}%'))
        }
        if self.category.data == 'resume' or self.category.data == 'cover_letter':
            return (result.jobposting for result in queries_dict[self.category.data])
        else:
            return queries_dict[self.category.data]


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete Entry')


class NotesForm(FlaskForm):
    notes = TextAreaField('Job Notes', validators=[Optional(), Length(max=1000)])
    submit = SubmitField('Save Notes')
