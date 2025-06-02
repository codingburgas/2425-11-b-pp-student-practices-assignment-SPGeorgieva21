from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.auth.forms import RegisterForm, LoginForm
from app.models import User
from app.extensions import db

auth_bp = Blueprint('auth', __name__)



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Проверка за съвпадение е направена вече от валидатора EqualTo
        # Можеш просто да вземеш паролата и да я запишеш в базата без хеширане (не се препоръчва за реален проект!)
        username = form.username.data
        password = form.password.data
        role = form.role.data

        # ... запис в базата

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # без хеширане
            login_user(user)
            flash("Успешен вход!", "success")
            return redirect(url_for('main.predict'))
        else:
            flash("Грешно потребителско име или парола.", "danger")
    return render_template('auth/login.html', form=form)
