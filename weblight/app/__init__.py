import logging
from logging.handlers import RotatingFileHandler
import traceback
from flask import Flask

# Load modules for flask-admin
from . import auth  # noqa

from .extensions import db, login_manager, admin_models, admin_views, admin, debug_toolbar, pagedown, csrf, api


def create_app(config_name='default'):
    app = Flask(__name__)
    extensions.app = app
    from config import config
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.config['LED'] = config[config_name].init_led()

    register_loghandler(app)
    register_extensions(app)
    register_blueprints(app)

    if app.debug:
        @app.errorhandler(Exception)
        def exception_handler(error):
            traceback.print_exc()
            return "!!!!" + repr(error)
    return app


def register_loghandler(app):
    handler = RotatingFileHandler('logs/dev.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(
    #     "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    # handler.setFormatter(formatter)

    app.logger.addHandler(handler)


def register_extensions(app):
    db.init_app(app)

    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    pagedown.init_app(app)
    # migrate.init_app(app, db)
    # babel.init_app(app)
    for model in admin_models:
        admin.add_view(model[1](model[0], db.session))
    for view in admin_views:
        admin.add_view(view)
    admin.init_app(app)
    csrf.init_app(app)
    return None


def register_blueprints(app):
    from app.mod_rest import api_bp
    app.register_blueprint(api_bp)

    from app.mod_frondend.controllers import mod_frontend as frontend_module
    app.register_blueprint(frontend_module)

    from app.auth import mod_auth as auth_module, mod_auth_rest as auth_rest_module
    app.register_blueprint(auth_module)
    app.register_blueprint(auth_rest_module)

    # from .admin import admin as admin_blueprint
    # app.register_blueprint(admin_blueprint, url_prefix="/admin")

    return None
