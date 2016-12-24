import math
from bibliopixel.animation import colors
from . import BaseStripAnim, FloatType, ColorType


class NightRider(BaseStripAnim):
    name = 'nightrider'
    params = dict(dict(speed=FloatType(value=1), size=FloatType(value=1), color=ColorType(value="#FFFFFF")),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(NightRider, self).__init__(device, start, end)

        self._animations = [
            {
                'f': lambda x: math.sin(x) / 2. + .5,
                'rgb': lambda x: (1., 1., 1.)
            }
        ]
        self._speed = 1
        self._color = (1, 1, 1)
        self._params_updated()

    def _params_updated(self):
        brightness = self._params['brightness'].get_value()
        self._speed = self._params['speed'].get_value()
        color = self._params['color'].get_value()
        (r, g, b) = colors.hex2rgb(color)
        self._color = (r * brightness, g * brightness, b * brightness)

    def step(self, amt=1):

        # turn all leds off
        leds = self._device.get_leds()
        for i in leds:
            self._led.setRGB(i, 0, 0, 0)

        for a in self._animations:
            x = self._step
            pos = float(a['f'](x) * (self._num_leds - 1))
            (r, g, b) = a['rgb'](x)
            (_r, _g, _b) = self._color
            (r, g, b) = (r * _r, g * _g, b * _b)

            first = math.floor(pos)
            second = (first + 1) % self._num_leds
            value = pos % 1
            valueN = 1 - value

            self._led.setRGB(leds[int(first)], int(r * valueN), int(g * valueN), int(b * valueN))
            self._led.setRGB(leds[int(second)], int(r * value), int(g * value), int(b * value))

        # Increment the internal step by the given amount
        self._step += amt * self._speed
