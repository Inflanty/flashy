# -*- coding: utf-8 -*-
"""
Demonstrates use of PlotWidget class. This is little more than a 
GraphicsView with a PlotItem placed in its center.
"""
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

#QtGui.QApplication.setGraphicsSystem('raster')
app = pg.mkQApp()
mw = QtGui.QMainWindow()
mw.setWindowTitle('pyqtgraph example: PlotWidget')
mw.resize(800,800)
cw = QtGui.QWidget()
mw.setCentralWidget(cw)
l = QtGui.QVBoxLayout()
cw.setLayout(l)

pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
l.addWidget(pw)
pw2 = pg.PlotWidget(name='Plot2')
l.addWidget(pw2)
pw3 = pg.PlotWidget()
l.addWidget(pw3)

mw.show()

## Create an empty plot curve to be filled later, set its pen
p1 = pw.plot()
p1.setPen((200,200,100))

pw.setLabel('left', 'Value', units='V')
pw.setLabel('bottom', 'Time', units='s')
pw.setXRange(0, 2)
pw.setYRange(0, 1e-10)

## Test large numbers
curve = pw3.plot(np.random.normal(size=100)*1e0, clickable=True)
curve.curve.setClickable(True)
curve.setPen('w')  ## white pen
curve.setShadowPen(pg.mkPen((70,70,30), width=6, cosmetic=True))


lr = pg.LinearRegionItem([1, 30], bounds=[0,100], movable=True)
pw3.addItem(lr)
line = pg.InfiniteLine(angle=90, movable=True)
pw3.addItem(line)
line.setBounds([0,200])

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    #    QtGui.QApplication.instance().exec_()
    tabEdit = [1, 3, 5, 7]
    tabCopy = tabEdit
    tabEdit[0] = 0
    print(tabEdit)
    print(tabCopy)

    varEdit = 1
    varCopy = varEdit
    varEdit = 0
    print(varEdit)
    print(varCopy)