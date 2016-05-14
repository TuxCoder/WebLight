# Import flask dependencies
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for
from flask.ext.login import login_required
from .forms import AnimationForm
from ..extensions import app

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_frontend = Blueprint('frontend', __name__, url_prefix='/')


@mod_frontend.route('/', methods=['GET'])
@login_required
def index():
    form = AnimationForm()
    devices = app.config.get('DEVICES')
    return render_template('index.html', devices=devices, form=form)
