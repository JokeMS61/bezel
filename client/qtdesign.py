# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dashtest.ui'
#
# Created: Wed Sep 21 11:32:01 2022
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(834, 409)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.message = QtGui.QLabel(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(5, 380, 571, 21))
        self.message.setFrameShape(QtGui.QFrame.Panel)
        self.message.setFrameShadow(QtGui.QFrame.Sunken)
        self.message.setObjectName(_fromUtf8("message"))
        self.btn_connect = QtGui.QPushButton(self.centralwidget)
        self.btn_connect.setGeometry(QtCore.QRect(445, 340, 66, 28))
        self.btn_connect.setObjectName(_fromUtf8("btn_connect"))
        self.btn_quit = QtGui.QPushButton(self.centralwidget)
        self.btn_quit.setGeometry(QtCore.QRect(515, 340, 66, 28))
        self.btn_quit.setObjectName(_fromUtf8("btn_quit"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 5, 576, 331))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.txt_speed = QtGui.QLabel(self.tab)
        self.txt_speed.setGeometry(QtCore.QRect(10, 50, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.txt_speed.setFont(font)
        self.txt_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_speed.setObjectName(_fromUtf8("txt_speed"))
        self.sl_volt = QtGui.QSlider(self.tab)
        self.sl_volt.setEnabled(False)
        self.sl_volt.setGeometry(QtCore.QRect(435, 80, 41, 191))
        self.sl_volt.setMaximum(120)
        self.sl_volt.setOrientation(QtCore.Qt.Vertical)
        self.sl_volt.setObjectName(_fromUtf8("sl_volt"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(10, 30, 53, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(215, 10, 61, 21))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.sl_temp_o = QtGui.QSlider(self.tab)
        self.sl_temp_o.setGeometry(QtCore.QRect(155, 80, 41, 191))
        self.sl_temp_o.setMaximum(120)
        self.sl_temp_o.setPageStep(1)
        self.sl_temp_o.setOrientation(QtCore.Qt.Vertical)
        self.sl_temp_o.setObjectName(_fromUtf8("sl_temp_o"))
        self.label_16 = QtGui.QLabel(self.tab)
        self.label_16.setEnabled(False)
        self.label_16.setGeometry(QtCore.QRect(485, 10, 81, 21))
        self.label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.sl_pressure_o = QtGui.QSlider(self.tab)
        self.sl_pressure_o.setEnabled(False)
        self.sl_pressure_o.setGeometry(QtCore.QRect(365, 80, 41, 191))
        self.sl_pressure_o.setMaximum(120)
        self.sl_pressure_o.setOrientation(QtCore.Qt.Vertical)
        self.sl_pressure_o.setObjectName(_fromUtf8("sl_pressure_o"))
        self.label_6 = QtGui.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(75, 30, 53, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(145, 10, 61, 21))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.sl_consumption = QtGui.QSlider(self.tab)
        self.sl_consumption.setEnabled(False)
        self.sl_consumption.setGeometry(QtCore.QRect(505, 80, 41, 191))
        self.sl_consumption.setMaximum(120)
        self.sl_consumption.setOrientation(QtCore.Qt.Vertical)
        self.sl_consumption.setObjectName(_fromUtf8("sl_consumption"))
        self.label_10 = QtGui.QLabel(self.tab)
        self.label_10.setEnabled(False)
        self.label_10.setGeometry(QtCore.QRect(285, 30, 53, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_8 = QtGui.QLabel(self.tab)
        self.label_8.setEnabled(True)
        self.label_8.setGeometry(QtCore.QRect(215, 30, 53, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.btn_speed_down = QtGui.QPushButton(self.tab)
        self.btn_speed_down.setGeometry(QtCore.QRect(35, 275, 21, 21))
        self.btn_speed_down.setObjectName(_fromUtf8("btn_speed_down"))
        self.label_14 = QtGui.QLabel(self.tab)
        self.label_14.setEnabled(False)
        self.label_14.setGeometry(QtCore.QRect(425, 30, 53, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.sl_speed = QtGui.QSlider(self.tab)
        self.sl_speed.setGeometry(QtCore.QRect(15, 80, 41, 191))
        self.sl_speed.setMaximum(180)
        self.sl_speed.setPageStep(1)
        self.sl_speed.setOrientation(QtCore.Qt.Vertical)
        self.sl_speed.setObjectName(_fromUtf8("sl_speed"))
        self.btn_speed_up = QtGui.QPushButton(self.tab)
        self.btn_speed_up.setGeometry(QtCore.QRect(15, 275, 21, 21))
        self.btn_speed_up.setObjectName(_fromUtf8("btn_speed_up"))
        self.label_9 = QtGui.QLabel(self.tab)
        self.label_9.setEnabled(False)
        self.label_9.setGeometry(QtCore.QRect(285, 10, 51, 21))
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.sl_drive = QtGui.QSlider(self.tab)
        self.sl_drive.setEnabled(True)
        self.sl_drive.setGeometry(QtCore.QRect(225, 80, 41, 191))
        self.sl_drive.setMaximum(8000)
        self.sl_drive.setOrientation(QtCore.Qt.Vertical)
        self.sl_drive.setObjectName(_fromUtf8("sl_drive"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(5, 10, 61, 20))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setText(_fromUtf8("<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">speed</span></p></body></html>"))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.sl_temp = QtGui.QSlider(self.tab)
        self.sl_temp.setGeometry(QtCore.QRect(85, 80, 41, 191))
        self.sl_temp.setMaximum(140)
        self.sl_temp.setPageStep(1)
        self.sl_temp.setOrientation(QtCore.Qt.Vertical)
        self.sl_temp.setObjectName(_fromUtf8("sl_temp"))
        self.label_11 = QtGui.QLabel(self.tab)
        self.label_11.setEnabled(False)
        self.label_11.setGeometry(QtCore.QRect(355, 10, 51, 21))
        self.label_11.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_13 = QtGui.QLabel(self.tab)
        self.label_13.setEnabled(False)
        self.label_13.setGeometry(QtCore.QRect(425, 10, 61, 21))
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_15 = QtGui.QLabel(self.tab)
        self.label_15.setEnabled(False)
        self.label_15.setGeometry(QtCore.QRect(495, 30, 53, 16))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_7 = QtGui.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(145, 30, 53, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_12 = QtGui.QLabel(self.tab)
        self.label_12.setEnabled(False)
        self.label_12.setGeometry(QtCore.QRect(355, 30, 53, 16))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.sl_gas = QtGui.QSlider(self.tab)
        self.sl_gas.setEnabled(False)
        self.sl_gas.setGeometry(QtCore.QRect(295, 80, 41, 191))
        self.sl_gas.setMaximum(120)
        self.sl_gas.setOrientation(QtCore.Qt.Vertical)
        self.sl_gas.setObjectName(_fromUtf8("sl_gas"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(75, 10, 61, 21))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.btn_watertemp_down = QtGui.QPushButton(self.tab)
        self.btn_watertemp_down.setGeometry(QtCore.QRect(105, 275, 21, 21))
        self.btn_watertemp_down.setObjectName(_fromUtf8("btn_watertemp_down"))
        self.btn_watertemp_up = QtGui.QPushButton(self.tab)
        self.btn_watertemp_up.setGeometry(QtCore.QRect(85, 275, 21, 21))
        self.btn_watertemp_up.setObjectName(_fromUtf8("btn_watertemp_up"))
        self.btn_oiltemp_down = QtGui.QPushButton(self.tab)
        self.btn_oiltemp_down.setGeometry(QtCore.QRect(175, 275, 21, 21))
        self.btn_oiltemp_down.setObjectName(_fromUtf8("btn_oiltemp_down"))
        self.btn_oiltemp_up = QtGui.QPushButton(self.tab)
        self.btn_oiltemp_up.setGeometry(QtCore.QRect(155, 275, 21, 21))
        self.btn_oiltemp_up.setObjectName(_fromUtf8("btn_oiltemp_up"))
        self.btn_drive_down = QtGui.QPushButton(self.tab)
        self.btn_drive_down.setGeometry(QtCore.QRect(245, 275, 21, 21))
        self.btn_drive_down.setObjectName(_fromUtf8("btn_drive_down"))
        self.btn_drive_up = QtGui.QPushButton(self.tab)
        self.btn_drive_up.setGeometry(QtCore.QRect(225, 275, 21, 21))
        self.btn_drive_up.setObjectName(_fromUtf8("btn_drive_up"))
        self.txt_watertemp = QtGui.QLabel(self.tab)
        self.txt_watertemp.setGeometry(QtCore.QRect(80, 50, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.txt_watertemp.setFont(font)
        self.txt_watertemp.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_watertemp.setObjectName(_fromUtf8("txt_watertemp"))
        self.txt_oiltemp = QtGui.QLabel(self.tab)
        self.txt_oiltemp.setGeometry(QtCore.QRect(150, 50, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.txt_oiltemp.setFont(font)
        self.txt_oiltemp.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_oiltemp.setObjectName(_fromUtf8("txt_oiltemp"))
        self.txt_drive = QtGui.QLabel(self.tab)
        self.txt_drive.setGeometry(QtCore.QRect(220, 50, 51, 26))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.txt_drive.setFont(font)
        self.txt_drive.setAlignment(QtCore.Qt.AlignCenter)
        self.txt_drive.setObjectName(_fromUtf8("txt_drive"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.groupBox = QtGui.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 266, 181))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.chk_blink_l = QtGui.QCheckBox(self.groupBox)
        self.chk_blink_l.setGeometry(QtCore.QRect(10, 20, 81, 20))
        self.chk_blink_l.setObjectName(_fromUtf8("chk_blink_l"))
        self.chk_blink_r = QtGui.QCheckBox(self.groupBox)
        self.chk_blink_r.setGeometry(QtCore.QRect(10, 45, 81, 20))
        self.chk_blink_r.setObjectName(_fromUtf8("chk_blink_r"))
        self.chk_highbeam = QtGui.QCheckBox(self.groupBox)
        self.chk_highbeam.setEnabled(True)
        self.chk_highbeam.setGeometry(QtCore.QRect(10, 70, 81, 20))
        self.chk_highbeam.setObjectName(_fromUtf8("chk_highbeam"))
        self.chk_foglight = QtGui.QCheckBox(self.groupBox)
        self.chk_foglight.setEnabled(True)
        self.chk_foglight.setGeometry(QtCore.QRect(10, 120, 81, 20))
        self.chk_foglight.setObjectName(_fromUtf8("chk_foglight"))
        self.chk_lowbeam = QtGui.QCheckBox(self.groupBox)
        self.chk_lowbeam.setEnabled(True)
        self.chk_lowbeam.setGeometry(QtCore.QRect(10, 95, 81, 20))
        self.chk_lowbeam.setObjectName(_fromUtf8("chk_lowbeam"))
        self.chk_cruisecontrol = QtGui.QCheckBox(self.groupBox)
        self.chk_cruisecontrol.setEnabled(True)
        self.chk_cruisecontrol.setGeometry(QtCore.QRect(120, 20, 106, 20))
        self.chk_cruisecontrol.setObjectName(_fromUtf8("chk_cruisecontrol"))
        self.chk_startstop = QtGui.QCheckBox(self.groupBox)
        self.chk_startstop.setEnabled(True)
        self.chk_startstop.setGeometry(QtCore.QRect(120, 45, 106, 20))
        self.chk_startstop.setObjectName(_fromUtf8("chk_startstop"))
        self.chk_preheat = QtGui.QCheckBox(self.groupBox)
        self.chk_preheat.setEnabled(True)
        self.chk_preheat.setGeometry(QtCore.QRect(120, 70, 106, 20))
        self.chk_preheat.setObjectName(_fromUtf8("chk_preheat"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_2.setEnabled(True)
        self.groupBox_2.setGeometry(QtCore.QRect(285, 10, 276, 271))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.chk_brake = QtGui.QCheckBox(self.groupBox_2)
        self.chk_brake.setEnabled(True)
        self.chk_brake.setGeometry(QtCore.QRect(10, 20, 81, 20))
        self.chk_brake.setObjectName(_fromUtf8("chk_brake"))
        self.chk_water_level = QtGui.QCheckBox(self.groupBox_2)
        self.chk_water_level.setEnabled(True)
        self.chk_water_level.setGeometry(QtCore.QRect(10, 45, 91, 20))
        self.chk_water_level.setObjectName(_fromUtf8("chk_water_level"))
        self.chk_oil_pressure = QtGui.QCheckBox(self.groupBox_2)
        self.chk_oil_pressure.setEnabled(True)
        self.chk_oil_pressure.setGeometry(QtCore.QRect(10, 70, 91, 20))
        self.chk_oil_pressure.setObjectName(_fromUtf8("chk_oil_pressure"))
        self.chk_engine = QtGui.QCheckBox(self.groupBox_2)
        self.chk_engine.setEnabled(True)
        self.chk_engine.setGeometry(QtCore.QRect(10, 95, 81, 20))
        self.chk_engine.setObjectName(_fromUtf8("chk_engine"))
        self.chk_tempsignal = QtGui.QCheckBox(self.groupBox_2)
        self.chk_tempsignal.setEnabled(True)
        self.chk_tempsignal.setGeometry(QtCore.QRect(120, 20, 101, 20))
        self.chk_tempsignal.setCheckable(True)
        self.chk_tempsignal.setObjectName(_fromUtf8("chk_tempsignal"))
        self.chk_battery = QtGui.QCheckBox(self.groupBox_2)
        self.chk_battery.setEnabled(True)
        self.chk_battery.setGeometry(QtCore.QRect(120, 45, 101, 20))
        self.chk_battery.setCheckable(True)
        self.chk_battery.setObjectName(_fromUtf8("chk_battery"))
        self.chk_gas = QtGui.QCheckBox(self.groupBox_2)
        self.chk_gas.setEnabled(True)
        self.chk_gas.setGeometry(QtCore.QRect(120, 70, 81, 20))
        self.chk_gas.setObjectName(_fromUtf8("chk_gas"))
        self.chk_dpf = QtGui.QCheckBox(self.groupBox_2)
        self.chk_dpf.setEnabled(True)
        self.chk_dpf.setGeometry(QtCore.QRect(120, 95, 101, 20))
        self.chk_dpf.setObjectName(_fromUtf8("chk_dpf"))
        self.chk_esp = QtGui.QCheckBox(self.groupBox_2)
        self.chk_esp.setEnabled(True)
        self.chk_esp.setGeometry(QtCore.QRect(10, 120, 81, 20))
        self.chk_esp.setObjectName(_fromUtf8("chk_esp"))
        self.chk_steering = QtGui.QCheckBox(self.groupBox_2)
        self.chk_steering.setEnabled(True)
        self.chk_steering.setGeometry(QtCore.QRect(120, 120, 101, 20))
        self.chk_steering.setObjectName(_fromUtf8("chk_steering"))
        self.chk_seatbelt = QtGui.QCheckBox(self.groupBox_2)
        self.chk_seatbelt.setEnabled(True)
        self.chk_seatbelt.setGeometry(QtCore.QRect(10, 145, 81, 20))
        self.chk_seatbelt.setObjectName(_fromUtf8("chk_seatbelt"))
        self.chk_airbag = QtGui.QCheckBox(self.groupBox_2)
        self.chk_airbag.setEnabled(True)
        self.chk_airbag.setGeometry(QtCore.QRect(120, 145, 101, 20))
        self.chk_airbag.setObjectName(_fromUtf8("chk_airbag"))
        self.chk_maintance = QtGui.QCheckBox(self.groupBox_2)
        self.chk_maintance.setEnabled(True)
        self.chk_maintance.setGeometry(QtCore.QRect(10, 170, 106, 20))
        self.chk_maintance.setObjectName(_fromUtf8("chk_maintance"))
        self.chk_abs = QtGui.QCheckBox(self.groupBox_2)
        self.chk_abs.setEnabled(True)
        self.chk_abs.setGeometry(QtCore.QRect(120, 170, 101, 20))
        self.chk_abs.setObjectName(_fromUtf8("chk_abs"))
        self.chk_wiper = QtGui.QCheckBox(self.groupBox_2)
        self.chk_wiper.setEnabled(True)
        self.chk_wiper.setGeometry(QtCore.QRect(10, 195, 101, 20))
        self.chk_wiper.setObjectName(_fromUtf8("chk_wiper"))
        self.chk_tires = QtGui.QCheckBox(self.groupBox_2)
        self.chk_tires.setEnabled(True)
        self.chk_tires.setGeometry(QtCore.QRect(120, 195, 101, 20))
        self.chk_tires.setObjectName(_fromUtf8("chk_tires"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 200, 266, 80))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.chk_door = QtGui.QCheckBox(self.groupBox_4)
        self.chk_door.setEnabled(True)
        self.chk_door.setGeometry(QtCore.QRect(15, 20, 81, 20))
        self.chk_door.setObjectName(_fromUtf8("chk_door"))
        self.chk_rest = QtGui.QCheckBox(self.groupBox_4)
        self.chk_rest.setEnabled(True)
        self.chk_rest.setGeometry(QtCore.QRect(15, 45, 106, 20))
        self.chk_rest.setObjectName(_fromUtf8("chk_rest"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.label_17 = QtGui.QLabel(self.tab_4)
        self.label_17.setGeometry(QtCore.QRect(10, 25, 306, 16))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.inp_intervall_speed = QtGui.QLineEdit(self.tab_4)
        self.inp_intervall_speed.setGeometry(QtCore.QRect(385, 20, 81, 22))
        self.inp_intervall_speed.setText(_fromUtf8(""))
        self.inp_intervall_speed.setObjectName(_fromUtf8("inp_intervall_speed"))
        self.label_18 = QtGui.QLabel(self.tab_4)
        self.label_18.setGeometry(QtCore.QRect(10, 55, 216, 16))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.chk_speedimpuls = QtGui.QCheckBox(self.tab_4)
        self.chk_speedimpuls.setGeometry(QtCore.QRect(385, 55, 81, 20))
        self.chk_speedimpuls.setChecked(True)
        self.chk_speedimpuls.setObjectName(_fromUtf8("chk_speedimpuls"))
        self.groupBox_3 = QtGui.QGroupBox(self.tab_4)
        self.groupBox_3.setGeometry(QtCore.QRect(5, 80, 536, 81))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.rbn_loglevel_error = QtGui.QRadioButton(self.groupBox_3)
        self.rbn_loglevel_error.setGeometry(QtCore.QRect(105, 30, 81, 20))
        self.rbn_loglevel_error.setObjectName(_fromUtf8("rbn_loglevel_error"))
        self.rbn_loglevel_warning = QtGui.QRadioButton(self.groupBox_3)
        self.rbn_loglevel_warning.setGeometry(QtCore.QRect(180, 30, 81, 20))
        self.rbn_loglevel_warning.setObjectName(_fromUtf8("rbn_loglevel_warning"))
        self.rbn_loglevel_info = QtGui.QRadioButton(self.groupBox_3)
        self.rbn_loglevel_info.setGeometry(QtCore.QRect(280, 30, 81, 20))
        self.rbn_loglevel_info.setObjectName(_fromUtf8("rbn_loglevel_info"))
        self.rbn_loglevel_debug = QtGui.QRadioButton(self.groupBox_3)
        self.rbn_loglevel_debug.setGeometry(QtCore.QRect(350, 30, 81, 20))
        self.rbn_loglevel_debug.setObjectName(_fromUtf8("rbn_loglevel_debug"))
        self.rbn_loglevel_critical = QtGui.QRadioButton(self.groupBox_3)
        self.rbn_loglevel_critical.setGeometry(QtCore.QRect(20, 30, 81, 20))
        self.rbn_loglevel_critical.setObjectName(_fromUtf8("rbn_loglevel_critical"))
        self.rbn_loglevel_notset = QtGui.QRadioButton(self.groupBox_3)
        self.rbn_loglevel_notset.setGeometry(QtCore.QRect(435, 30, 81, 20))
        self.rbn_loglevel_notset.setChecked(True)
        self.rbn_loglevel_notset.setObjectName(_fromUtf8("rbn_loglevel_notset"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.btn_command = QtGui.QPushButton(self.tab_5)
        self.btn_command.setGeometry(QtCore.QRect(470, 20, 71, 23))
        self.btn_command.setObjectName(_fromUtf8("btn_command"))
        self.inp_commandid = QtGui.QLineEdit(self.tab_5)
        self.inp_commandid.setGeometry(QtCore.QRect(350, 20, 51, 21))
        self.inp_commandid.setObjectName(_fromUtf8("inp_commandid"))
        self.commandlist = QtGui.QListWidget(self.tab_5)
        self.commandlist.setEnabled(False)
        self.commandlist.setGeometry(QtCore.QRect(10, 50, 531, 241))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.commandlist.setFont(font)
        self.commandlist.setObjectName(_fromUtf8("commandlist"))
        self.inp_commandvalue = QtGui.QLineEdit(self.tab_5)
        self.inp_commandvalue.setGeometry(QtCore.QRect(408, 20, 51, 21))
        self.inp_commandvalue.setObjectName(_fromUtf8("inp_commandvalue"))
        self.tabWidget.addTab(self.tab_5, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.lstfile = QtGui.QListWidget(self.tab_3)
        self.lstfile.setGeometry(QtCore.QRect(10, 10, 271, 251))
        self.lstfile.setObjectName(_fromUtf8("lstfile"))
        self.btn_stop = QtGui.QPushButton(self.tab_3)
        self.btn_stop.setEnabled(True)
        self.btn_stop.setGeometry(QtCore.QRect(40, 270, 26, 28))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(True)
        font.setWeight(75)
        self.btn_stop.setFont(font)
        self.btn_stop.setObjectName(_fromUtf8("btn_stop"))
        self.btn_play = QtGui.QPushButton(self.tab_3)
        self.btn_play.setGeometry(QtCore.QRect(10, 270, 26, 28))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setBold(True)
        font.setWeight(75)
        self.btn_play.setFont(font)
        self.btn_play.setObjectName(_fromUtf8("btn_play"))
        self.lstcontent = QtGui.QListWidget(self.tab_3)
        self.lstcontent.setGeometry(QtCore.QRect(295, 10, 266, 251))
        self.lstcontent.setObjectName(_fromUtf8("lstcontent"))
        self.progressfile = QtGui.QProgressBar(self.tab_3)
        self.progressfile.setGeometry(QtCore.QRect(150, 270, 406, 26))
        self.progressfile.setProperty("value", 0)
        self.progressfile.setObjectName(_fromUtf8("progressfile"))
        self.chk_repeat = QtGui.QCheckBox(self.tab_3)
        self.chk_repeat.setGeometry(QtCore.QRect(75, 275, 81, 20))
        self.chk_repeat.setObjectName(_fromUtf8("chk_repeat"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.btn_change_gauge = QtGui.QPushButton(self.centralwidget)
        self.btn_change_gauge.setGeometry(QtCore.QRect(375, 340, 66, 28))
        self.btn_change_gauge.setObjectName(_fromUtf8("btn_change_gauge"))
        self.btn_ping = QtGui.QPushButton(self.centralwidget)
        self.btn_ping.setGeometry(QtCore.QRect(305, 340, 66, 28))
        self.btn_ping.setObjectName(_fromUtf8("btn_ping"))
        self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(590, 20, 231, 381))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.label_19 = QtGui.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(10, 20, 111, 21))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.lbl_fps = QtGui.QLabel(self.groupBox_5)
        self.lbl_fps.setGeometry(QtCore.QRect(110, 20, 111, 21))
        self.lbl_fps.setObjectName(_fromUtf8("lbl_fps"))
        self.label_20 = QtGui.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(10, 43, 46, 20))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.lbl_loglevel = QtGui.QLabel(self.groupBox_5)
        self.lbl_loglevel.setGeometry(QtCore.QRect(110, 40, 111, 20))
        self.lbl_loglevel.setObjectName(_fromUtf8("lbl_loglevel"))
        self.label_21 = QtGui.QLabel(self.groupBox_5)
        self.label_21.setGeometry(QtCore.QRect(10, 66, 71, 20))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.lbl_servername = QtGui.QLabel(self.groupBox_5)
        self.lbl_servername.setGeometry(QtCore.QRect(110, 62, 111, 21))
        self.lbl_servername.setObjectName(_fromUtf8("lbl_servername"))
        self.label_22 = QtGui.QLabel(self.groupBox_5)
        self.label_22.setGeometry(QtCore.QRect(10, 90, 71, 16))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.lbl_serveraddress = QtGui.QLabel(self.groupBox_5)
        self.lbl_serveraddress.setGeometry(QtCore.QRect(110, 86, 111, 20))
        self.lbl_serveraddress.setObjectName(_fromUtf8("lbl_serveraddress"))
        self.label_23 = QtGui.QLabel(self.groupBox_5)
        self.label_23.setGeometry(QtCore.QRect(10, 110, 81, 20))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.lbl_serverport = QtGui.QLabel(self.groupBox_5)
        self.lbl_serverport.setGeometry(QtCore.QRect(110, 110, 46, 16))
        self.lbl_serverport.setObjectName(_fromUtf8("lbl_serverport"))
        self.label_24 = QtGui.QLabel(self.groupBox_5)
        self.label_24.setGeometry(QtCore.QRect(10, 133, 91, 20))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.lbl_clientaddress = QtGui.QLabel(self.groupBox_5)
        self.lbl_clientaddress.setGeometry(QtCore.QRect(110, 130, 46, 21))
        self.lbl_clientaddress.setObjectName(_fromUtf8("lbl_clientaddress"))
        self.label_25 = QtGui.QLabel(self.groupBox_5)
        self.label_25.setGeometry(QtCore.QRect(10, 153, 91, 20))
        self.label_25.setObjectName(_fromUtf8("label_25"))
        self.lbl_clientport = QtGui.QLabel(self.groupBox_5)
        self.lbl_clientport.setGeometry(QtCore.QRect(110, 153, 111, 20))
        self.lbl_clientport.setObjectName(_fromUtf8("lbl_clientport"))
        self.btn_stopserver = QtGui.QPushButton(self.centralwidget)
        self.btn_stopserver.setEnabled(False)
        self.btn_stopserver.setGeometry(QtCore.QRect(220, 340, 81, 31))
        self.btn_stopserver.setObjectName(_fromUtf8("btn_stopserver"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "i-sig 1.0 client", None))
        self.message.setText(_translate("MainWindow", "message", None))
        self.btn_connect.setText(_translate("MainWindow", "connect", None))
        self.btn_quit.setText(_translate("MainWindow", "quit client", None))
        self.txt_speed.setText(_translate("MainWindow", "0", None))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\">(km/h)</span></p></body></html>", None))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">drive</span></p></body></html>", None))
        self.label_16.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">consumption</span></p></body></html>", None))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\"> (°C)</span></p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">oil</span></p></body></html>", None))
        self.label_10.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\">(liter)</span></p></body></html>", None))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\">(rpm)</span></p></body></html>", None))
        self.btn_speed_down.setText(_translate("MainWindow", "-", None))
        self.label_14.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\">(volt)</span></p></body></html>", None))
        self.btn_speed_up.setText(_translate("MainWindow", "+", None))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">gas</span></p></body></html>", None))
        self.label_11.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">oil</span></p></body></html>", None))
        self.label_13.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">voltage</span></p></body></html>", None))
        self.label_15.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\">(l/100km)</span></p></body></html>", None))
        self.label_7.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\"> (°C)</span></p></body></html>", None))
        self.label_12.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:6pt;\">(bar)</span></p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-weight:600;\">water</span></p></body></html>", None))
        self.btn_watertemp_down.setText(_translate("MainWindow", "-", None))
        self.btn_watertemp_up.setText(_translate("MainWindow", "+", None))
        self.btn_oiltemp_down.setText(_translate("MainWindow", "-", None))
        self.btn_oiltemp_up.setText(_translate("MainWindow", "+", None))
        self.btn_drive_down.setText(_translate("MainWindow", "-", None))
        self.btn_drive_up.setText(_translate("MainWindow", "+", None))
        self.txt_watertemp.setText(_translate("MainWindow", "0", None))
        self.txt_oiltemp.setText(_translate("MainWindow", "0", None))
        self.txt_drive.setText(_translate("MainWindow", "0", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "values", None))
        self.groupBox.setTitle(_translate("MainWindow", "info", None))
        self.chk_blink_l.setText(_translate("MainWindow", "Blink left", None))
        self.chk_blink_r.setText(_translate("MainWindow", "Blink right", None))
        self.chk_highbeam.setText(_translate("MainWindow", "highbeam", None))
        self.chk_foglight.setText(_translate("MainWindow", "fog lights", None))
        self.chk_lowbeam.setText(_translate("MainWindow", "lowbeam", None))
        self.chk_cruisecontrol.setText(_translate("MainWindow", "cruise control", None))
        self.chk_startstop.setText(_translate("MainWindow", "start / stop", None))
        self.chk_preheat.setText(_translate("MainWindow", "preheat", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "error / warning", None))
        self.chk_brake.setText(_translate("MainWindow", "brake", None))
        self.chk_water_level.setText(_translate("MainWindow", "water level", None))
        self.chk_oil_pressure.setText(_translate("MainWindow", "oil pressure", None))
        self.chk_engine.setText(_translate("MainWindow", "engine", None))
        self.chk_tempsignal.setText(_translate("MainWindow", "temperature", None))
        self.chk_battery.setText(_translate("MainWindow", "battery", None))
        self.chk_gas.setText(_translate("MainWindow", "gas", None))
        self.chk_dpf.setText(_translate("MainWindow", "dpf", None))
        self.chk_esp.setText(_translate("MainWindow", "esp", None))
        self.chk_steering.setText(_translate("MainWindow", "steering", None))
        self.chk_seatbelt.setText(_translate("MainWindow", "seatbelt", None))
        self.chk_airbag.setText(_translate("MainWindow", "airbag", None))
        self.chk_maintance.setText(_translate("MainWindow", "maintance", None))
        self.chk_abs.setText(_translate("MainWindow", "abs", None))
        self.chk_wiper.setText(_translate("MainWindow", "wiper", None))
        self.chk_tires.setText(_translate("MainWindow", "tires", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "attention", None))
        self.chk_door.setText(_translate("MainWindow", "door", None))
        self.chk_rest.setText(_translate("MainWindow", "rest", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "signals", None))
        self.label_17.setText(_translate("MainWindow", "Intervall Geschwindigkeitsimpuls in Millisekunden", None))
        self.label_18.setText(_translate("MainWindow", "Lieferung Geschwindigkeitsimpuls", None))
        self.chk_speedimpuls.setText(_translate("MainWindow", "on/off", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Debuglevel", None))
        self.rbn_loglevel_error.setText(_translate("MainWindow", "Error", None))
        self.rbn_loglevel_warning.setText(_translate("MainWindow", "Warning", None))
        self.rbn_loglevel_info.setText(_translate("MainWindow", "Info", None))
        self.rbn_loglevel_debug.setText(_translate("MainWindow", "Debug", None))
        self.rbn_loglevel_critical.setText(_translate("MainWindow", "Critical", None))
        self.rbn_loglevel_notset.setText(_translate("MainWindow", "not set", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "config", None))
        self.btn_command.setText(_translate("MainWindow", "send", None))
        self.btn_command.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "command", None))
        self.btn_stop.setText(_translate("MainWindow", "II", None))
        self.btn_play.setText(_translate("MainWindow", ">", None))
        self.chk_repeat.setText(_translate("MainWindow", "repeat", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "file", None))
        self.btn_change_gauge.setText(_translate("MainWindow", "change", None))
        self.btn_ping.setText(_translate("MainWindow", "ping", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "processdata (server)", None))
        self.label_19.setText(_translate("MainWindow", "frames / sec", None))
        self.lbl_fps.setText(_translate("MainWindow", "./.", None))
        self.label_20.setText(_translate("MainWindow", "Loglevel", None))
        self.lbl_loglevel.setText(_translate("MainWindow", "./.", None))
        self.label_21.setText(_translate("MainWindow", "servername", None))
        self.lbl_servername.setText(_translate("MainWindow", "./.", None))
        self.label_22.setText(_translate("MainWindow", "serveraddress", None))
        self.lbl_serveraddress.setText(_translate("MainWindow", "./.", None))
        self.label_23.setText(_translate("MainWindow", "serverport", None))
        self.lbl_serverport.setText(_translate("MainWindow", "./.", None))
        self.label_24.setText(_translate("MainWindow", "clientaddress", None))
        self.lbl_clientaddress.setText(_translate("MainWindow", "./.", None))
        self.label_25.setText(_translate("MainWindow", "clientport", None))
        self.lbl_clientport.setText(_translate("MainWindow", "./.", None))
        self.btn_stopserver.setText(_translate("MainWindow", "Stop Server", None))
