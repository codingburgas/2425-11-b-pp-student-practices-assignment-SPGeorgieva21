from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class PredictForm(FlaskForm):
    size = IntegerField('Размер (m²)', validators=[DataRequired(), NumberRange(min=1)])
    rooms = IntegerField('Брой стаи', validators=[DataRequired(), NumberRange(min=1)])
    floor = IntegerField('Етаж', validators=[DataRequired(), NumberRange(min=0)])
    furnished = SelectField('Обзаведен', choices=[('yes', 'Да'), ('no', 'Не')], validators=[DataRequired()])
    city = SelectField('Град', choices=[
        ('sofia', 'София'),
        ('plovdiv', 'Пловдив'),
        ('varna', 'Варна'),
        ('burgas', 'Бургас')
    ], validators=[DataRequired()])
    submit = SubmitField('Предскажи')