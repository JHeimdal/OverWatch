#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import socket

import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QLabel, QPushButton
                             , QHBoxLayout, QStyleFactory, QSplitter, QTextEdit
                             , QGridLayout, QLCDNumber, QDial, QProgressBar)
from pyqtgraph import PlotWidget


class DataCollect(QThread):
    """ Object that broadcast data from DataWatch to Overwatch """
    def __init__(self, signal):
        super().__init__()
        self.ip_port = ('192.168.0.104', 9994)
        self.signal = signal

    def __del__(self):
        self.wait()

    def run(self):
        # try:
        #     pass
        # except ConnectionRefusedError as e:
        #     raise
        # finally:
        #    pass
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(self.ip_port)
        self.soc.sendall("Update".encode())
        data = self.soc.recv(1024)
        self.soc.close()
        self.signal.emit(data.decode())


class OverWatch(QWidget):
    update_sig = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.collDat)
        self.timer.start(5000)
        self.collectData = DataCollect(self.update_sig)
        self.update_sig.connect(self.update)
        self.inrec = []
        self.dsb1 = []
        self.dsb2 = []
        self.dsb3 = []
        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout()

        # tH is the house temperature panel
        tH = QFrame(self)
        tH.setFrameShape(QFrame.StyledPanel)
        tHvbox = QGridLayout()
        tHvbox.addWidget(QLabel('Inside'), 1, 1, 1, 2)
        tHvbox.addWidget(QLabel('Outside'), 1, 3, 1, 2)
        tHvbox.addWidget(QLabel('Temp:'), 2, 0)
        tHvbox.addWidget(QLabel('C'), 2, 2)
        tHvbox.addWidget(QLabel('C'), 2, 4)
        tHvbox.addWidget(QLabel('Humidity:'), 3, 0)
        tHvbox.addWidget(QLabel('%'), 3, 2)
        tHvbox.addWidget(QLabel('%'), 3, 4)
        self.outTemp = QLCDNumber()
        self.inTemp = QLCDNumber()
        self.outHD = QLCDNumber()
        self.inHD = QLCDNumber()
        # get the palette
        palette = self.inTemp.palette()
        # palette.setColor(palette.Window, QtGui.QColor(255, 0, 0))
        palette.setColor(palette.Light, QtGui.QColor(0, 0, 0))
        palette.setColor(palette.Dark, QtGui.QColor(0, 0, 0))
        self.inTemp.setPalette(palette)
        self.outTemp.setPalette(palette)
        self.inHD.setPalette(palette)
        self.outHD.setPalette(palette)

        tHvbox.addWidget(self.outTemp, 2, 3, 1, 1)
        tHvbox.addWidget(self.inTemp, 2, 1, 1, 1)
        tHvbox.addWidget(self.outHD, 3, 3, 1, 1)
        tHvbox.addWidget(self.inHD, 3, 1, 1, 1)
        self.tPlot = PlotWidget()
        tHvbox.addWidget(self.tPlot, 4, 0, 4, 5)
        self.weekbt = QPushButton('Week')
        self.monthbt = QPushButton('Month')
        tHvbox.addWidget(self.weekbt, 8, 0)
        tHvbox.addWidget(self.monthbt, 8, 1)
        self.pBar = QProgressBar()
        self.pBar.setOrientation(Qt.Vertical)
        tHvbox.addWidget(self.pBar, 4, 6)
        self.pBar.setRange(950, 1050)

        tH.setLayout(tHvbox)

        tr = QFrame(self)
        tr.setFrameShape(QFrame.StyledPanel)

        bt = QFrame(self)
        bt.setFrameShape(QFrame.StyledPanel)

        split1 = QSplitter(Qt.Horizontal)
        split1.addWidget(bt)
        split1.addWidget(tr)

        split2 = QSplitter(Qt.Vertical)
        split2.addWidget(tH)
        split2.addWidget(split1)
        hbox.addWidget(split2)
        self.tPlot.plot(self.inrec, pen=None, symbol='x')
        self.setLayout(hbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('OverWatch')
        self.show()
        self.collDat()

    def collDat(self):
        """ collect values """
        self.collectData.start()

    def update(self, dat):
        """ Update the plot """
        data = dict([[v.split(':')[0], float(v.split(':')[1])] for v in dat.split(',')])
        self.inTemp.display(data['InTemp'])
        self.outTemp.display(data['DSB1'])
        self.inHD.display(data['InHD'])
        self.outHD.display(data['DSB2'])
        # self.pBar.setValue(int(data['OutPress']))
        self.inrec.append(data['InTemp'])
        self.dsb1.append(data['DSB1'])
        self.dsb2.append(data['DSB2'])
        self.dsb3.append(data['DSB3'])
        self.tPlot.plot(self.inrec, symbol='x')
        self.tPlot.plot(self.dsb1, symbol='o')
        self.tPlot.plot(self.dsb2, symbol='o')
        self.tPlot.plot(self.dsb3, symbol='o')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ovw = OverWatch()
    sys.exit(app.exec_())
