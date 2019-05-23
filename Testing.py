import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5 import QtCore


class PicButton(QAbstractButton):
    def __init__(self, parent=None):
        super(PicButton, self).__init__(parent)
        self.m_flag = False
        self.well_id = str()

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(QColor(255,255,255))  # returns a white color
        # for circle make the ellipse radii match
        radx = 120
        rady = 120
        # draw red circle
        paint.setPen(QColor(225,10,10))  # creates a red outline
        center = Qt.QPoint(125, 125)
        # optionally fill each circle yellow
        if self.m_flag:
            paint.setBrush(QColor(201,201,201))
        else:
            paint.setBrush(QColor(78,219,229))
        paint.drawEllipse(center, radx, rady)
        paint.end()

    def sizeHint(self):
        return QtCore.QSize(250, 250)


app = QApplication(sys.argv)
window = QWidget()
layout = QHBoxLayout(window)

button = PicButton()
layout.addWidget(button)

window.show()
sys.exit(app.exec_())