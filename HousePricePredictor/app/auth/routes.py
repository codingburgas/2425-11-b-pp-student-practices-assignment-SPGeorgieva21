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
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken.')
            return redirect(url_for('auth.register'))

        user = User(
            username=form.username.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.home'))

    return render_template('auth/register.html', form=form)  # <-- правилен път

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        flash("Успешен вход!", "success")
        return redirect(url_for('main.dashboard'))  # или друга страница

    return render_template('auth/login.html', form=form)