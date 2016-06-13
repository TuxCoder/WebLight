from .extensions import app


class Device:
    def __init__(self, name='', leds=[]):
        self.name = name
        self.leds = leds
        self.anim = None
        self.brightness = 1

    def get_led(self):
        return app.config.get('LED')

    def get_leds(self):
        return self.leds

    def getName(self):
        return self.name

    def on(self):
        app.logger.debug('[Device] \'%s\' [%d] on', self.name, id(self))
        self.off()
        for i in self.leds:
            self.get_led().setRGB(i, 255, 255, 255)
        self.get_led().update()

    def off(self):
        if self.anim is not None:
            app.logger.debug('[Device] stop running animation [%d]', id(self.anim))
            self.anim.stopThread(wait=True)
            self.anim = None

        for i in self.leds:
            self.get_led().setRGB(i, 0, 0, 0)
        self.get_led().update()

    def set_anim(self, anim: classmethod, fps=25, params={}):

        if app.config.get('LDE_FPS') is not None:
            fps = app.config.get('LDE_FPS')

        if self.anim is not None:
            self.off()
        self.anim = anim(device=self)
        self.anim.set_params(params=params)
        self.anim.run(fps=fps, threaded=True)

        app.logger.debug('[Device] \'%s\' [%d] start animation [%s] with %d fps', self.name, id(self), id(self.anim),
                         fps)

    def get_anim(self):
        return self.anim

    def set_brightness(self, brightness: float):
        if brightness < 0 or brightness > 1:
            raise ValueError('brightness out of range 0 <= b <=1')
        self.brightness = brightness

    def get_brightness(self):
        return self.brightness
