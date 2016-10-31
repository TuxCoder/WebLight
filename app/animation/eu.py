import math
from . import BaseStripAnim,FloatType


class EU(BaseStripAnim):
    name = 'eu'
    params = dict(dict(speed=FloatType(value=1), size=FloatType(value=1)),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(EU, self).__init__(device, start, end)

    def _params_updated(self):
        brightness = self._params['brightness'].get_value()
        self._speed = self._params['speed'].get_value()
        self._size = self._params['size'].get_value()
        self._max = int(255 * brightness + .5)

    def step(self, amt=1):

        pos = 0
        for i in self._device.get_leds():

            if math.floor((self._step * self._size + i) / self._size) % 2 == 0:
                self._led.setRGB(i, self._max, self._max, 0)  # yellow
            else:
                self._led.setRGB(i, 0, 0, self._max)  # blue
            pos += 1
        # Increment the internal step by the given amount
        self._step += amt * self._speed