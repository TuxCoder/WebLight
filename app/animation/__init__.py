import logging
from bibliopixel.animation import BaseStripAnim as OrgBaseStripAnim
from copy import deepcopy
from ..extensions import app


class ParamType(object):
    type = None
    value = None

    def __init__(self, value=None, **kwargs):
        self.value = value

    def get_value(self):
        return self.value


class FloatType(ParamType):
    type = 'float'
    min = None
    max = None
    step = None

    def __init__(self, value=None, min=None, max=None, step=None, **kwargs):
        super().__init__(value, **kwargs)
        self.min = min
        self.max = max
        self.step = step

    def get_value(self):
        try:
            self.value = float(self.value)
            if self.min is not None:
                self.value = max(self.value, self.min)
            if self.max is not None:
                self.value = min(self.value, self.max)
            return self.value
        except (TypeError, ValueError):
            return 1


class RangeType(FloatType):
    type = 'range'

    def __init__(self, value=None, min=None, max=None, step=None, **kwargs):
        super().__init__(value, min, max, step, **kwargs)


class ColorType(ParamType):
    type = 'color'


class BooleanType(ParamType):
    type = 'boolean'


class BaseStripAnim(OrgBaseStripAnim):
    name = None
    params = {
        'brightness': RangeType(value=1, min=0, max=1, step=0.01)
    }

    def __init__(self, device, start=0, end=-1, logger=None):
        super(BaseStripAnim, self).__init__(device.get_led(), start, end)
        self._device = device
        self._num_leds = len(self._device.get_leds())
        self._params = deepcopy(self.params)
        self._amt = 1
        if logger is None:
            self.logger = logging.getLogger(__name__)

        self._params_updated()

    def __exit__(self, type, value, traceback):
        self._exit(type, value, traceback)
        self.stopThread(wait=True)
        self._led.waitForUpdate()

    def preRun(self, amt=1):
        app.logger.debug('[BaseStripAnim] run')
        # prefent turning off all lights
        # super(BaseStripAnim, self).preRun(amt)

    def get_params(self):
        return self._params

    def set_params(self, params):
        for name, param in params.items():
            self._params[name].value = param.value
        self._params_updated()
        return

    def _params_updated(self):
        self._brightness = self._params['brightness'].get_value()
        return

    def run(self, amt=None, fps=None, sleep=None, max_steps=0, untilComplete=False, max_cycles=0, threaded=False,
            joinThread=False, callback=None, seconds=None):
        if fps is not None:
            self._amt = 1. / fps
        super(BaseStripAnim, self).run(amt=self._amt, fps=fps, sleep=sleep, max_steps=max_steps,
                                       untilComplete=untilComplete,
                                       max_cycles=max_cycles, threaded=threaded, joinThread=joinThread,
                                       callback=callback, seconds=seconds)


from .audio_visulizer import AudioVisulizer
from .eu import EU
from .night_rider import NightRider
from .on import ON
from .rainbow import Rainbow
from .stroposcope import Stroposcope

animation_params = {
    'text': ParamType,
    'float': FloatType,
    'range': RangeType,
    'color': ColorType,
    'boolean': BooleanType
}

animations = {
    'rainbow': Rainbow,
    'stroposcope': Stroposcope,
    'eu': EU,
    'nightrider': NightRider,
    'on': ON,
    'audiovisulizer': AudioVisulizer
}
