import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5 import QtCore


class WellButton(QAbstractButton):
    def __init__(self, parent=None):
        super(WellButton, self).__init__(parent)
        self.counter = 0
        self.well_id = str()
        self.wellsize = 0

        # Well content information
        self.max_volume = 0
        self.min_volume = 0
        self.dilution_factor = 1
        self.contents = list()  # List of tuples with the media/sample name and volume of each

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(QColor(255, 255, 255))  # returns a white color
        # for circle make the ellipse radii match
        radx = self.wellsize/2
        rady = self.wellsize/2
        # draw red circle
        paint.setPen(QColor(225,10,10))  # creates a red outline
        center = Qt.QPoint(self.wellsize/2, self.wellsize/2)
        # optionally fill each circle yellow
        if self.counter%2 == 0:
            paint.setBrush(QColor(201,201,201))
        else:
            paint.setBrush(QColor(78,219,229))
        paint.drawEllipse(center, radx, rady)
        paint.end()

    def sizeHint(self):
        return QtCore.QSize(self.wellsize+1, self.wellsize+1)

    def change_select(self):
        self.counter += 1
        self.update()
