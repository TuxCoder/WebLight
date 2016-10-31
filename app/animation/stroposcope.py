from bibliopixel.animation import colors

from . import BaseStripAnim, FloatType, ColorType


class Stroposcope(BaseStripAnim):
    name = 'stroposcope'
    params = dict(dict(speed=FloatType(value=1), color=ColorType(value="#FFFFFF")),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(Stroposcope, self).__init__(device, start, end)

    def _params_updated(self):
        brightness = self._params['brightness'].get_value()
        self._speed = self._params['speed'].get_value()
        color = self._params['color'].get_value()
        (r, g, b) = colors.hex2rgb(color)
        self._color = (int(brightness * r + .5), int(brightness * g + .5), int(brightness * b + .5))

    def step(self, amt=1):

        if int(self._step * 2. % 2) == 0:
            (r, g, b) = self._color
        else:
            (r, g, b) = (0, 0, 0)

        for i in self._device.get_leds():
            self._led.setRGB(i, r, g, b)

        # Increment the internal step by the given amount
        self._step += amt * self._speed
