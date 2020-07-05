import multiprocessing
import os
import socket
import struct
import sys
import threading
import time
from pathlib import Path
from threading import Thread

import pyaudio
from GUI.afterstream import Ui_afterStream
from GUI.configure1 import Ui_conf1_dialog
from GUI.configure2 import Ui_conf2_dialog
from GUI.configure3 import Ui_conf3_dialog
from GUI.earthdrill import Ui_earthquake_dialog
from GUI.filetransfer import Ui_fileTr
from GUI.firedrill import Ui_fire_dialog
from GUI.liveannou import Ui_live_dialog
from GUI.main import Ui_MainWindow
from GUI.onstream import Ui_MainWindow1
from Progress.roleclient.wav_client import Client_wave
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSignal, QRegExp, QObject, QThread, QSettings, pyqtSlot, QTime
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from Progress.Client import Client_Send
from Progress.Client import Live_Client
from Progress.Client2 import Client2_Send


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


# MAINWINDOW
class MyMainWindow(QMainWindow, Ui_MainWindow):
    window1_1 = pyqtSignal()
    window1_2 = pyqtSignal()
    window1_3 = pyqtSignal()
    action_exit = pyqtSignal()

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_1.clicked.connect(self.switch1)
        self.pushButton_2.clicked.connect(self.switch2)
        self.pushButton_3.clicked.connect(self.switch3)
        self.actionExit.triggered.connect(self.switchexit)

        self.settings = QtCore.QSettings()
        try:
            self.resize(self.settings.value('window size'))

        except:
            pass

    def switch1(self):
        self.window1_1.emit()

    def switch2(self):
        self.window1_2.emit()

    def switch3(self):
        self.window1_3.emit()

    def switchexit(self):
        self.action_exit.emit()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        super(MyMainWindow).__init__()


# ONSTREAM WINDOW
class StreamWindow(QtWidgets.QMainWindow, Ui_MainWindow1):
    window2_1 = QtCore.pyqtSignal()
    window2_2 = QtCore.pyqtSignal()
    window2_3 = QtCore.pyqtSignal()
    actionbtn1 = QtCore.pyqtSignal()
    action_exit = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(StreamWindow, self).__init__(parent)

        self.setupUi(self)
        self.pushButton_live.clicked.connect(self.switch1)
        self.pushButton_fire.clicked.connect(self.switch2)
        self.pushButton_earth.clicked.connect(self.switch3)
        self.actionBack.triggered.connect(self.switch4)
        self.actionExit.triggered.connect(self.switchexit)

        self.settings = QtCore.QSettings()
        try:
            self.resize(self.settings.value('window size'))

        except:
            pass

    def switch1(self):
        self.window2_1.emit()

    def switch2(self):
        self.window2_2.emit()

    def switch3(self):
        self.window2_3.emit()

    def switch4(self):
        self.actionbtn1.emit()

    def switchexit(self):
        self.action_exit.emit()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        super(StreamWindow).__init__()


# AFTERSTREAM WINDOW
class StreamWindow1(QtWidgets.QMainWindow, Ui_afterStream):
    switch_window3 = QtCore.pyqtSignal()
    actionbtn = QtCore.pyqtSignal()
    action_exit = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(StreamWindow1, self).__init__(parent)
        self.setupUi(self)
        self.actionBack.triggered.connect(self.switchback)
        self.actionExit.triggered.connect(self.switchexit)

        self.settings = QtCore.QSettings()
        try:
            self.resize(self.settings.value('window size'))

        except:
            pass

    def switchback(self):
        self.actionbtn.emit()

    def switchexit(self):
        self.action_exit.emit()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        super(StreamWindow1).__init__()


# FILE TRANSFER WINDOW
class FileTransferWindow(QtWidgets.QMainWindow, Ui_fileTr):
    actionbtn = QtCore.pyqtSignal()
    action_exit = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(FileTransferWindow, self).__init__(parent)
        self.setupUi(self)
        self.actionBack.triggered.connect(self.switchback)
        self.actionExit.triggered.connect(self.switchexit)

        self.settings = QtCore.QSettings()
        try:
            self.resize(self.settings.value('window size'))

        except:
            print("Error resizing window! ")

    def switchback(self):
        self.actionbtn.emit()

    def switchexit(self):
        self.action_exit.emit()

    def closeEvent(self, event):
        self.settings.setValue('window size', self.size())
        super(FileTransferWindow).__init__()


