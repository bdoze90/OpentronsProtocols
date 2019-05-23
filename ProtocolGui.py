"""This file starts a GUI where you can change the settings for each of the protocols. The protocol settings
    are loaded via their settings file, which is generated and read in their settings class."""

import sys
import os
from PyQt5 import QtWidgets, Qt, QtGui, QtCore, uic
from PlateFeatures import WellButton


class protocolGui(QtWidgets.QMainWindow):
    def __init__(self):
        super(protocolGui, self).__init__()
        uic.loadUi('Opentrons_Settings.ui', self)
        settings_file_location = 'Volumes/Seagate_Drive/Settings_Files'
        # Plate settings
        self.addplatebutton.clicked.connect(self.add_plate)
        filler_plate = Plate(self)
        self.Plates = {'Select Plate...': filler_plate}
        self.curPlatecomboBox.addItem('Select Plate...')
        self.plate_window = filler_plate
        self.curPlatecomboBox.currentIndexChanged.connect(self.flip_plates)
        self.show()
        # There should be a way of tracking the current wells selected either here or in the plate class

        # To track the number of wells selected:
        self.selected_wells = list()  # This lists the wells of the current plate that are selected

    def add_plate(self):
        ptypes = ['6-well', '12-well', '24-well', '96-well', '384-well']
        p_dialog = QtWidgets.QDialog()
        uic.loadUi('platedialog.ui', p_dialog)
        p_dialog.platetypeCombo.addItems(ptypes)
        # Run the dialog and get the information from P_dialog input
        if p_dialog.exec():
            p_name = p_dialog.nameofplate.text()
            p_type = p_dialog.platetypeCombo.currentText()
            plate = Plate(self.centralWidget())
            plate.p_name = p_name
            plate.set_dimensions(p_type)
            self.Plates[p_name] = plate
            self.curPlatecomboBox.addItem(p_name)

    def flip_plates(self):
        plate_window = self.Plates[self.curPlatecomboBox.currentText()]
        plate_window.setGeometry(379, 190, 381, 261)
        print("hello?")
        plate_window.show()

#  Need selected wells information.  Need row and column button labels to select all of a row or column.
#   Need a drag select option


class Plate(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Plate, self).__init__(parent)
        self.p_name = str()
        self.alphabet = "ABCDEFGHIJKLMNOP"

        # This container stores the information for the wells
        self.wells = list()  # stores all of the well buttons containing information on the contents of the well

    def set_dimensions(self, ptype):
        dim = (0, 0)
        if ptype == '6-well':
            dim = (2, 3)
        elif ptype == '12-well':
            dim = (3, 4)
        elif ptype == '24-well':
            dim = (4, 6)
        elif ptype == '96-well':
            dim = (8, 12)
        elif ptype == '384-well':
            dim = (16, 24)

        mylayout = QtWidgets.QGridLayout()
        wellsize = 500 / (dim[0] + dim[1])
        mylayout.setSpacing(wellsize/11)

        for i in range(dim[0]):
            for j in range(dim[1]):
                button = WellButton()
                button.wellsize = wellsize
                self.wells.append(button)
                button.well_id = self.alphabet[i] + str(j + 1)
                button.setToolTip(button.well_id)
                mylayout.addWidget(button, i, j)

        for button in self.wells:
            button.clicked.connect(button.change_select)

        self.setLayout(mylayout)

app = Qt.QApplication(sys.argv)
startup = protocolGui()
sys.exit(app.exec_())
