# Import flask dependencies
from flask import Blueprint, render_template, Response
from ..extensions import app

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_frontend = Blueprint('frontend', __name__, url_prefix='/')


@mod_frontend.route('/', methods=['GET'])
def index():
    return app.send_static_file('index.html')

@mod_frontend.route('styles/<file>', methods=['GET'])
def styles(file):
    return app.send_static_file('styles/'+file)

@mod_frontend.route('scripts/<file>', methods=['GET'])
def scripts(file):
    return app.send_static_file('scripts/'+file)

@mod_frontend.route('csrf.js', methods=['GET'])
def csrf():
    return Response(render_template("csrf.js"), mimetype='application/json')
