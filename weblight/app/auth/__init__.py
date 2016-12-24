from flask import Blueprint

mod_auth = Blueprint("auth", __name__)
mod_auth_rest = Blueprint("auth_rest", __name__, url_prefix="/api")

from . import views, admin, rest  # noqa
