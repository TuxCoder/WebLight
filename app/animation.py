from bibliopixel.animation import StripChannelTest, BaseStripAnim as OrgBaseStripAnim
from bibliopixel.animation import colors
import math
from copy import copy
from .extensions import app
from .util import Color
from flask_json import json_response


class ParamType(object):
    type = None
    value = None

    def __init__(self, value=None):
        self.value = value


class FloatType(ParamType):
    type = 'float'
    min = None
    max = None
    step = None

    def __init__(self, value=None, min=None, max=None, step=None):
        super().__init__(value)
        self.min = min
        self.max = max
        self.step = step


class RangeType(FloatType):
    type = 'range'

    def __init__(self, value=None, min=None, max=None, step=None):
        super().__init__(value, min, max, step)


class ColorType(ParamType):
    type = 'color'


class BaseStripAnim(OrgBaseStripAnim):
    name = None
    params = {
        'brightness': RangeType(value=1, min=0, max=1, step=0.01)
    }

    def __init__(self, device, start=0, end=-1):
        super(BaseStripAnim, self).__init__(device.get_led(), start, end)
        self._device = device
        self._num_leds = len(self._device.get_leds())

    def __exit__(self, type, value, traceback):
        self._exit(type, value, traceback)
        self.stopThread(wait=True)
        self._led.waitForUpdate()

    def preRun(self, amt=1):
        app.logger.debug('[BaseStripAnim] run')
        # prefent turning off all lights
        # super(BaseStripAnim, self).preRun(amt)

    def get_options(self):
        return []

    def set_options(self, args=[]):
        return

    def run(self, amt=None, fps=None, sleep=None, max_steps=0, untilComplete=False, max_cycles=0, threaded=False,
            joinThread=False, callback=None, seconds=None):
        if amt is None and fps is not None:
            amt = 1. / fps
        super(BaseStripAnim, self).run(amt=amt, fps=fps, sleep=sleep, max_steps=max_steps, untilComplete=untilComplete,
                                       max_cycles=max_cycles, threaded=threaded, joinThread=joinThread,
                                       callback=callback, seconds=seconds)


class Rainbow(BaseStripAnim):
    name = 'rainbow'
    params = dict(dict(speed=FloatType(), size=FloatType()), **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(Rainbow, self).__init__(device, start, end)
        self._cache = []

    def preRun(self, amt=1):
        super(Rainbow, self).preRun(amt)
        self._fill_cache(amt)

    def _fill_cache(self, amt=1):
        fps = 1 / amt
        # caching of values requires O(n) ram
        steps = len(self._device.get_leds()) * self._size / self.params['speed'].value * fps
        steps = int(steps + .5)
        for i in range(0, steps):
            val = int(i / steps * 255 + .5)  # round hack
            color = colors.hsv2rgb((val, 1, self.params['brightness'].value))
            if len(self._cache) < i:
                self._cache[i] = color
            else:
                self._cache.append(color)

    def step(self, amt=1):

        fps = 1 / amt

        step = self._step * self._num_leds
        pos = 0
        for i in self._device.get_leds():
            tmp = self._cache[(step + int(pos * fps + .5)) % len(self._cache)]
            print(tmp)
            (r, g, b) = tmp
            self._led.setRGB(i, r, g, b)
            pos += 1

        # Increment the internal step by the given amount
        self._step += amt


class NightRider(BaseStripAnim):
    name = 'nightrider'
    params = dict(dict(speed=FloatType(value=1), size=FloatType(value=1), color=ColorType(value="#FFFFF")),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(NightRider, self).__init__(device, start, end)
        self._speed = 1.
        self._color = (1, 1, 1)

        self._animations = [
            {
                'f': lambda x: math.sin(x) / 2. + .5,
                'rgb': lambda x: (1., 1., 1.)
            }
        ]

    def step(self, amt=1):
        brightness = self.params['brightness'].value
        max = int(255 * brightness + .5)

        # turn all leds off
        leds = self._device.get_leds()
        for i in leds:
            self._led.setRGB(i, 0, 0, 0)

        for a in self._animations:
            x = self._step * self._speed
            pos = float(a['f'](x) * (self._num_leds - 1))
            (r, g, b) = a['rgb'](x)
            (_r, _g, _b) = self._color
            (r, g, b) = (r * _r, g * _g, b * _b)

            first = math.floor(pos)
            second = (first + 1) % self._num_leds
            value = pos % 1
            valueN = 1 - value

            value *= max
            valueN *= max

            self._led.setRGB(leds[int(first)], int(r * valueN), int(g * valueN), int(b * valueN))
            self._led.setRGB(leds[int(second)], int(r * value), int(g * value), int(b * value))

        # Increment the internal step by the given amount
        self._step += amt


class EU(BaseStripAnim):
    name = 'eu'
    params = dict(dict(speed=FloatType(value=1), size=FloatType(value=1)),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(EU, self).__init__(device, start, end)
        self._yellow = (255, 255, 0)
        self._blue = (0, 0, 255)

    def step(self, amt=1):
        brightness = self.params['brightness'].value
        speed = self.params['speed'].value
        size = self.params['size'].value
        max = int(255 * brightness + .5)

        pos = 0
        for i in self._device.get_leds():

            if math.floor((self._step * speed * size + i) / size) % 2 == 0:
                self._led.setRGB(i, 255, 255, 0)
            else:
                self._led.setRGB(i, 0, 0, 255)
            pos += 1
        # Increment the internal step by the given amount
        self._step += amt


class Stroposcope(BaseStripAnim):
    name = 'stroposcope'
    params = dict(dict(speed=FloatType(value=1), color=ColorType(value=1)),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(Stroposcope, self).__init__(device, start, end)

    def step(self, amt=1):
        brightness = self.params['brightness'].value
        speed = self.params['speed'].value
        color = self.params['color'].value
        (r, g, b) = colors.hex2rgb(color)

        if int(self._step * 2. * speed % 2) == 0:
            brightness = 0

        (r, g, b) = (int(brightness * r + .5), int(brightness * g + .5), int(brightness * b + .5))

        for i in self._device.get_leds():
            self._led.setRGB(i, r, g, b)

        # Increment the internal step by the given amount
        self._step += amt

    def set_options(self, args=[]):
        super(Stroposcope, self).set_options(args)
        if 'speed' in args:
            self._speed = float(args.get('speed'))
        if 'color' in args:
            color = args.get('color')
            (r, g, b) = Color.hex2rgb(color[1:])
            self._color = (r / 255., g / 255., b / 255.)


animation_params = {
    'text': ParamType,
    'float': FloatType,
    'range': RangeType,
    'color': ColorType
}

animations = {
    'rainbow': Rainbow,
    'stroposcope': Stroposcope,
    'eu': EU,
    'nightrider': NightRider
}
