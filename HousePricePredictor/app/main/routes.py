from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.main.forms import PredictForm, EditProfileForm
from app.models import db, User  # добави User, за да ползваме методи на модела

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Старата парола е грешна.', 'danger')
            return render_template('main/edit_profile.html', form=form)

        current_user.username = form.username.data
        current_user.set_password(form.new_password.data)  # хеширане на новата парола
        db.session.commit()
        flash('Профилът беше обновен успешно.', 'success')
        return redirect(url_for('ai.predict'))

    form.username.data = current_user.username
    return render_template('main/edit_profile.html', form=form)
