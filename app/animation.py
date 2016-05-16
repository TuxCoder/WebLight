from bibliopixel.animation import StripChannelTest, BaseStripAnim as OrgBaseStripAnim
from threading import Thread
import math
from .extensions import app
from .util import Color


class BaseStripAnim(OrgBaseStripAnim):
    def __init__(self, device, start=0, end=-1):
        super(BaseStripAnim, self).__init__(device.get_led(), start, end)
        self._device = device
        self._num_leds = len(self._device.get_leds())

    def __exit__(self, type, value, traceback):
        self._exit(type, value, traceback)
        self.stopThread(wait=True)
        self._led.waitForUpdate()

    def preRun(self, ant=1):
        app.logger.debug('[BaseStripAnim] run')

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
    def __init__(self, device, start=0, end=-1):
        super(Rainbow, self).__init__(device, start, end)
        self._speed = 1. / 5
        self._size = 1.

    def step(self, amt=1):
        max = 255
        pos = 0
        for i in self._device.get_leds():
            step = float(self._step * self._speed * self._num_leds)
            val = int(
                ((step % self._num_leds * self._size) + pos) *
                (1. / self._size / self._num_leds) * max %
                max)
            self._led.setHSV(i, (val, max, max))
            pos += 1

        # Increment the internal step by the given amount
        self._step += amt

    def set_options(self, args=[]):
        if 'speed' in args:
            self._speed = float(args.get('speed'))
        if 'size' in args:
            self._size = float(args.get('size'))


class NightRider(BaseStripAnim):
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
        max = 255

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

    def get_options(self):
        return {
            'speed': self._speed,
            'color': '#' + Color.rgb2hex(self._color)
        }

    def set_options(self, args={}):
        if 'speed' in args:
            self._speed = float(args.get('speed'))
        if 'color' in args:
            color = args.get('color')
            (r, g, b) = Color.hex2rgb(color[1:])
            self._color = (r / 255., g / 255., b / 255.)


class EU(BaseStripAnim):
    def __init__(self, device, start=0, end=-1):
        super(EU, self).__init__(device, start, end)
        self._speed = 1.
        self._width = 1.
        self._yellow = (255, 255, 0)
        self._blue = (0, 0, 255)

    def step(self, amt=1):
        max = 255
        pos = 0
        for i in self._device.get_leds():

            if math.floor((self._step * self._speed * self._width + i) / self._width) % 2 == 0:
                self._led.setRGB(i, 255, 255, 0)
            else:
                self._led.setRGB(i, 0, 0, 255)
            pos += 1
        # Increment the internal step by the given amount
        self._step += amt

    def set_options(self, args=[]):
        if 'speed' in args:
            self._speed = float(args.get('speed'))
        if 'size' in args:
            self._width = float(args.get('size'))


class Stroposcope(BaseStripAnim):
    def __init__(self, device, start=0, end=-1):
        super(Stroposcope, self).__init__(device, start, end)
        self._speed = 1. / 5
        self._color = (1, 1, 1)

    def step(self, amt=1):
        max = 255
        pos = 0
        (r, g, b) = self._color

        for i in self._device.get_leds():
            if int(self._step * 2. * self._speed % 2) == 0:
                max = 0
            else:
                max = 255
            self._led.setRGB(i, int(max * r), int(max * g), int(max * b))
            pos += 1

        # Increment the internal step by the given amount
        self._step += amt

    def set_options(self, args=[]):
        if 'speed' in args:
            self._speed = float(args.get('speed'))
        if 'color' in args:
            color = args.get('color')
            (r, g, b) = Color.hex2rgb(color[1:])
            self._color = (r / 255., g / 255., b / 255.)


animations = {
    'rainbow': Rainbow,
    'stroposcope': Stroposcope,
    'eu': EU,
    'nightrider': NightRider
}
