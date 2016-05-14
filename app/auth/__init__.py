from flask import Blueprint

mod_auth = Blueprint("auth", __name__)

from . import views, admin  # noqa
