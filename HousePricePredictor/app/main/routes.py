from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main.forms import PredictForm, EditProfileForm
from app.models import db  # ако използваш SQLAlchemy

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    form = PredictForm()
    prediction = None

    if form.validate_on_submit():
        size = form.size.data
        rooms = form.rooms.data
        prediction = size * 1000 + rooms * 5000

    return render_template('ai/predict.html', form=form, prediction=prediction)

@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = form.password.data  # TODO: хеширай паролата!
        db.session.commit()
        flash('Профилът беше обновен успешно.', 'success')
        return redirect(url_for('main.index'))  # Можеш да промениш към dashboard
    form.username.data = current_user.username
    return render_template('main/edit_profile.html', form=form)
