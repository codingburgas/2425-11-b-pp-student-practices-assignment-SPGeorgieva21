from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Prediction

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    # Тук е твоята логика за редакция на профил (оставям я както е)
    pass  # замени с твоята имплементация

@main_bp.route('/prediction_history')
@login_required
def prediction_history():
    # Взимаме само прогнозите на текущия потребител
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).all()
    return render_template('main/prediction_history.html', predictions=user_predictions)

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contac.html')

