from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.fields.simple import StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class PredictForm(FlaskForm):
    size = IntegerField('Размер (m²)', validators=[DataRequired(), NumberRange(min=1)])
    rooms = IntegerField('Брой стаи', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Предскажи')
    
class EditProfileForm(FlaskForm):
    username = StringField('Нов потребител', validators=[DataRequired()])
    password = PasswordField('Нова парола', validators=[DataRequired()])
    submit = SubmitField('Запази промените')
