#!/usr/bin/env python

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import sys

class View(QDialog):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)

        self.originalPalette = QApplication.palette()

        styleComboBox = QComboBox()
        styleComboBox.addItems(QStyleFactory.keys())

        styleLabel = QLabel("&Style:")
        styleLabel.setBuddy(styleComboBox)

        self.useStylePaletteCheckBox = QCheckBox("&Use style's standard palette")
        self.useStylePaletteCheckBox.setChecked(True)

        disableWidgetsCheckBox = QCheckBox("&Disable widgets")

        self.createTabGroup()

        styleComboBox.activated[str].connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        disableWidgetsCheckBox.toggled.connect(self.tabGroup.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout,0,0,1,2)
        mainLayout.addWidget(self.tabGroup,1,0,1,2)
        mainLayout.setRowStretch(0,1)
        #mainLayout.setRowStretch(1,1)
        #mainLayout.setRowStretch(2,1)
        #mainLayout.setColumnStretch(0,1)
        #mainLayout.setColumnStretch(1,1)
        self.setLayout(mainLayout)

        self.setWindowTitle("Styles")
        self.changeStyle('Fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        if (self.useStylePaletteCheckBox.isChecked()):
            QApplication.setPalette(QApplication.style().standardPalette())
        else:
            QApplication.setPalette(self.originalPalette)

    def advanceProgressBar(self):
        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)

    def createAnalogControls(self):
        self.analogControls = QGroupBox("")

        layout = QHBoxLayout()
        velocity = QSlider(Qt.Vertical, self.analogControls)
        speed = QSlider(Qt.Vertical, self.analogControls)

        layout.addWidget(velocity)
        layout.addWidget(speed)
        layout.addStretch(1)

        self.analogControls.setLayout(layout)

    def createDigitalErrors(self):
        self.digitalErrors = QGroupBox("Error")
        layout = QVBoxLayout()

        cbBrakes = QCheckBox("brakes")
        cbEngine = QCheckBox("engine")

        layout.addWidget(cbBrakes)
        layout.addWidget(cbEngine)
        layout.addStretch(1)
        self.digitalErrors.setLayout(layout)

    def createDigitalWarnings(self):
        self.digitalWarnings = QGroupBox("Warning")

        layout = QVBoxLayout()
        cbWaterTemperature = QCheckBox("water")
        layout.addWidget(cbWaterTemperature)

        self.digitalWarnings.setLayout(layout)

    def createDigitalInformation(self):
        self.digitalInformation = QGroupBox("Information")

        layout = QVBoxLayout()
        cbDoors = QCheckBox("doors")
        layout.addWidget(cbDoors)

        self.digitalInformation.setLayout(layout)

    def createDigitalControls(self):

        self.createDigitalErrors()
        self.createDigitalWarnings()
        self.createDigitalInformation()

        self.digitalControls = QGroupBox()
        layout = QHBoxLayout()

        layout.addWidget(self.digitalErrors)
        layout.addWidget(self.digitalWarnings)
        layout.addWidget(self.digitalInformation)
        layout.addStretch(1)

        self.digitalControls.setLayout(layout)

    def createTabGroup(self):

        self.createAnalogControls()
        self.createDigitalControls()

        self.tabGroup = QTabWidget()
        ##self.tabGroup.setSizePolicy(QSizePolicy.Preferred,QSizePolicy.Ignored)
        analogtab = QWidget();
        analoglayout = QHBoxLayout()
        analoglayout.addWidget(self.analogControls)
        ##analoglayout.setStretch(1,1)
        analogtab.setLayout(analoglayout)

        digitaltab = QWidget()
        digitallayout = QHBoxLayout()
        digitallayout.addWidget(self.digitalControls)
        ##digitallayout.setStretch(1,1)
        digitaltab.setLayout(digitallayout)

        self.tabGroup.addTab(analogtab,"&Analog")
        self.tabGroup.addTab(digitaltab,"&Digital")

if __name__ == '__main__':
    appctxt = ApplicationContext()
    surface = View()
    surface.show()
    sys.exit(appctxt.app.exec_())
