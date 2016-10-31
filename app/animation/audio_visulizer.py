import socket
import math
from struct import *
from threading import Thread
from bibliopixel.animation import colors
from . import BaseStripAnim, RangeType, FloatType,BooleanType


class AudioVisulizer(BaseStripAnim):
    name = 'audiovisulizer'
    params = dict(dict(
        saturation=RangeType(value=1, min=0, max=1, step=0.01),
        value=FloatType(30, min=1),
        offset=FloatType(60),
        start=RangeType(value=.01, min=0, max=1, step=0.01),
        end=RangeType(value=.7, min=0, max=1, step=0.01),
        min_value=RangeType(value=.05, min=0, max=1, step=0.01),
        log=RangeType(value=False),
        color_offset=RangeType(value=0, min=0, max=1, step=0.01),
        high_pass=RangeType(value=20, step=1)),
    **BaseStripAnim.params)

    num_data = 2048

    def __init__(self, device, start=0, end=-1):
        super(AudioVisulizer, self).__init__(device, start, end)

        self.udp_data = self._prepare_data([-100.0] * self.num_data)

        self._stoped = False
        self._udp_server = Thread(target=self.udp_server)
        self._udp_server.daemon = True
        self._udp_server.start()

    def __exit__(self, type, value, traceback):
        super().__exit__(type, value, traceback)

        self._stoped = True
        self._udp_server.join()

    def udp_server(self):
        UDP_IP = "0.0.0.0"
        UDP_PORT = 9999

        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((UDP_IP, UDP_PORT))
        sock.settimeout(1)

        i = 0
        while self._stoped == False:
            size = 4
            input_size = self.num_data * 2 * size
            mtu = 1472
            data = b''
            while len(data) < input_size:
                try:
                    d, addr = sock.recvfrom(mtu)
                except socket.timeout:
                    break
                data += d
                if len(d) != mtu:
                    break

            if len(data) != input_size:
                continue

            floats = unpack('' + 'f' * self.num_data * 2, data)

            out = [-100] * self.num_data
            for i in range(self.num_data):
                out[i] = (floats[i] + floats[self.num_data * 2 - 1 - i]) / 2

            self.udp_data = self._prepare_data(out)

    def get_data(self):
        return self.udp_data

    def _prepare_data(self, data):
        src_start = int(self.num_data * self._start)
        src_end = int(self.num_data * self._end)
        src_num = src_end - src_start
        w = src_num / self._num_leds
        out = [0] * self._num_leds
        for i in range(self._num_leds):
            if self._log:
                src_from = (pow(10, i / self.num * x) - 1) / (math.pow(10, x) - 1) * src_num + src_start
                src_to = (pow(10, (i + 1) / self.num * x) - 1) / (math.pow(10, x) - 1) * src_num + src_start
            else:
                src_from = i * w + src_start
                src_to = (i + 1) * w + src_start

            pre_s = int(src_from)
            s = math.ceil(src_from)
            e = math.floor(src_to)
            post_e = math.ceil(src_to)
            post_e = min(post_e, self.num_data - 1)
            pre_s_diff = 1 - (src_from % 1)
            post_e_diff = src_to % 1
            v = data[pre_s] * pre_s_diff + sum(data[s:e]) + data[post_e] * post_e_diff
            v /= pre_s_diff + e - s + post_e_diff
            # norm value
            v = (v + self._offset + 20.0 * i / self._num_leds) / self._value
            out[i] = min(max(v, self._min_value), 1)
        return out

    def step(self, amt=1):

        data = self.get_data()

        s = int(self._saturation * 255)
        for i, led in enumerate(self._device.get_leds()):
            v = data[i]
            v = int(v * 255 * self._brightness)
            h = int(255 * (i / self._num_leds + self._color_offset)) % 255
            (r, g, b) = colors.hsv2rgb((h, s, v))

            self._led.setRGB(led, r, g, b)

    def _params_updated(self):
        super()._params_updated()

        self._saturation = self._params['saturation'].get_value()
        self._value = self._params['value'].get_value()
        self._offset = self._params['offset'].get_value()
        self._start = self._params['start'].get_value()
        self._end = self._params['end'].get_value()
        self._min_value = self._params['min_value'].get_value()
        self._min_value = self._params['high_pass'].get_value()
        self._log = self._params['log'].get_value()
        self._color_offset = self._params['color_offset'].get_value()