class Worker(QObject):
    finished = pyqtSignal()
    finished2 = pyqtSignal()
    intReady = pyqtSignal(int)

    @pyqtSlot()
    def procCounter(self):  # A slot takes no params
        for i in range(1, 43000):
            if paused:
                break
            time.sleep(1)
            self.intReady.emit(i)
            i += 1

        self.finished.emit()
        self.finished2.emit()


class Worker_1(QObject):
    finished = pyqtSignal()
    finished2 = pyqtSignal()
    intReady = pyqtSignal(int)

    @pyqtSlot()
    def procCounter_1(self):  # A slot takes no params
        self.settings = QSettings()
        song_dur = self.settings.value("songplay")
        from pydub import AudioSegment
        sound_1 = AudioSegment.from_file(song_dur)
        sound_nsec = sound_1.duration_seconds
        sound_int = int(sound_nsec)
        print(sound_int)
        for i in range(sound_int,-1, -1):
            if paused:
                break
            time.sleep(1)
            self.intReady.emit(i)
        self.finished.emit()
        self.finished2.emit()


paused = False

# ONSTREAM SIDE --------->>>
# Live Announcement on onstream -->
class live_announce(QtWidgets.QDialog, Ui_live_dialog):
    btn1 = pyqtSignal()
    btn2 = pyqtSignal()
    btn3 = pyqtSignal()
    btn4 = pyqtSignal()

    def __init__(self, parent=None):
        super(live_announce, self).__init__(parent)
        self.settings = QtCore.QSettings
        self.setupUi(self)
        self.toolButton_1.clicked.connect(self.switch1)
        self.toolButton_2.clicked.connect(self.switch2)
        self.toolButton_3.clicked.connect(self.switch3)
        self.pushButton7.clicked.connect(self.playing_stream)
        self.pushButton8.clicked.connect(self.stop_live)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.buttonBox.accepted.connect(self.stop_live)
        self.buttonBox.rejected.connect(self.stop_live)
        # self.comboBox_1.connect()
        # self.comboBox_1.currentIndexChanged[int].connect(self.changetext1)
        # self.comboBox_2.currentIndexChanged[int].connect(#)
        # self.comboBox_3.currentIndexChanged[int].connect()
        # self.comboBox_2.model().item(2).setEnabled(False)

        self.obj = Worker()
        self.thread = QThread()
        self.pushButton1.clicked.connect(self.resume_p)
        self.obj.finished2.connect(lambda: self.pushButton7.setEnabled(True))

    def resume_p(self):
        pass

    def stop_live(self):
        global paused
        paused = True
        w = Live_Client.stop_playing(self)


    def switch1(self):
        self.btn1.emit()

    def switch2(self):
        self.btn2.emit()

    def switch3(self):
        self.btn3.emit()

    def switch4(self):
        self.btn4.emit()



    def showTime(self, i):
        # currentTime = QTime.currentTime()
        time_edit = QTime(00, 00, 00)
        # if time_start == True:
        every_1 = time_edit.addSecs(i)
        displayTxt = every_1.toString('hh:mm:ss')
        if paused:
            displayTxt = time_edit.toString('hh:mm:ss')
        # self.label_5.setText(displayTxt)
        self.label_5.setText(
            f"<html><head/><body><p>Record Time:</p><p><span style=\" color:#0000ff;\">{displayTxt}</span></p></body></html>")
        self.label_5.adjustSize()


    def playing_stream(self):
        self.settings = QSettings()
        print("signal hit")
        get_ip1 = self.settings.value("readip")
        get_port1 = self.settings.value("readport")
        if get_port1 != None:
            get_port1 = int(get_port1)
        get_ip2 = self.settings.value("readip2")
        get_port2 = self.settings.value("readport2")
        if get_port2 != None:
            get_port2 = int(get_port2)
        get_ip3 = self.settings.value("readip3")
        get_port3 = self.settings.value("readport3")
        if get_port3 != None:
            get_port3 = int(get_port3)
        if (get_ip1 == None and get_port1 == None) and (get_ip2 == None and get_port2 == None) and (
                get_ip3 == None and get_port3 == None):
            self.play_popup(0)
        else:
            if not self.thread.isRunning():
                self.pushButton7.setEnabled(False)
                global paused
                paused = False

                self.obj.intReady.connect(self.showTime)
                self.obj.moveToThread(self.thread)
                self.obj.finished.connect(self.thread.quit)
                self.thread.started.connect(self.obj.procCounter)
                self.thread.start()

                self.thread1 = QThread()
                self.obj2 = Client_Send(ip=get_ip1, port=get_port1, ip2=get_ip2, port2=get_port2,
                                        ip3=get_ip3, port3=get_port3)
                self.obj2.moveToThread(self.thread1)
                self.obj2.finished1.connect(self.thread1.quit)
                self.thread1.started.connect(self.obj2.running_all)
                self.thread1.start()

            # self.AudioThread = Thread(target=self.record, daemon=True)
            # self.udpThread = Thread(target=self.streaming, daemon=True)
            # self.AudioThread.start()
            # self.udpThread.start()

    def play_popup(self, event):
        msg_text = "Can't start playing, unspecified IP and Port address!"
        QMessageBox.setStyleSheet(self, "QMessageBox, {background-color: rgb(226, 226, 226);}")
        create_popup = QMessageBox.warning(self, "Unable to Play", msg_text, QMessageBox.Ok)
        try:
            if create_popup == QMessageBox.Ok:
                event.accept()
        except:
            pass

    def closeEvent(self, event=None):
        self.stop_live()
        close_message = "Are you sure you want to quit?"
        QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
        create_reply = QMessageBox.question(self, 'Warning', close_message,
                                            QMessageBox.Yes | QMessageBox.No)

        if create_reply == QMessageBox.Yes:
            event.accept()
            global paused
            paused = True
        else:
            event.ignore()


