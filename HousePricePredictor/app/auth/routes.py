from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import RegisterForm, LoginForm
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            # Redirect to custom error page with message
            flash('Потребител с това потребителско име вече съществува.', 'danger')
            return redirect(url_for('main.error'))

        user = User(username=username, email=email, role=role)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Успешна регистрация! Моля, влезте в профила си.', 'success')
        return redirect(url_for('auth.login'))

    # If form not valid, still show form (e.g., for CSRF or field errors)
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('ai.predict'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Успешен вход!", "success")
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('ai.predict'))
        else:
            # On failed login: redirect to error page
            flash("Грешно потребителско име или парола.", "danger")
            return redirect(url_for('main.error'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
