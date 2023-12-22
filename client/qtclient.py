__author__ = 'JK'

from PyQt5.QtWidgets import QApplication
from networkclient import NetworkClient
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from threading import Thread
from timing import *
from tools import *
from messagehelper import *
from settings import *

import sys
import pygame
import obd

global app

# noinspection PyUnresolvedReferences,PyPep8Naming

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("qtdesign.ui", self)
        #self.setupUi(self)
        self.nc = NetworkClient()
        self.connectionestablished = False
        self.sendspeedimpuls = True
        self.speedimpulsintervall = 500
        self.sim_repeat = False
        self.speed_value = 0
        self.ProcessServerRunning = True
        self.IntervallServerRunning = True
        self.attempt2connect = False
        self.id1 = None
        self.id2 = None
        self.id3 = None
        self.actualSimData = None

        self.sl_speed.valueChanged.connect(self.sendspeed)
        self.sl_temp.valueChanged.connect(lambda: self.sendValue(self.sl_temp, self.txt_watertemp, ID_TEMPW))
        self.sl_temp_o.valueChanged.connect(lambda: self.sendValue(self.sl_temp_o, self.txt_oiltemp, ID_TEMPO))
        self.sl_drive.valueChanged.connect(lambda: self.sendValue(self.sl_drive, self.txt_drive, ID_DRIVE))

        self.chk_blink_l.clicked.connect(lambda: self.sendSignal(self.chk_blink_l, ID_BLINKL))
        self.chk_blink_r.clicked.connect(lambda: self.sendSignal(self.chk_blink_r, ID_BLINKR))
        self.chk_highbeam.clicked.connect(lambda: self.sendSignal(self.chk_highbeam,ID_HIGHBEAM))
        self.chk_lowbeam.clicked.connect(lambda: self.sendSignal(self.chk_lowbeam,ID_LOWBEAM))
        self.chk_foglight.clicked.connect(lambda: self.sendSignal(self.chk_foglight, ID_FOGLIGHT))
        self.chk_preheat.clicked.connect(lambda: self.sendSignal( self.chk_preheat, ID_PREHEAT))
        self.chk_cruisecontrol.clicked.connect(lambda: self.sendSignal( self.chk_cruisecontrol, ID_CRUISECONTROL))
        self.chk_startstop.clicked.connect(lambda: self.sendSignal( self.chk_startstop, ID_STARTSTOP))
        self.chk_tempsignal.clicked.connect(lambda: self.sendSignal( self.chk_tempsignal, ID_TEMPSIG))
        self.chk_battery.clicked.connect(lambda: self.sendSignal( self.chk_battery, ID_BATTERY))
        self.chk_engine.clicked.connect(lambda: self.sendSignal( self.chk_engine, ID_ENGINE))
        self.chk_gas.clicked.connect(lambda: self.sendSignal( self.chk_gas, ID_GAS))
        self.chk_oil_pressure.clicked.connect(lambda: self.sendSignal( self.chk_oil_pressure, ID_OILPRESSURE))
        self.chk_brake.clicked.connect(lambda: self.sendSignal( self.chk_brake, ID_BRAKE))
        self.chk_foglight.clicked.connect(lambda: self.sendSignal( self.chk_foglight, ID_FOGLIGHT))
        self.chk_water_level.clicked.connect(lambda: self.sendSignal( self.chk_water_level, ID_WATER))
        self.chk_maintance.clicked.connect(lambda: self.sendSignal( self.chk_maintance, ID_MAINTANCE))
        self.chk_dpf.clicked.connect(lambda: self.sendSignal( self.chk_dpf, ID_DPF))
        self.chk_esp.clicked.connect(lambda: self.sendSignal( self.chk_esp, ID_ESP))
        self.chk_door.clicked.connect(lambda: self.sendSignal( self.chk_door, ID_DOOR))
        self.chk_rest.clicked.connect(lambda: self.sendSignal( self.chk_rest, ID_REST))
        self.chk_steering.clicked.connect(lambda: self.sendSignal( self.chk_steering, ID_STEERING))
        self.chk_airbag.clicked.connect(lambda: self.sendSignal( self.chk_airbag, ID_AIRBAG))
        self.chk_seatbelt.clicked.connect(lambda: self.sendSignal( self.chk_seatbelt, ID_SEATBELT))
        self.chk_abs.clicked.connect(lambda: self.sendSignal( self.chk_abs, ID_ABS))
        self.chk_wiper.clicked.connect(lambda: self.sendSignal( self.chk_wiper, ID_WIPER))
        self.chk_tires.clicked.connect(lambda: self.sendSignal( self.chk_tires, ID_TIRES))

        self.chk_speedimpuls.stateChanged.connect(self.speedimpuls)
        self.chk_repeat.stateChanged.connect(self.simulationrepeat)

        self.btn_obdConnect.clicked.connect(self.obdactivate)
        self.chk_obdFast.clicked.connect(self.obdfast)
        self.chk_obdLowPower.clicked.connect(self.obdlowpower)
        self.inp_obdTimeout.textEdited.connect(self.obdtimeout)
        #self.com_obdserial.stateChanged.connect(self.obdserial)

        self.rbn_loglevel_critical.clicked.connect(lambda: self.setLogLevel(LOGLEVEL_CRITICAL))
        self.rbn_loglevel_error.clicked.connect(lambda: self.setLogLevel(LOGLEVEL_ERROR))
        self.rbn_loglevel_warning.clicked.connect(lambda: self.setLogLevel(LOGLEVEL_WARNING))
        self.rbn_loglevel_info.clicked.connect(lambda: self.setLogLevel(LOGLEVEL_INFO))
        self.rbn_loglevel_debug.clicked.connect(lambda: self.setLogLevel(LOGLEVEL_DEBUG))
        self.rbn_loglevel_notset.clicked.connect(lambda: self.setLogLevel(LOGLEVEL_NOTSET))

        self.btn_connect.clicked.connect(self.connectServer)
        self.btn_change_gauge.clicked.connect(self.changegauge)
        self.btn_speed_up.clicked.connect(self.speedup)
        self.btn_speed_down.clicked.connect(self.speeddown)
        self.btn_quit.clicked.connect(self.exit)
        self.btn_stopserver.clicked.connect(self.stopServer)
        self.btn_ping.clicked.connect(self.sendPing)
        self.btn_play.clicked.connect(self.play)
        self.btn_command.clicked.connect(self.command)
        #self.btn_load.clicked.connect(self.load)

        self.inp_intervall_speed.textEdited.connect(self.intervallspeed)
        self.inp_intervall_speed.setText(str(self.speedimpulsintervall))

        self.lstfile.clicked.connect(self.printfile)
