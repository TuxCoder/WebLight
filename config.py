import os
from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel.drivers.serial_driver import DriverSerial, LEDTYPE
from bibliopixel.led import *
from bibliopixel.drivers.LPD8806 import *

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    from app.leds import Device

    DEVICES = {
        'work_place': Device(name='light', leds=list(reversed(range(0, 26)))),
        'printer': Device(name='printer', leds=[26, 27, 31, 30, 29, 28]),
        'status': Device(name='status', leds=list(range(0, 18))),
    }
    LDE_FPS = 60

    SECRET_KEY = os.environ.get("SECRET_KEY") or \
                 "asdfasdgasdasdfsdfdsfasd"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = False
    DATABASE_QUERY_TIMEOUT = 0.5
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    CSRF_SESSION_KEY = "secret"

    JSON_ADD_STATUS = True
    JSON_STATUS_FIELD_NAME = 'status'

    LANGUAGES = {
        "en": "English",
        "de": "Deutsch"
    }

    LED = None

    @staticmethod
    def init_led():
        #driverA = DriverLPD8806(32, c_order=ChannelOrder.BRG, dev="/dev/spidev0.0")
        #driverB = DriverLPD8806(18, c_order=ChannelOrder.BRG, dev="/dev/spidev0.1")

        #return LEDStrip([driverA, driverB], threadedUpdate=True)
        driver = DriverDummy(50)
        # driver = DriverVisualizer(50, port=1618)
        return LEDStrip(driver, threadedUpdate=True)

    #        driver = DriverLPD8806(32, c_order=ChannelOrder.BRG, use_py_spi="/dev/spidev0.0")
    #        return LEDStrip(driver, threadedUpdate=True)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = True
    LDE_FPS = 30  # to slow visualizer

    @staticmethod
    def init_led():
        driver = DriverDummy(50)
        # driver = DriverVisualizer(50, port=1618)
        return LEDStrip(driver, threadedUpdate=True)


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    @staticmethod
    def init_led_driver():
        Config.DRIVER = DriverDummy(32)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
