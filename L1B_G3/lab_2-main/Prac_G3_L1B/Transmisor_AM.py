#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Transmisor AM
# Author: L1BG3
# Copyright: uis
# Description: transmisorAM
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from CalculoPotenciaComunicaciones import CalculoPotenciaComunicaciones  # grc-generated hier_block
from ModuladorAM import ModuladorAM  # grc-generated hier_block
from gnuradio import analog
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore



from gnuradio import qtgui

class Transmisor_AM(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Transmisor AM", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Transmisor AM")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Transmisor_AM")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 200000
        self.Ka = Ka = 1
        self.GTX = GTX = 0
        self.FM = FM = 1000
        self.FC = FC = 50000000
        self.Ac = Ac = 0.1
        self.A = A = 1

        ##################################################
        # Blocks
        ##################################################
        self._Ka_range = Range(0, 4, 0.0001, 1, 200)
        self._Ka_win = RangeWidget(self._Ka_range, self.set_Ka, "Coeficiente Ka", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ka_win)
        self._GTX_range = Range(0, 30, 1, 0, 200)
        self._GTX_win = RangeWidget(self._GTX_range, self.set_GTX, "Ganancia de Tx", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._GTX_win)
        self._FM_range = Range(0, 20000, 100, 1000, 200)
        self._FM_win = RangeWidget(self._FM_range, self.set_FM, "Frecuencia de mensaje", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._FM_win)
        self._FC_range = Range(50000000, 2200000000, 1000000, 50000000, 200)
        self._FC_win = RangeWidget(self._FC_range, self.set_FC, "Frecuencia Portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._FC_win)
        self._Ac_range = Range(0, 1, 0.0001, 0.1, 200)
        self._Ac_win = RangeWidget(self._Ac_range, self.set_Ac, "Amplitud Portadora", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._Ac_win)
        self._A_range = Range(0, 1, 0.0001, 1, 200)
        self._A_win = RangeWidget(self._A_range, self.set_A, "Amplitud Modulante", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._A_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(FC, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(GTX, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, FM, A, 0, 0)
        self.ModuladorAM_0 = ModuladorAM(
            Ac=Ac,
            Ka=Ka,
        )
        self.CalculoPotenciaComunicaciones_0 = CalculoPotenciaComunicaciones(
            l_vect=1024,
        )

        self.top_layout.addWidget(self.CalculoPotenciaComunicaciones_0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.ModuladorAM_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.CalculoPotenciaComunicaciones_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.ModuladorAM_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Transmisor_AM")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_Ka(self):
        return self.Ka

    def set_Ka(self, Ka):
        self.Ka = Ka
        self.ModuladorAM_0.set_Ka(self.Ka)

    def get_GTX(self):
        return self.GTX

    def set_GTX(self, GTX):
        self.GTX = GTX
        self.uhd_usrp_sink_0.set_gain(self.GTX, 0)

    def get_FM(self):
        return self.FM

    def set_FM(self, FM):
        self.FM = FM
        self.analog_sig_source_x_0.set_frequency(self.FM)

    def get_FC(self):
        return self.FC

    def set_FC(self, FC):
        self.FC = FC
        self.uhd_usrp_sink_0.set_center_freq(self.FC, 0)

    def get_Ac(self):
        return self.Ac

    def set_Ac(self, Ac):
        self.Ac = Ac
        self.ModuladorAM_0.set_Ac(self.Ac)

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A
        self.analog_sig_source_x_0.set_amplitude(self.A)




def main(top_block_cls=Transmisor_AM, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
