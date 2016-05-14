from flask_json import FlaskJSON
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask.ext.admin import Admin
from flask.ext.pagedown import PageDown

admin = Admin(base_template='admin_base.html', template_mode='bootstrap3')
debug_toolbar = DebugToolbarExtension()
json = FlaskJSON()
db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
app = None

admin_models = []  # Add your admin models here.
admin_views = []  # Add your admin views here.