from flask import (Blueprint, render_template, flash, 
                   redirect, url_for, request)
from flask_login import login_user, logout_user, current_user, login_required

from ShoppingListApp.users.models import User

from .forms import RegistrationForm, LoginForm, ResetPasswordForm


user_views = Blueprint("user_views", __name__, url_prefix="/user")


@user_views.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("site_views.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data
        user = User()
        user.username = username
        user.password = User.hash_password(password)
        user.save()
        flash(f"Account created for '{form.username.data}'.", category="success")
        return redirect(url_for("site_views.home"))
    return render_template("register.html", title="Register", form=form)


@user_views.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("site_views.home"))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data
        user = User.find_by_username(username)
        if user is None:
            flash(f"User with username '{username}' is not registered.", 'danger')
        else:
            if not user.match_password(password):
                flash("Username and password do not match!", 'danger')
            else:
                flash("Login successful!", category='success')
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next', url_for("site_views.home"))
                return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@user_views.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("site_views.home"))


@user_views.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@user_views.route("/reset_password", methods=["POST", "GET"])
@login_required
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.find_by_id(current_user.get_id())
        user.password = User.hash_password(form.password.data)
        user.save()
        flash(f"New password is set for '{user.username}'.", category="success")
        return redirect(url_for("site_views.home"))
    return render_template("reset_password.html", title="Reset Your Password", form=form)
