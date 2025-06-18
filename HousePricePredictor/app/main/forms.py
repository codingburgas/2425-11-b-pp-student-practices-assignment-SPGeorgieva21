from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.fields.simple import StringField, PasswordField
from wtforms.validators import DataRequired, NumberRange

class PredictForm(FlaskForm):
    size = IntegerField('Размер (m²)', validators=[DataRequired(), NumberRange(min=1)])
    rooms = IntegerField('Брой стаи', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Предскажи')

class EditProfileForm(FlaskForm):
    username = StringField('Нов потребител', validators=[DataRequired()])
    old_password = PasswordField('Стара парола', validators=[DataRequired()])
    new_password = PasswordField('Нова парола', validators=[DataRequired()])
    visibility = SelectField('Видимост на прогнозите', choices=[('public', 'Публичен'), ('private', 'Само аз')])
    submit = SubmitField('Запази промените')
