import os
from bibliopixel.drivers.visualizer import DriverVisualizer
from bibliopixel.drivers.dummy_driver import DriverDummy
from bibliopixel.led import *
from bibliopixel.drivers.LPD8806 import *

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    from app.leds import Device

    DEVICES = {
        'light': Device(name='light', leds=list(reversed(range(0, 26)))),
        'printer': Device(name='printer', leds=[26, 27, 30, 31, 28, 29]),
    }

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
        driver = DriverLPD8806(32, c_order=ChannelOrder.BRG, use_py_spi="/dev/spidev0.0")
        return LEDStrip(driver, threadedUpdate=True)

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

    @staticmethod
    def init_led():
        driver = DriverVisualizer(32)
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

