"""Routes for the auth blueprint."""

from flask import abort, flash, redirect, render_template, request, url_for
from flask.ext.login import (current_user, login_required, login_user,
                             logout_user)

from . import mod_auth
from ..models.auth import User
from ..util import flash_form_errors
from .forms import ChangePasswordForm, LoginForm


@mod_auth.route("/login", methods=["GET", "POST"])
def login():
    """Login form.

    Validates login parameter after POST request.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=form.login_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            return redirect(next or url_for("frontend.index"))

        flash("Invalid username or password.", "error")

    return render_template("auth/login.html", form=form)


@mod_auth.route("/logout")
@login_required
def logout():
    """Log out the user.

    This route has no viewable content.
    """
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))


@mod_auth.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile

    Shows user details and provides formulars to change fields.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.current_password.data):
            current_user.password = form.new_password.data
            return redirect(url_for("auth.logout"))
        else:
            flash("Your current password does not match", "error")
    else:
        flash_form_errors(form)

    return render_template("auth/profile.html", user=current_user, form=form)


@mod_auth.route("/user/<int:user_id>")
def user(user_id):
    """Profile page for the current user.

    The user is picked by his matriculation number as route parameter.
    """
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)
