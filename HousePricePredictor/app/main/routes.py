from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import PredictionHistory, User
from app.main.forms import EditProfileForm
from app import db
import logging

main_bp = Blueprint('main', __name__)
logger = logging.getLogger(__name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()

    if request.method == 'GET':
        form.username.data = current_user.username
        form.visibility.data = 'public' if current_user.is_public else 'private'

    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.username = form.username.data
            current_user.set_password(form.new_password.data)
            current_user.is_public = True if form.visibility.data == 'public' else False
            db.session.commit()
            flash("Профилът е обновен успешно!", "success")
            return redirect(url_for('main.edit_profile'))
        else:
            flash("Грешна стара парола!", "danger")

    return render_template('main/edit_profile.html', form=form)

@main_bp.route('/prediction_history')
@login_required
def prediction_history():
    try:
        user_predictions = PredictionHistory.query.filter_by(user_id=current_user.id)\
            .order_by(PredictionHistory.timestamp.desc()).all()

        others_predictions = PredictionHistory.query\
            .join(User).filter(User.id != current_user.id, User.is_public == True)\
            .order_by(PredictionHistory.timestamp.desc()).all()

        return render_template('main/prediction_history.html',
                               predictions=user_predictions,
                               others_predictions=others_predictions)
    except Exception as e:
        logger.error(f"Error retrieving prediction history: {e}")
        flash("An error occurred while loading your prediction history.", "danger")
        return redirect(url_for('main.error'))

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    return render_template('main/contact.html')

@main_bp.route('/errors')
def error():
    return render_template('main/errors.html')
