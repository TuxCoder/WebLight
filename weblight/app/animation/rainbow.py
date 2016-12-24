from bibliopixel.animation import colors
from . import BaseStripAnim,FloatType


class Rainbow(BaseStripAnim):
    name = 'rainbow'
    params = dict(dict(speed=FloatType(1), size=FloatType(1)), **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(Rainbow, self).__init__(device, start, end)
        self._cache = []

    def preRun(self, amt=1):
        super(Rainbow, self).preRun(amt)
        self._fill_cache(self._amt)

    def _fill_cache(self, amt):
        fps = 1 / amt

        # caching of values requires O(n) ram
        new_cache = {}
        steps = len(self._device.get_leds()) * fps * self._size
        steps = int(steps + .5)
        for i in range(0, steps):
            val = int(i / steps * 255 + .5)
            color = colors.hsv2rgb((val, 255, int(255 * self._brightness)))
            new_cache[i] = color

        self._cache = new_cache

    def _params_updated(self):
        super()._params_updated()

        self._speed = self._params['speed'].get_value()
        self._size = self._params['size'].get_value()

        self._fill_cache(self._amt)

    def step(self, amt=1):

        fps = 1 / amt
        cache = self._cache

        step = self._step * self._num_leds
        pos = 0
        for i in self._device.get_leds():
            (r, g, b) = cache[int(step + int(pos * fps + .5)) % len(cache)]
            self._led.setRGB(i, r, g, b)
            pos += 1

        # Increment the internal step by the given amount
        self._step += amt * self._speed
