import socket
import math
from struct import *
from threading import Thread
from bibliopixel.animation import colors
from . import BaseStripAnim, RangeType, FloatType, BooleanType


class AudioVisulizer(BaseStripAnim):
    name = 'audiovisulizer'
    params = dict(dict(
        saturation=RangeType(value=1, min=0, max=1, step=0.01),
        value=FloatType(30, min=1),
        offset=FloatType(60),
        start=RangeType(value=.01, min=0, max=1, step=0.01),
        end=RangeType(value=.7, min=0, max=1, step=0.01),
        min_value=RangeType(value=.05, min=0, max=1, step=0.01),
        log=BooleanType(value=False),
        log_base=FloatType(value=1, min=1, step=1),
        color_offset=RangeType(value=0.8, min=0, max=1, step=0.01),
        color_size=FloatType(value=1.2, min=0.01, max=2, step=0.01),
        color_direction=BooleanType(value=True),
        pos=RangeType(value=0, min=0, max=1, step=0.01),
        high_pass=FloatType(value=20, step=1),
        sources=FloatType(value=1, min=1, step=1)
    ), **BaseStripAnim.params)

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
        num = int(math.ceil(self._num_leds / self._sources))

        src_start = (self.num_data - 1) * self._start
        src_end = (self.num_data - 1) * self._end
        src_num = src_end - src_start
        w = src_num / num
        out = [0] * num

        src_from = 0
        for i in range(num):
            if self._log:
                src_to = (pow(10, (i + 1) / num * self._log_base) - 1) / (
                    math.pow(10, self._log_base) - 1) * src_num + src_start
            else:
                src_to = (i + 1) * w + src_start
            # v = AudioVisulizer._sum_array(data, src_from, src_to) / (src_to - src_from)
            v = AudioVisulizer._max_array(data, src_from, src_to)
            v = (v + self._offset + self._high_pass * i / num) / self._value
            out[i] = min(max(v, self._min_value), 1)
            src_from = src_to
        return out

    @staticmethod
    def _max_array(array, start, end):
        start_int = int(start)
        start_diff = start - start_int
        end_int = int(end)
        end_diff = end - end_int
        diff = end - start
        v = min(array)

        if start < 0 or end > (len(array) - 1) or end < start:
            raise IndexError()

        if start is end:
            return None
        if start_int is end_int:  # eg 1.3 to 1.7
            return array[start_int]
        if start_diff > 0:
            d = start_diff
            v1 = array[start_int]
            v2 = array[start_int + 1]
            x = AudioVisulizer._interpolate_value(v1, v2, d)
            v = max(v, x)
        if end_diff > 0:
            d = end_diff
            v1 = array[end_int]
            v2 = array[end_int + 1]
            x = AudioVisulizer._interpolate_value(v1, v2, d)
            v = max(x, v)

        return max(max(array[start_int:end_int + 1]), v)

    @staticmethod
    def _sum_array(array, start, end):
        _sum = 0
        start_int = int(start)
        start_diff = start - start_int
        end_int = int(end)
        end_diff = end - end_int
        diff = end - start

        if start < 0 or end > (len(array) - 1) or end < start:
            raise IndexError()

        if start is end:
            return 0
        if start_int is end_int:  # eg 1.3 to 1.7
            d1 = start % 1
            d2 = end % 1
            v1 = array[start_int]
            v2 = array[start_int + 1]
            x1 = AudioVisulizer._interpolate_value(v1, v2, d1)
            x2 = AudioVisulizer._interpolate_value(v1, v2, d2)
            v = (x1 + x2) / 2 * diff
            return v
        if start_diff > 0:
            d = start_diff
            v1 = array[start_int]
            v2 = array[start_int + 1]
            x = AudioVisulizer._interpolate_value(v1, v2, d)
            _sum += (x + v2) / 2 * d
            start_int += 1
        if end_diff > 0:
            d = end_diff
            v1 = array[end_int]
            v2 = array[end_int + 1]
            x = AudioVisulizer._interpolate_value(v1, v2, d)
            _sum += (v1 + x) / 2 * d

        _sum += array[start_int] / 2 + array[end_int] / 2
        start_int += 1
        end_int -= 1
        if start_int >= end_int:
            return _sum
        _sum += sum(array[start_int:end_int + 1])

        return _sum

    @staticmethod
    def _interpolate_value(v1, v2, d):
        """
        _interpolate_value(0,1,.7) == 0.7

        :param v1:  float
        :param v2:  float
        :param d:   float   0< d < 1
        :return:    float
        """
        return v1 * (1 - d) + v2 * d

    def step(self, amt=1):

        data = self.get_data()
        num = len(data)

        s = int(self._saturation * 255)
        offset = int(self._pos * num)
        for i, led in enumerate(self._device.get_leds()):
            i += offset
            i = i % (2 * num - 2)
            if i >= num:
                i = (2 * num - 2) - i
            v = data[i]
            v = int(v * 255 * self._brightness)
            h = i / num / self._color_size
            if self._color_direction:
                h *= -1
            h += 1 + self._color_offset
            h = int(255 * h % 255)
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
        self._high_pass = self._params['high_pass'].get_value()
        self._log = self._params['log'].get_value()
        self._log_base = self._params['log_base'].get_value()
        self._color_offset = self._params['color_offset'].get_value()
        self._color_size = self._params['color_size'].get_value()
        self._color_direction = self._params['color_direction'].get_value()
        self._sources = self._params['sources'].get_value()
        self._pos = self._params['pos'].get_value()
