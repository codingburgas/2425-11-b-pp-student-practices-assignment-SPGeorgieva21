from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PredictForm(FlaskForm):
    size = FloatField('Размер', validators=[DataRequired()])
    rooms = IntegerField('Брой стаи', validators=[DataRequired()])
    furnished = SelectField('Обзаведен', choices=[('yes', 'Да'), ('no', 'Не')], validators=[DataRequired()])
    floor = IntegerField('Етаж', validators=[DataRequired()])
    city = SelectField('Град', choices=[
        ('sofia', 'София'),
        ('plovdiv', 'Пловдив'),
        ('varna', 'Варна'),
        ('burgas', 'Бургас')
    ], validators=[DataRequired()])
    submit = SubmitField('Predict Price')
