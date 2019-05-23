import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import Qt
from PyQt5 import QtCore


wellsize = 500 / (8 + 12)
platedimensions = (8, 12)
alphabet = "ABCDEFGHIJKLMNOP"


class PlateArea(QWidget):
    def __init__(self, parent=None):
        super(PlateArea, self).__init__(parent)
        self.row_buttons = list()
        self.column_buttons = list()
        for row in range(platedimensions[0]):
            row_name = alphabet[row]
            mybutton = Qt.QPushButton()
            mybutton.setText(row_name)
            mybutton.setGeometry(wellsize, wellsize)  # this may need its location in the widget as well
            mybutton.clicked.connect(lambda: self.select_all_wells(row+1))
        for column in range(platedimensions[1]):
            col = column+1
            mybutton = Qt.QPushButton()
            mybutton.setText(str(col))
            mybutton.setGeometry(wellsize,wellsize)  # again this may need the location in the widget as well
            mybutton.clicked.connect(lambda: self.select_all_wells(col))

    def select_all_wells(self, rowcol_index):
        print("oh hello!")






app = QApplication(sys.argv)
window = QWidget()
layout = QGridLayout(window)
layout.setSpacing(wellsize/10)
window.resize(wellsize*platedimensions[1]+10, wellsize*platedimensions[0]+10)
print(window.geometry())

window.show()
sys.exit(app.exec_())
