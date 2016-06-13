from ..extensions import api

from flask_restful import Resource, fields, marshal_with, reqparse
from flask.ext.login import current_user
from flask.json import JSONEncoder
from flask import Blueprint

from ..extensions import app, api
from ..animation import animations, animation_params
from ..animation import BaseStripAnim
from ..animation import ParamType, FloatType

api_bp = Blueprint('api', __name__, url_prefix='/api')
api.init_app(api_bp)


class User(Resource):
    @marshal_with({
        'user_id': fields.Integer,
        'login_name': fields.String
    })
    def get(self):
        return current_user


class ParamItems(fields.Raw):
    def format(self, values):
        out = {}
        for k, v in values.items():
            out[k] = v.__dict__
            out[k]['type'] = v.type
        return out

    def __init__(self, alt_attribute=None, **kwargs):
        super(ParamItems, self).__init__(**kwargs)
        self.alt_attribute = alt_attribute

    def output(self, key, obj):

        value = fields.get_value(key if self.attribute is None else self.attribute, obj)

        if value is None and self.alt_attribute is not None:
            value = fields.get_value(self.alt_attribute, obj)

        if value is None:
            return self.default

        return self.format(value)


animations_fiels = {
    'name': fields.String,
    'params': ParamItems(attribute='_params', alt_attribute='params')
}


class Animations(Resource):
    @marshal_with(animations_fiels)
    def get(self):
        items = list(animations.values())
        return items


device_fields = {
    'name': fields.String,
    'animation': fields.Nested(animations_fiels, attribute='anim')
}


def animationParser(ani):
    out = {}
    out['name'] = ani['name']
    out['params'] = {}
    for name, param in ani['params'].items():
        _class = animation_params[param['type']]
        del param['type']
        out['params'][name] = _class(**param)

    return out


device_parser = reqparse.RequestParser()
device_parser.add_argument('name')
device_parser.add_argument('animation', type=animationParser)


class Device(Resource):
    @marshal_with(device_fields)
    def get(self, device_id):
        return app.config.get('DEVICES')[device_id]

    @marshal_with(device_fields)
    def post(self, device_id):
        args = device_parser.parse_args()
        device = app.config.get('DEVICES')[device_id]
        if args['animation'] == None:
            device.off()
            return device

        animation = animations[args['animation']['name']]
        if device.get_anim() is None or device.get_anim().name != animation.name:
            # animation changed
            device.set_anim(animation, params=args['animation']['params'])
            return device

        device.get_anim().set_params(args['animation']['params'])

        return device


class Devices(Resource):
    @marshal_with(device_fields)
    def get(self):
        return list(app.config.get('DEVICES').values())


api.add_resource(User, '/user')
api.add_resource(Devices, '/device')
api.add_resource(Device, '/device/<string:device_id>')
api.add_resource(Animations, '/animation')
