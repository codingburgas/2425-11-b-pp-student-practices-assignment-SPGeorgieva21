from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PredictForm(FlaskForm):
    size = IntegerField('Размер (m²)', validators=[DataRequired(), NumberRange(min=1)])
    rooms = IntegerField('Брой стаи', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Предскажи')
