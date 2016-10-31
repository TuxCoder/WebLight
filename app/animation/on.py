from bibliopixel.animation import colors
from . import BaseStripAnim, ColorType


class ON(BaseStripAnim):
    name = 'on'
    params = dict(dict(color=ColorType(value="#FFFFFF")),
                  **BaseStripAnim.params)

    def __init__(self, device, start=0, end=-1):
        super(ON, self).__init__(device, start, end)

    def _params_updated(self):
        brightness = self._params['brightness'].get_value()
        color = self._params['color'].get_value()
        (r, g, b) = colors.hex2rgb(color)
        self._color = (int(brightness * r + .5), int(brightness * g + .5), int(brightness * b + .5))

        (r, g, b) = self._color
        for i in self._device.get_leds():
            self._led.setRGB(i, r, g, b)

    def step(self, amt=1):
        # Increment the internal step by the given amount
        self._step += amt

    def run(self, amt=None, fps=None, sleep=None, max_steps=0, untilComplete=False, max_cycles=0, threaded=False,
            joinThread=False, callback=None, seconds=None):
        super().run(amt=amt, fps=None, sleep=1000, max_steps=max_steps, untilComplete=untilComplete,
                    max_cycles=max_cycles, threaded=threaded,
                    joinThread=False, callback=None, seconds=None)
