from flask_json import FlaskJSON
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin import Admin

admin = Admin()
debug_toolbar = DebugToolbarExtension()
json = FlaskJSON()
db = SQLAlchemy()
login_manager = LoginManager()
app = None

admin_models = []  # Add your admin models here.
admin_views = []  # Add your admin views here.