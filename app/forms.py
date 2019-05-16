from flask_wtf import FlaskForm
from wtforms import  FloatField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField, HiddenField, RadioField
from wtforms.validators import DataRequired
# from app.models import User
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional, AnyOf


class SearchForm(FlaskForm):
    stock_symbol = StringField('Enter Stock Symbol', validators=[DataRequired()])
    submit = SubmitField('Search')