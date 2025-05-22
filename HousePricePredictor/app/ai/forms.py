from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class PredictForm(FlaskForm):
    size = FloatField('Size (sq ft)', validators=[DataRequired()])
    rooms = IntegerField('Number of Rooms', validators=[DataRequired()])
    submit = SubmitField('Predict Price')