#        self.btn_watertemp_up.clicked.connect(self.watertempup)
#        self.btn_watertemp_down.clicked.connect(self.watertempdown)
#        self.btn_oiltemp_up.clicked.connect(self.oiltempup)
#        self.btn_oiltemp_down.clicked.connect(self.oiltempdown)

        self.setState(self.btn_play,False)
        self.setState(self.btn_stop,False)

        self.startIntervallServer()
        self.startProcessServer()
        self.loadfilelist(g_sim)
        self.show()

        self.starttime = getLocalTime()
        self.startingTime = micros()
        self.mh = MessageHelper()

        self.obdinit()
        # self.initialize()

    def initialize(self):
        # Loglevels uebertragen
        if self.rbn_loglevel_debug.isChecked() == True:
            self.setLogLevel(LOGLEVEL_DEBUG)
        elif self.rbn_loglevel_info.isChecked() == True:
            self.setLogLevel(LOGLEVEL_INFO)
        elif self.rbn_loglevel_warning.isChecked() == True:
            self.setLogLevel(LOGLEVEL_WARNING)
        elif self.rbn_loglevel_error.isChecked() == True:
            self.setLogLevel(LOGLEVEL_ERROR)
        elif self.rbn_loglevel_critical.isChecked() == True:
            self.setLogLevel(LOGLEVEL_CRITICAL)
        elif self.rbn_loglevel_notset.isChecked() == True:
            self.setLogLevel(LOGLEVEL_NOTSET)

        # Hostadress abfragen:
        self.sendMessage(ID_SERVERNAME,'')
        self.sendMessage(ID_SERVERADR,'')
        self.sendMessage(ID_SERVERPORT,'')
        self.sendMessage(ID_CLIENTADR,'')
        self.sendMessage(ID_CLIENTPORT,'')
        self.sendMessage(ID_LOGLEVEL,'')
        self.sendMessage(ID_FRAMERATE,'')

    def command(self):
        id = str(self.inp_commandid.text())
        value =str(self.inp_commandvalue.text())
        self.sendMessage(id, value)

    def simrepeat(self):
        while self.sim_repeat == True:
            self.playfile()

    def play(self):
        if self.sim_repeat == True:
            self.simrepeat()
        else:
            self.playfile()

    def playfile(self):

        index = self.lstcontent.model().index(0,0)
        self.lstcontent.setCurrentIndex(index)

        lasttime = 0
        row = 0
        for entry in self.actualSimData:
            row = row + 1
            time = int(entry[0])
            waittime = time - lasttime
            pygame.time.delay(waittime)
            lasttime = time

            qApp.processEvents()

            for i in range(1, len(entry)):
                message = entry[i]
                entries = message.split("=")
                self.sendMessage(entries[0], entries[1])
                self.progressfile.setValue(row)


    def setState(self, object, state=True):
        object.setEnabled(state)

    def printfile(self):
        zeilen=0
        entry = self.lstfile.currentItem().text()
        self.message.setText(str(entry))
        filename = g_sim + entry
        file = open(filename, 'r')
        self.lstcontent.clear()
        self.actualSimData = []
        for line in file:
            zeilen = zeilen + 1
            line = line.rstrip()
            line = line.rstrip(";")
            self.lstcontent.addItem(line)
            eintrag = line.split(";")
            self.actualSimData.append(eintrag)
        file.close()

        index = self.lstcontent.model().index(0,0)
        self.progressfile.setMaximum(zeilen)
        self.progressfile.setMinimum(0)
        self.progressfile.setValue(0)
        self.lstcontent.setCurrentIndex(index)
        self.setState(self.btn_play,True)
        self.setState(self.btn_stop,True)


    def loadfilelist(self,path):
        for filename in os.listdir(path):
            if os.path.isfile(os.path.join(path, filename)):
                self.lstfile.addItem(filename)

    def sendSignal(self, signalobject, identifier):
        if signalobject.isChecked():
            self.sendMessage(identifier, ID_ON)
        elif not signalobject.isChecked():
            self.sendMessage(identifier, ID_OFF)

    def sendValue(self, valueobject, txtobject, identifier):
        value = valueobject.value()
        txtobject.setText(str(value))
        logger.debug("ID: %s , sendValue: %s ", identifier, value)
        self.sendMessage(identifier, value)

    def changegauge(self):
        self.sendMessage(ID_INNERDASH, ID_INCREASE)

    def setLogLevel(self, loglevel):
        self.sendMessage(ID_LOGLEVEL,loglevel)
        logger.setLevel(loglevel)

    # ------------------------ OBD ------------------------------
    def obdinit(self):
        # obd Ports
        ports = obd.scan_serial()
        logger.debug("OBD Ports %s:",ports)
        self.com_obdSerial.clear()
        self.com_obdSerial.addItems(ports)

        # obd Baudrate
        self.com_obdBaudrate.clear()
        baudrates = ["Auto","9600","19200","38400","57600","115200"]
        self.com_obdBaudrate.addItems(baudrates)

        # obd Protokoll
        protokolls = ["1 SAE J1850 PWM",
                      "2 SAE J1850 VPW",
                      "3 AUTO ISO 9141-2",
                      "4 ISO 14230-4 (KWP 5BAUD)",
                      "5 ISO 14230-4 (KWP FAST)",
                      "6 ISO 15765-4 (CAN 11/500)",
                      "7 ISO 15765-4 (CAN 29/500)",
                      "8 ISO 15765-4 (CAN 11/250)",
                      "9 ISO 15765-4 (CAN 29/250)",
                      "A SAE J1939 /CAN 29/250)"]
        self.com_obdProtokoll.addItems(protokolls)

        # obd Fast
        # --
        return True

        #com_obdserial.addItems (ports)

    def obdactivate(self):
        port = self.com_obdSerial.currentText()
        baudrate = self.com_obdBaudrate.currentText()
        protokol = self.com_obdProtokoll.currentText()

        if self.chk_obdFast.isChecked() == True:
            fast = "True"
        else:
            fast = "False"

        timeout = self.inp_obdTimeout.text()

        if self.chk_obdLowPower.isChecked() == True:
            lowpower = "True"
        else:
            lowpower = "False"

        if self.chk_obdVoltage.isChecked() == True:
            voltage = "True"
        else:
            voltage = "False"

        item = '---------- Connect Parameter ---------- '
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'Port : ' + port
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'Baudrate : ' + baudrate
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'Protokol : ' + protokol
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'Fast Option : ' + fast
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'Timeout : ' + timeout
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'Low Power Option : ' + lowpower
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        item = 'check Voltage Option : ' + voltage
        self.lst_obdOutput.addItem(item)
        self.lst_obdOutput.repaint()
        self.lst_obdOutput.addItem("    ")
        self.lst_obdOutput.repaint()
        self.lst_obdOutput.addItem("waiting for response ...    ")
        self.lst_obdOutput.repaint()

        if baudrate == "Auto":
            baudrate = None
        strprotokol = str(protokol).split(" ")
        self.lst_obdOutput.repaint()

        connection = obd.OBD("COM3",
                             baudrate,
                             strprotokol[0],
                             self.chk_obdFast.isChecked(),
                             int(timeout),
                             self.chk_obdVoltage.isChecked(),
                             self.chk_obdLowPower.isChecked())
        strstatus = connection.status()
        self.lst_obdOutput.addItem("Status :    " + strstatus)


        #if connection != None:
        #    if connection.status() == OBDStatus.CAR_CONNECTED:
        #        self.lst_obdOutput.addItem("connected !    ")
        #        r = connection.query(obd.commands.RPM)
        #        item = "Drehzahl : " + r
        #        self.lst_obdOutput.addItem(item)
        #    else:
        #        self.lst_obdOutput.addItem("Connection not established")

        return True
    def obdserial(self):
        return True

    def obdfast(self):
        return True

    def obdlowpower(self):
        return True

    def obdtimeout(self):
        return True
    # ----------------------------------------------------------------

    def stopServer(self):
        self.sendMessage(ID_QUIT,False)

    def startIntervallServer(self):
        self.IntervallServerRunning = True
        self.id1 = Thread(target=self.sendintervallspeed)
        self.id1.start()
        logger.debug("run intervall server. id=%s",self.id1)

    def stopIntervallServer(self):
        self.sendspeedimpuls = False
        logger.info("sendspeedimpuls = False")
        self.IntervallServerRunning = False
        logger.info("IntervallServerRunning = False")


        # Intervallserver
        wait = 2 * self.speedimpulsintervall
        pygame.time.wait(wait)
        logger.info("wait %s milliseconds",wait)
        if self.id1 == None:
            logger.info("Intervallserver stopped")
        else:
            logger.info("Intervallserver not stopped")

    def stopProcessServer(self):

        self.sendMessage("KME",'')
        pygame.time.wait(500)
        if self.id3 == None:
            logger.info("Processserver stopped")
        else:
            logger.info("Processserver not stopped")


    def exit(self):
        self.stopIntervallServer()
        self.stopProcessServer()

        # Status zurücksetzen
        self.attempt2connect = False
        logger.info("attempt2connect False")

        self.sim_repeat = False
        logger.info("sim_repeat False")

        logger.info("attempt 2 stop networkclient")
        self.nc.stop()
        logger.info("networkclient stopped")

        self.connectionestablished = False
        logger.info("connectionestablished False")

        self.close()

    def receiveMessages(self):
        if self.connectionestablished == True:
            rawvalue = self.nc.receive()
            if rawvalue != None:
                value = rawvalue.decode("utf-8")
                logger.debug("len(value) = %s", len(value))
                if len(value) == 0:
                    self.connectionestablished = False
                    return None
                messages = self.mh.getallMessages(value)
                if messages is not None:
                    return messages
            else:
                self.connectionestablished = False

    def sendMessage(self, id, value='', receive=False):
        if self.connectionestablished == True:

            message = formatMessageContent(id,value)
            if message != None:
                rc = self.nc.send(message, receive)

                if rc != None:
                    time = micros() - self.startingTime
                    timeentry = getTimeKey(time)
                    listentry = timeentry + ' | ' + str(value) + ' | ' + str(message)
                    self.commandlist.insertItem(0,listentry)
                    self.message.setText("last command: <" + str(message) + "> result=" + str(rc))
                else:
                    logger.warning("Exception occurs. attempt to reset")

                return value
            else:
                logger.error("Message Format error")
        else:
            self.message.setText("no connection. Please connect first")

    def connectServer(self):
        self.btn_connect.setEnabled(False)
        #self.id2 = Thread(target=self.establishConnection)
        #self.id2.start()
        self.establishConnection()


    def startProcessServer(self):
        self.id3 = Thread(target=self.processServerData)
        self.id3.start()
        logger.debug("run process server. id=%s", self.id3)

    def processServerData(self):
        while self.ProcessServerRunning == True:
            if self.connectionestablished == True:
                logger.debug("call receiveMessage")
                messages = self.receiveMessages()
                logger.debug("return from receiveMessages")
                if messages:
                    logger.debug ("message received: %s", messages)
                    for x in range(0,len(messages)):
                        id = messages[x][0]
                        value = messages[x][1]
                        if  id == ID_QUIT:
                            pass
                        elif id == ID_KILLME:
                            self.ProcessServerRunning = False
                        elif id == ID_FRAMERATE:
                            self.lbl_fps.setText(value)
                        elif id == ID_LOGLEVEL:
                            self.lbl_loglevel.setText(value)
                        elif id == ID_SERVERNAME:
                            self.lbl_servername.setText(value)
                        elif id == ID_SERVERADR:
                            self.lbl_serveraddress.setText(value)
                        elif id == ID_SERVERPORT:
                            self.lbl_serverport.setText(value)
                        elif id == ID_CLIENTADR:
                            self.lbl_clientaddress.setText(value)
                        elif id == ID_CLIENTPORT:
                            self.lbl_clientport.setText(value)
                        else:
                            logger.debug("id=%s value=%s",id,value)
                else:
                    # es konnte keine Nachricht aus dem Datenstrom entnommen
                    # werden
                    logger.debug ("no valid message from server")
                    # self.btn_connect.setEnabled(True)
                    # self.running = False
                    # self.connectionestablished = 0
                    # self.message.setText("connection to server lost")
                    #self.connectServer()

        self.id3 = None
        logger.debug("quit process server.")


    def resetConnection(self):
        self.nc.stop()
        self.nc = None
        self.nc = NetworkClient()
        self.connectionestablished = False
        self.attempt2connect = False
        self.connectServer()

    def establishConnection(self):

        if self.attempt2connect == False:
            rc = 1
            rounds = 0
            initial_message = "attempt to connect "
            message = initial_message
            dot = ". "

            if self.connectionestablished == False:
                self.attempt2connect = True

                while ((rc != 0) and (self.attempt2connect == True)):
                    message = message + dot
                    self.message.setText(message)
                    rc = self.nc.connectServer()
                    time.sleep(1)
                    logger.debug("attempt to connect socket. rc=%s",rc)
                    rounds = rounds + 1
                    if rounds > 5:
                        message = initial_message
                        rounds = 0
                        # weil ohne connection macht die Anwendung keinen Sinn

            self.attempt2connect = False
            if rc == 0:
                self.connectionestablished = True
                logger.debug("connection established")
                self.message.setText("connection established")
                self.initialize()
            else:
                self.connectionestablished = False
                self.message.setText("connection error " + str(rc))
                self.resetConnection()

    def sendPing(self):
        received = self.sendMessage("ping",0,True)
        if received is not None:
            if 0 < len(received):
                text = "{server found at: %s}".format(received)
                self.message.setText(text)

    def setValue(self, direction):
        pass

    def speedup(self):
        value = self.sl_speed.value()
        value = value + 1
        self.sl_speed.setValue(value)
        self.sendspeedvalue()

    def speeddown(self):
        value = self.sl_speed.value()
        value = value - 1
        self.sl_speed.setValue(value)
        self.sendspeedvalue()


    def sendintervallspeed(self):
        waittime = self.speedimpulsintervall

        while self.IntervallServerRunning == True:
            pygame.time.wait(waittime)
            if self.connectionestablished == True:

                if self.sendspeedimpuls == True:
                    self.sendMessage(ID_FRAMERATE, '')
                    if self.speed_value > 0:
                        self.sendMessage(ID_SPEED, self.speed_value, False)

        self.id1 = None
        logger.debug("quit intervall server.")

    def intervallspeed(self):
        value = str(self.inp_intervall_speed.text())
        self.speedimpulsintervall = int(value)

    def sendspeed(self):
        self.speed_value = self.sl_speed.value()
        self.sendValue(self.sl_speed, self.txt_speed, ID_SPEED)

    def speedimpuls(self):
        if self.chk_speedimpuls.isChecked():
            self.sendspeedimpuls = True
        else:
            self.sendspeedimpuls = False

    def simulationrepeat(self):
        if self.chk_repeat.isChecked():
            self.sim_repeat = True
        else:
            self.sim_repeat = False

    def closeEvent(self, event):
        app.quit()

def main():
    app = QApplication([])
    #app = QtWidgets.QApplication(sys.argv)'
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()