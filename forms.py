from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length
from datetime import datetime

class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author_id = SelectField('Author', validators=[DataRequired()], coerce=int)
    year_published = IntegerField('Year Published', validators=[
        DataRequired(),
        NumberRange(min=1000, max=datetime.now().year, message="Please enter a valid year")
    ])
    catalogue_id = SelectField('Catalogue', validators=[], coerce=int)
    submit = SubmitField('Submit')

class CatalogueForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=1, max=100, message="Name must be between 1 and 100 characters")
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500, message="Description cannot exceed 500 characters")
    ])
    submit = SubmitField('Submit')