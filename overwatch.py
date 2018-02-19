#!/usr/bin/env python3.6

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame,QLabel,QPushButton,
    QHBoxLayout,QStyleFactory,QSplitter,QTextEdit,QGridLayout,QLCDNumber,QDial)
from pyqtgraph import PlotWidget

class OverWatch(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout()

        # tH is the house temperature panel
        tH = QFrame(self)
        tH.setFrameShape(QFrame.StyledPanel)
        tHvbox = QGridLayout()
        tHvbox.addWidget(QLabel('Out Temp'),1,0)
        tHvbox.addWidget(QLabel('In Temp') ,1,1)
        self.outTemp=QLCDNumber()
        self.inTemp=QLCDNumber()
        tHvbox.addWidget(self.outTemp,2,0)
        tHvbox.addWidget(self.inTemp ,2,1)
        self.tPlot = PlotWidget()
        tHvbox.addWidget(self.tPlot, 3,0,2,2)
        self.weekbt = QPushButton('Week')
        self.monthbt = QPushButton('Month')
        tHvbox.addWidget(self.weekbt, 5,0)
        tHvbox.addWidget(self.monthbt,5,1)
        self.windDir = QDial()
        self.windDir.setWrapping(True)
        self.windDir.setNotchesVisible(True)
        tHvbox.addWidget(self.windDir,1,2,5,5)

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
        self.tPlot.plot([2,4,6,8],[1,2,3,4],pen=None,symbol='x')
        self.setLayout(hbox)
        self.setGeometry(300,300,800,600)
        self.setWindowTitle('Splitter')
        self.show()

if __name__=='__main__':
    app = QApplication(sys.argv)
    ovw = OverWatch()
    sys.exit(app.exec_())
    
