from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserManagementForm(FlaskForm):
    username = StringField('Потребителско име', validators=[DataRequired()])
    role = SelectField('Роля', choices=[('user', 'Потребител'), ('admin', 'Админ')], validators=[DataRequired()])
    submit = SubmitField('Запази')

class EditUserForm(FlaskForm):
    username = StringField('Потребителско име', validators=[DataRequired()])
    role = SelectField('Роля', choices=[('admin', 'Админ'), ('teacher', 'Учител'), ('student', 'Ученик')], validators=[DataRequired()])
    submit = SubmitField('Запази')