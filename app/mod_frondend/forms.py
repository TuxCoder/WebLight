from flask_wtf import Form
from wtforms import SelectField, IntegerField, StringField
from wtforms.validators import DataRequired, NumberRange

from ..animation import animations


class AnimationForm(Form):
    animation = SelectField(
        "Animation",
        choices=dict(zip(list(animations.keys()), list(animations.keys()))).items(),
        validators=[DataRequired()])
    size = IntegerField(
        "Size",
        default=1,
        validators=[NumberRange(min=0)])
    speed = IntegerField(
        "Speed",
        default=1)
    color = StringField(
        "Color",
        default="#FFFFFF")

    def __init__(self, *args, **kwargs):
        """
        Initiates a new user form object
        :param args: Python default
        :param kwargs: Python default
        """
        Form.__init__(self, *args, **kwargs)
        self.csrf_enabled = False