client_connect = True


# FireDrill ---->
class FireDrill1(QtWidgets.QDialog, Ui_fire_dialog):
    swt1 = pyqtSignal()
    swt2 = pyqtSignal()
    swt3 = pyqtSignal()

    def __init__(self, parent=None):
        super(FireDrill1, self).__init__(parent)
        self.setupUi(self)
        self.toolButton1.clicked.connect(self.switch1)
        self.toolButton2.clicked.connect(self.switch2)
        self.toolButton_2.clicked.connect(self.switch3)
        # self.comboBox_1.removeItem(0)
        # self.comboBox_1.removeItem(1)
        # self.comboBox_1.removeItem(2)
        text1 = self.comboBox.activated[str].connect(self.open_file)
        self.settings = QSettings()
        self.songs_list = self.settings.value("songlist")
        self.song_list_loc = []
        self.new_list = []
        self.dict_song = self.settings.value("songdict")
        print(self.dict_song)
        self.pick_list = {}
        self.read_setting()
        self.label_txt = QtWidgets.QLabel(self.splitter_2)
        self.label_txt.setObjectName("label_txt")
        self.label_txt.setText("Playing time:")
        self.label_time = QtWidgets.QLabel(self.splitter_2)
        self.label_time.setObjectName("label_time")
        self.label_time.setText("00:00:00")
        self.label_time.setStyleSheet("color: rgb(0, 0, 255);")

        self.pushButton7.clicked.connect(self.play_button)
        self.pushButton8.clicked.connect(self.stop_button)

        self.buttonBox.accepted.connect(self.stop_button)
        self.buttonBox.rejected.connect(self.stop_button)
        self.obj = Worker_1()
        self.thread = QThread()
        self.obj.finished2.connect(lambda: self.pushButton7.setEnabled(True))



        # ------------------------
        # initialize socket
        # self.socket_gui = None
        # self.settings = QtCore.QSettings()
        # self.host_1 = self.settings.value("readip00")
        # self.port_1 = self.settings.value('readport00')
        # self.host_2 = self.settings.value("readip01")
        # self.port_2 = self.settings.value('readport01')
        # self.host_3 = self.settings.value("readip02")
        # self.port_3 = self.settings.value('readport02')
        #
        # hostname = socket.gethostname()
        # self.host = '127.0.0.1'
        #     # socket.gethostbyname(hostname)
        # self.port = 12345
        #
        # self.all_connections = []
        # self.all_addresses = []

    def switch1(self):
        self.swt1.emit()

    def switch2(self):
        self.swt2.emit()

    def switch3(self):
        self.swt3.emit()

    def stop_button(self):
        global paused
        paused = True
        time_edit = QTime(00, 00, 00)
        glob_pause = Client_wave.stop_play(self)

        # displayTxt = time_edit.toString('hh:mm:ss')

    def showTime(self, i):
        # currentTime = QTime.currentTime()
        time_edit = QTime(00, 00, 00)
        every_1 = time_edit.addSecs(i)
        displayTxt = every_1.toString('hh:mm:ss')
        if paused:
            displayTxt = time_edit.toString('hh:mm:ss')
        self.label_time.setText(displayTxt)
        self.label_time.adjustSize()

    def play_button(self):
        self.settings = QSettings()
        print("signal hit")
        self.get_ip1 = self.settings.value("readip00")
        self.get_port1 = self.settings.value("readport00")
        if self.get_port1 is not None:
            self.get_port1 = int(self.get_port1)
        self.get_ip2 = self.settings.value("readip01")
        self.get_port2 = self.settings.value("readport01")
        if self.get_port2 is not None:
            self.get_port2 = int(self.get_port2)
        self.get_ip3 = self.settings.value("readip02")
        self.get_port3 = self.settings.value("readport02")
        if self.get_port3 is not None:
            self.get_port3 = int(self.get_port3)
        song_name = self.settings.value("songplay")
        if (self.get_ip1 is None and self.get_port1 is None) and (self.get_ip2 is None and self.get_port2 is None) and (
                self.get_ip3 is None and self.get_port3 is None):
            self.play_popup(0)
        elif song_name is None:
            self.song_empty_popup(1)
        else:
            if not self.thread.isRunning():
                self.pushButton7.setEnabled(False)
                global paused
                paused = False

                self.obj.intReady.connect(self.showTime)
                self.obj.moveToThread(self.thread)
                self.obj.finished.connect(self.thread.quit)
                self.thread.started.connect(self.obj.procCounter_1)
                self.thread.start()

                self.thread_1 = QThread()
                self.obj_2 = Client2_Send(ip=self.get_ip1, port=self.get_port1, ip2=self.get_ip2, port2=self.get_port2,
                                          ip3=self.get_ip3, port3=self.get_port3, source=song_name)
                self.obj_2.moveToThread(self.thread_1)
                self.obj_2.finished.connect(self.thread_1.quit)
                self.thread_1.started.connect(self.obj_2.running_all)
                #self.obj_2.finished_1.connect(lambda: self.pushButton7.setEnabled(True))
                self.thread_1.start()


    def play_popup(self, event):
        msg_text = "Can't start playing, unspecified IP and Port address!"
        QMessageBox.setStyleSheet(self, "QMessageBox, {background-color: rgb(226, 226, 226);}")
        create_popup = QMessageBox.warning(self, "Unable to Play", msg_text, QMessageBox.Ok)
        try:
            if create_popup == QMessageBox.Ok:
                event.accept()
        except:
            pass

    def song_empty_popup(self, event):
        msg_text = "Can't start streaming. \n" \
                   "Be sure to select a song before playing."
        QMessageBox.setStyleSheet(self, "QMessageBox, {background-color: rgb(226, 226, 226);}")
        create_popup = QMessageBox.warning(self, "Sound error", msg_text, QMessageBox.Ok)
        try:
            if create_popup == QMessageBox.Ok:
                event.accept()
        except:
            pass

    def read_setting(self):
        try:
            for i in self.songs_list:
                self.file_name = Path(i).stem
                self.song_list_loc.append(self.file_name)
                # print(self.song_list_loc)
                self.comboBox.insertItem(0, QIcon("12.png"), self.file_name)
            self.comboBox.setCurrentIndex(0)
        except TypeError as e:
            print(e)

    def open_file(self, name):
        self.settings = QSettings()
        if name == "Add more":
            dialog_title = "Choose a Sound File"
            sound_file = QtWidgets.QFileDialog.getOpenFileName(self, dialog_title, os.path.expandvars(""),
                                                               "Sound files (*.mp3 *.wav *.ogg)")
            self.directory_path = sound_file[0]

            print(self.directory_path)
            self.name_file = Path(self.directory_path).stem  # set the filename

            print(self.pick_list)
            if self.name_file != "" and not self.name_file in [self.comboBox.itemText(i) for i in
                                                               range(self.comboBox.count())]:
                self.comboBox.insertItem(0, QIcon("12.png"), self.name_file)
                self.comboBox.setCurrentText(self.name_file)
                self.location_song = self.directory_path

                if self.name_file not in self.pick_list:
                    self.pick_list[self.name_file] = self.directory_path
                    self.settings.setValue("songdict", self.pick_list)

                if not self.location_song in self.song_list_loc:
                    self.song_list_loc.append(self.location_song)
                    print(self.song_list_loc)
                    self.settings.setValue("songplay", self.directory_path)
                    self.settings.setValue("songlist", self.song_list_loc)
                else:
                    print("Already in list")
                    pass

            else:
                pass

        else:
            if name != '':

                if self.dict_song is not None:
                    self.pick_list = {**self.dict_song, **self.pick_list}
                if name in self.pick_list:
                    song_selected = self.pick_list[name]
                    self.settings.setValue("songplay", song_selected)
                    print(f"location: {song_selected}")
                    self.settings.setValue("songdict", self.pick_list)


    def closeEvent(self, event):
        global paused
        paused = True
        song_list = self.settings.value("songlist")
        song_play = self.settings.value("songplay")
        if song_list is not None and song_play is not None:
            close_message = "Do you want to save changes?"
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
                paused = True
            elif create_reply == QMessageBox.No:
                self.settings.remove("songplay")
                self.settings.remove("songlist")
                self.settings.remove("songdict")
                print("Remove changes!")
                event.accept()
                paused = True
            else:
                event.ignore()
        else:
            pass


