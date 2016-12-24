"""Routes for the auth blueprint."""

from flask import abort, flash, redirect, render_template, request, url_for,jsonify
from flask.ext.login import (current_user, login_required, login_user,
                             logout_user)

from . import mod_auth_rest
from ..models.auth import User
from ..util import flash_form_errors
from .forms import ChangePasswordForm, LoginForm
from flask_json import as_json


@mod_auth_rest.route("/login", methods=["GET"])
@as_json
def loginGet():
    """Login form.
    """
    form = LoginForm()

    return dict(form=form.data)

@mod_auth_rest.route("/login", methods=["POST"])
@as_json
def loginPost():
    """Login form.
    Validates login parameter after POST request.
    """
    form = LoginForm(data=request.get_json())
    if form.validate_on_submit():
        user = User.query.filter_by(login_name=form.login_name.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            return dict() #success
        return dict(error="Invalid username or password."), 401;
    else:
        return dict(error="Bad Request"), 400;


@mod_auth_rest.route("/logout", methods=["POST"])
@login_required
@as_json
def logout():
    """Log out the user.

    This route has no viewable content.
    """
    logout_user()
    return dict();
