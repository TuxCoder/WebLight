#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Fft
# Generated: Mon Oct 31 09:42:50 2016
##################################################

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser


class fft(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Fft")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 44100
        self.fft_size = fft_size = 1024*4
        self.alpha = alpha = .3

        ##################################################
        # Blocks
        ##################################################
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_f(
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	ref_scale=2,
        	frame_rate=30,
        	avg_alpha=alpha,
        	average=True,
        )
#        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_float*fft_size, '172.31.107.41', 9999, 1472, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_float*fft_size, '127.0.0.1', 9999, 1472, True)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((0, ))
        self.audio_source_0 = audio.source(samp_rate, '', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.audio_source_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.audio_source_0, 1), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.logpwrfft_x_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.logpwrfft_x_0, 0), (self.blocks_udp_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.logpwrfft_x_0.set_avg_alpha(self.alpha)


def main(top_block_cls=fft, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
