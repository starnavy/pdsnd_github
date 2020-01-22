from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired
from flask import request

class FilterForm(FlaskForm):
    user_name = StringField('Name', validators=[InputRequired(message="What do you prefer to be called?")])

    cities = [('All Cities', ''), ('Chicago', 'Chicago'), ('New York City', 'New York City'), ('Washington', 'Washington')]
    choose_cities = SelectField(choices = cities, default = ['0'])

    months = [('All Months',''), ('January', 'January'), ('February', 'February'), ('March', 'March'), ('April', 'April'),
   ('May', 'May'), ('June', 'June') ]
    choose_months = SelectField(choices = months, default = ['0'])

    day_of_week = [('All Days',''), ('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
   ('Friday', 'Friday'), ('Saturday', 'Saturday'), ('Sunday', 'Sunday') ]
    choose_days = SelectField(choices = day_of_week, default = ['0'])

    submit = SubmitField('Submit!')

    confirm = SubmitField('Confirm!')
