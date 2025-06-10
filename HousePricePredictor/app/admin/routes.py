from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Prediction, Model
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Нямате достъп до тази страница.', 'danger')
        return redirect(url_for('main.index'))

    total_users = User.query.count()
    total_predictions = Prediction.query.count()
    total_models = Model.query.count()
    users = User.query.all()  # <-- Добавено

    return render_template('admin/dashboard.html',
                           total_users=total_users,
                           total_predictions=total_predictions,
                           total_models=total_models,
                           users=users)  # <-- Добавено

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('Нямате достъп до тази страница.', 'danger')
        return redirect(url_for('main.index'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')

        if username:
            user.username = username
        if role:
            user.role = role

        db.session.commit()

        flash('Потребителят беше обновен успешно.', 'success')
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin/edit_user.html', user=user)
