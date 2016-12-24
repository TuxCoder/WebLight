"""Utility constants and functions."""

from flask import flash
import struct
import codecs


def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash("Error in {}: {}".format(
                getattr(form, field).label.text,
                error), "error")


class Color:
    @staticmethod
    def hex2rgb(hex):
        return struct.unpack('BBB', codecs.decode(hex, 'hex'))

    @staticmethod
    def rgb2hex(rgb):
        codecs.encode(struct.pack('BBB', *rgb), 'hex')
