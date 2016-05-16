from .extensions import app

class Device:
    def __init__(self, name='', leds=[]):
        self._name = name
        self._leds = leds
        self._anim = None

    def get_led(self):
        return app.config.get('LED')

    def get_leds(self):
        return self._leds

    def getName(self):
        return self._name

    def on(self):
        app.logger.debug('[Device] \'%s\' [%d] on', self._name, id(self))
        self.off()
        for i in self._leds:
            self.get_led().setRGB(i, 255, 255, 255)
        self.get_led().update()

    def off(self):
        if self._anim is not None:
            app.logger.debug('[Device] stop running animation [%d]', id(self._anim))
            self._anim.stopThread(wait=True)
            app.logger.info('stoped? %d', self._anim.stopped())
            self._anim = None

        for i in self._leds:
            self.get_led().setRGB(i, 0, 0, 0)
        self.get_led().update()

    def set_anim(self, anim: classmethod, fps=25, args=[]):

        if app.config.get('LDE_FPS') is not None:
            fps = app.config.get('LDE_FPS')

        if self._anim is not None:
            self.off()
        self._anim = anim(device=self)
        self._anim.set_options(args=args)
        self._anim.run(fps=fps, threaded=True)

        app.logger.debug('[Device] \'%s\' [%d] start animation [%s] with %d fps', self._name, id(self), id(self._anim),fps)
