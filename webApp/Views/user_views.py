from flask import (Blueprint, render_template, flash, 
                   redirect, url_for)

from Models.User import User

from Forms.registerForm import RegistrationForm
from Forms.loginForm import LoginForm


user_views = Blueprint("user_views", __name__, url_prefix="/user")


@user_views.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data 
        password = form.password.data 
        if User.find_by_username(username) is not None:
            flash(f"User with username '{username}' is already registed.", 'danger')
        else:
            user = User()
            user.username = username
            user.password = User.hash_password(password)
            user.save()
            flash(f"Account created for '{form.username.data}'.", category="success")
            return redirect(url_for("site.home"))

    return render_template("register.html", title="Register", form=form)


@user_views.route("/login", methods=["POST", "GET"])
def login():
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
                return redirect(url_for("site.home"))
    return render_template("login.html", title="Login", form=form)
