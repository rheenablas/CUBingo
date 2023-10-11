from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired 

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[InputRequired()])
    submit = SubmitField('Submit')