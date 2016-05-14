# Import flask dependencies
from flask import Blueprint, request
from flask_json import as_json

from ..animation import animations
from ..extensions import app
from ..util import Color

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_rest = Blueprint('api', __name__, url_prefix='/api')


@mod_rest.route('/device', methods=['GET'])
@as_json
def device_list():
    return dict(devices=app.config.get('DEVICES').keys())


@mod_rest.route('/device/<device>/on', methods=['GET'])
@as_json
def device_on(device):
    devices = app.config.get('DEVICES')
    if device not in devices:
        return dict(), 404

    device = devices[device]

    device.on()
    return dict()


@mod_rest.route('/device/<device>/off', methods=['GET'])
@as_json
def device_off(device):
    devices = app.config.get('DEVICES')
    if device not in devices:
        return dict(), 404

    device = devices[device]

    device.off()
    return dict()


@mod_rest.route('/device/<device>/animation', methods=['GET'])
@as_json
def device_animation(device):
    devices = app.config.get('DEVICES')
    if device not in devices:
        return dict(msg='device not found'), 404
    device = devices[device]

    animation = request.args.get('animation')
    if animation not in animations:
        return dict(msg='animation not found'), 404

    args = request.args.copy()

    device.set_anim(animations[animation], args=args)

    return dict()