# Earthquake Drill ---->
class EarthDrill1(QtWidgets.QDialog, Ui_earthquake_dialog):
    swt1 = pyqtSignal()
    swt2 = pyqtSignal()
    swt3 = pyqtSignal()

    def __init__(self, parent=None):
        super(EarthDrill1, self).__init__(parent)
        self.setupUi(self)
        self.toolButton_1.clicked.connect(self.switch1)
        self.toolButton_2.clicked.connect(self.switch2)
        self.toolButton_3.clicked.connect(self.switch3)
        text1 = self.comboBox.activated[str].connect(self.open_file)
        self.settings = QSettings()
        self.songs_list = self.settings.value("songlist01")
        self.song_list_loc = []
        self.new_list = []
        self.read_setting()

        self.pushButton7.clicked.connect(self.play_button)
        self.pushButton8.clicked.connect(self.stop_button)

        self.buttonBox.accepted.connect(self.stop_button)
        self.buttonBox.rejected.connect(self.stop_button)

    def switch1(self):
        self.swt1.emit()

    def switch2(self):
        self.swt2.emit()

    def switch3(self):
        self.swt3.emit()

    def stop_button(self):
        global paused
        paused = True
        time_edit = QTime(00, 00, 00)
        displayTxt = time_edit.toString('hh:mm:ss')

    def showTime(self, i):
        # currentTime = QTime.currentTime()
        time_edit = QTime(00, 00, 00)
        every_1 = time_edit.addSecs(i)
        displayTxt = every_1.toString('hh:mm:ss')
        if paused:
            displayTxt = time_edit.toString('hh:mm:ss')
        # self.label_5.setText(displayTxt)
        self.label_5.setText(
            f"<html><head/><body><p>Playing time:</p><p><span style=\" color:#0000ff;\">{displayTxt}</span></p></body></html>")
        self.label_5.adjustSize()


    def play_button(self):
        global paused
        paused = False
        self.obj = Worker()
        self.thread = QThread()
        self.obj.intReady.connect(self.showTime)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.procCounter)
        self.thread.start()

    def read_setting(self):
        try:
            for i in self.songs_list:
                self.file_name = Path(i).stem
                self.song_list_loc.append(self.file_name)
                # print(self.song_list_loc)
                self.comboBox.insertItem(0, QIcon("12.png"), self.file_name)
            self.comboBox.setCurrentIndex(0)
        except TypeError as e:
            print(e)

    def open_file(self, name):
        self.settings = QSettings()
        if name == "Add more":
            dialog_title = "Choose a Sound File"
            sound_file = QtWidgets.QFileDialog.getOpenFileName(self, dialog_title, os.path.expandvars(''),
                                                               "Sound files (*.mp3 *.wav *.ogg)")
            self.directory_path = sound_file[0]
            self.name_file = Path(self.directory_path).stem  # set the filename

            if self.name_file != "" and not self.name_file in [self.comboBox.itemText(i) for i in
                                                               range(self.comboBox.count())]:
                self.comboBox.insertItem(0, QIcon("12.png"), self.name_file)
                self.comboBox.setCurrentText(self.name_file)
                self.location_song = (self.directory_path)

                if not self.location_song in self.song_list_loc:
                    self.song_list_loc.append(self.location_song)
                    print(self.song_list_loc)
                    self.settings.setValue("songplay01", self.directory_path)
                    self.settings.setValue("songlist01", self.song_list_loc)
                else:
                    print("Already in list")
                    pass

            else:
                pass


        else:
            if name != '':
                song_selected = os.path.expanduser('~/' + name)
                self.settings.setValue("songplay01", song_selected)
            else:
                pass

    def closeEvent(self, event):
        global paused
        paused = True
        song_list = self.settings.value('songlist01')
        song_play = self.settings.value('songplay01')
        if song_list != None and song_play != None:
            close_message = "Do you want to save changes?"
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()

                paused = True
            elif create_reply == QMessageBox.No:
                self.settings.remove("songplay01")
                self.settings.remove("songlist01")
                print("Remove changes!")
                paused = True
                event.accept()
            else:
                event.ignore()

        else:
            pass


class config1_1(QtWidgets.QDialog, Ui_conf1_dialog):

    # setbtn1_1 = pyqtSignal()
    def __init__(self, parent=None):
        super(config1_1, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.input_ip = self.lineEdit_1
        self.input_ip.setValidator(ipValidator)

        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        # self.buttonBox.accepted.connect(self.ok_pressed1)
        self.buttonBox.rejected.connect(self.reject)
        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext", self.text1)
        self.settings.setValue("readip", self.ip_addr1)
        self.settings.setValue('readport', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext")
        readip1 = self.settings.value("readip")
        readport1 = self.settings.value('readport')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext")
        read_ip1 = self.settings.value("readip")
        read_port1 = self.settings.value("readport")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext")
                self.settings.remove("readip")
                self.settings.remove("readport")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config1_2(QtWidgets.QDialog, Ui_conf2_dialog):
    # setbtn1_2 = pyqtSignal()

    def __init__(self, parent=None):
        super(config1_2, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.textEdit.setReadOnly(True)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEdit_1.setValidator(ipValidator)

        self.input_ip = self.lineEdit_1
        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)
        # ------------------------------
        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)
        self.buttonBox.rejected.connect(self.reject)
        self.read_settings()

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext2")
        readip1 = self.settings.value("readip2")
        readport1 = self.settings.value('readport2')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext2", self.text1)
        self.settings.setValue("readip2", self.ip_addr1)
        self.settings.setValue('readport2', self.ip_port1)
        print(self.text1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext2")
        read_ip1 = self.settings.value("readip2")
        read_port1 = self.settings.value("readport2")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext2")
                self.settings.remove("readip2")
                self.settings.remove("readport2")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config1_3(QtWidgets.QDialog, Ui_conf3_dialog):
    # setbtn1_3 = pyqtSignal()
    def __init__(self, parent=None):
        super(config1_3, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.textEdit.setReadOnly(True)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression

        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEdit_1.setValidator(ipValidator)

        self.input_ip = self.lineEdit_1
        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext3", self.text1)
        self.settings.setValue("readip3", self.ip_addr1)
        self.settings.setValue('readport3', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext3")
        readip1 = self.settings.value("readip3")
        readport1 = self.settings.value('readport3')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext3")
        read_ip1 = self.settings.value("readip3")
        read_port1 = self.settings.value("readport3")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext3")
                self.settings.remove("readip3")
                self.settings.remove("readport3")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config2_1(QtWidgets.QDialog, Ui_conf1_dialog):
    # setbtn1_1 = pyqtSignal()
    def __init__(self, parent=None):
        super(config2_1, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.input_ip = self.lineEdit_1
        self.input_ip.setValidator(ipValidator)

        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext00", self.text1)
        self.settings.setValue("readip00", self.ip_addr1)
        self.settings.setValue('readport00', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext00")
        readip1 = self.settings.value("readip00")
        readport1 = self.settings.value('readport00')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext00")
        read_ip1 = self.settings.value("readip00")
        read_port1 = self.settings.value("readport00")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext00")
                self.settings.remove("readip00")
                self.settings.remove("readport00")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config2_2(QtWidgets.QDialog, Ui_conf2_dialog):
    # setbtn1_2 = pyqtSignal()

    def __init__(self, parent=None):
        super(config2_2, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.textEdit.setReadOnly(True)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEdit_1.setValidator(ipValidator)

        self.input_ip = self.lineEdit_1
        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)
        # ------------------------------
        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)
        self.buttonBox.rejected.connect(self.reject)
        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext01", self.text1)
        self.settings.setValue("readip01", self.ip_addr1)
        self.settings.setValue('readport01', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext01")
        readip1 = self.settings.value("readip01")
        readport1 = self.settings.value('readport01')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext01")
        read_ip1 = self.settings.value("readip01")
        read_port1 = self.settings.value("readport01")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext01")
                self.settings.remove("readip01")
                self.settings.remove("readport01")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config2_3(QtWidgets.QDialog, Ui_conf3_dialog):
    # setbtn1_3 = pyqtSignal()
    def __init__(self, parent=None):
        super(config2_3, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.textEdit.setReadOnly(True)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression

        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEdit_1.setValidator(ipValidator)

        self.input_ip = self.lineEdit_1
        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext02", self.text1)
        self.settings.setValue("readip02", self.ip_addr1)
        self.settings.setValue('readport02', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext02")
        readip1 = self.settings.value("readip02")
        readport1 = self.settings.value('readport02')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext02")
        read_ip1 = self.settings.value("readip02")
        read_port1 = self.settings.value("readport02")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext02")
                self.settings.remove("readip02")
                self.settings.remove("readport02")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config3_1(QtWidgets.QDialog, Ui_conf1_dialog):
    # setbtn1_1 = pyqtSignal()
    def __init__(self, parent=None):
        super(config3_1, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.input_ip = self.lineEdit_1
        self.input_ip.setValidator(ipValidator)

        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.read_settings)
        self.buttonBox.rejected.connect(self.reject)
        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext03", self.text1)
        self.settings.setValue("readip03", self.ip_addr1)
        self.settings.setValue('readport03', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext03")
        readip1 = self.settings.value("readip03")
        readport1 = self.settings.value('readport03')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext03")
        read_ip1 = self.settings.value("readip03")
        read_port1 = self.settings.value("readport03")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext03")
                self.settings.remove("readip03")
                self.settings.remove("readport03")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config3_2(QtWidgets.QDialog, Ui_conf2_dialog):
    # setbtn1_2 = pyqtSignal()

    def __init__(self, parent=None):
        super(config3_2, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.textEdit.setReadOnly(True)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEdit_1.setValidator(ipValidator)

        self.input_ip = self.lineEdit_1
        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)
        # ------------------------------
        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext04", self.text1)
        self.settings.setValue("readip04", self.ip_addr1)
        self.settings.setValue('readport04', self.ip_port1)
        print(self.text1)

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext04")
        readip1 = self.settings.value("readip04")
        readport1 = self.settings.value('readport04')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext04")
        read_ip1 = self.settings.value("readip04")
        read_port1 = self.settings.value("readport04")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext04")
                self.settings.remove("readip04")
                self.settings.remove("readport04")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")


class config3_3(QtWidgets.QDialog, Ui_conf3_dialog):
    # setbtn1_3 = pyqtSignal()
    def __init__(self, parent=None):
        super(config3_3, self).__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.textEdit.setReadOnly(True)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression

        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.lineEdit_1.setValidator(ipValidator)

        self.input_ip = self.lineEdit_1
        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.read_settings()

    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext = self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                      "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext05", self.text1)
        self.settings.setValue("readip05", self.ip_addr1)
        self.settings.setValue('readport05', self.ip_port1)
        print(self.text1)

    def closeEvent(self, event):
        read_text1 = self.settings.value("readtext05")
        read_ip1 = self.settings.value("readip05")
        read_port1 = self.settings.value("readport05")
        if read_text1 != None and read_ip1 != None and read_port1 != None:
            close_message = "Do you want to save changes you apply? "
            QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
            create_reply = QMessageBox.question(self, 'Warning', close_message,
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if create_reply == QMessageBox.Yes:
                event.accept()
            elif create_reply == QMessageBox.No:
                self.settings = QSettings()
                self.settings.remove("readtext05")
                self.settings.remove("readip05")
                self.settings.remove("readport05")
                print("Remove changes!")
                event.accept()
            else:
                event.ignore()

        else:
            print("No input!")

    def read_settings(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext05")
        readip1 = self.settings.value("readip05")
        readport1 = self.settings.value('readport05')
        if readtext1 == None:
            text_disp = "Add IP address and Port number to connect."
            self.textEdit.setPlainText(text_disp)
        else:
            self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readport1)


# --------------*_*_*_*_*_*------------

# Manage windows
class Controller:
    def __init__(self):
        pass

    def exit1(self):
        sys.exit()

    def show_main(self):
        self.window1 = MyMainWindow()
        self.window1.window1_1.connect(self.show_onstream)
        self.window1.window1_2.connect(self.show_afstream)
        self.window1.window1_3.connect(self.show_filetrans)
        self.window1.action_exit.connect(self.exit1)
        self.window1.show()

    def show_onstream(self):
        self.window2 = StreamWindow()
        self.window2.window2_1.connect(self.show_livea1)
        self.window2.window2_2.connect(self.show_firea1)
        self.window2.window2_3.connect(self.show_eartha1)
        self.window2.actionbtn1.connect(self.backmain1)
        self.window2.action_exit.connect(self.exit1)
        self.window2.show()
        self.window1.hide()

    def backmain1(self):
        self.show_main()
        self.window2.hide()

    def backmain2(self):
        self.show_main()
        self.window3.hide()

    def backmain3(self):
        self.show_main()
        self.window4.hide()

    def show_afstream(self):
        self.window3 = StreamWindow1()
        self.window3.actionbtn.connect(self.backmain2)
        self.window3.action_exit.connect(self.exit1)
        self.window3.show()
        self.window1.hide()

    def show_filetrans(self):
        self.window4 = FileTransferWindow()
        self.window4.actionbtn.connect(self.backmain3)
        self.window4.action_exit.connect(self.exit1)
        self.window4.show()
        self.window1.hide()

    def show_livea1(self):
        self.window2_1 = live_announce()
        self.window2_1.btn1.connect(self.show_config1_1)
        self.window2_1.btn2.connect(self.show_config1_2)
        self.window2_1.btn3.connect(self.show_config1_3)
        self.x1 = self.window2_1.show()

    def show_firea1(self):
        self.window2_2 = FireDrill1()
        self.window2_2.swt1.connect(self.show_config2_1)
        self.window2_2.swt2.connect(self.show_config2_2)
        self.window2_2.swt3.connect(self.show_config2_3)
        self.x2 = self.window2_2.show()

    def show_eartha1(self):
        self.window2_3 = EarthDrill1()
        self.window2_3.swt1.connect(self.show_config3_1)
        self.window2_3.swt2.connect(self.show_config3_2)
        self.window2_3.swt3.connect(self.show_config3_3)
        self.x3 = self.window2_3.show()

    def show_config1_1(self):
        self.dialog = config1_1()
        self.dialog.show()

    def show_config1_2(self):
        self.dialog = config1_2()
        self.dialog.show()

    def show_config1_3(self):
        self.dialog = config1_3()
        self.dialog.show()

    def show_config2_1(self):
        self.dialog = config2_1()
        self.dialog.show()

    def show_config2_2(self):
        self.dialog = config2_2()
        self.dialog.show()

    def show_config2_3(self):
        self.dialog = config2_3()
        self.dialog.show()

    def show_config3_1(self):
        self.dialog = config3_1()
        self.dialog.show()

    def show_config3_2(self):
        self.dialog = config3_2()
        self.dialog.show()

    def show_config3_3(self):
        self.dialog = config3_3()
        self.dialog.show()


# Initialize window
def mainrun():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys

    QtCore.QCoreApplication.setOrganizationName("Electorscit")
    QtCore.QCoreApplication.setOrganizationDomain("electorscit.com")
    QtCore.QCoreApplication.setApplicationName("MyApp")
    mainrun()
