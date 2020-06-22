import os
import socket
import threading
from pathlib import Path
from threading import Thread
import sys
import pyaudio

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia
from PyQt5.QtCore import pyqtSignal, QRegExp, QObject, QThread, QSettings
from PyQt5.QtGui import QRegExpValidator, QIntValidator, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, qApp

from GUI.main import Ui_MainWindow
from GUI.afterstream import Ui_afterStream
from GUI.configure1 import Ui_conf1_dialog
from GUI.configure2 import Ui_conf2_dialog
from GUI.configure3 import Ui_conf3_dialog
from GUI.earthdrill import Ui_earthquake_dialog
from GUI.filetransfer import Ui_fileTr
from GUI.firedrill import Ui_fire_dialog
from GUI.liveannou import Ui_live_dialog
from GUI.onstream import Ui_MainWindow1
from pydub import AudioSegment
from pydub.playback import play


def trap_exc_during_debug(*args):
    # when app raises uncaught exception, print info
    print(args)


# install exception hook: without this, uncaught exception would cause application to exit
sys.excepthook = trap_exc_during_debug


#MAINWINDOW
class MyMainWindow(QMainWindow,Ui_MainWindow):

    window1_1 = pyqtSignal()
    window1_2 = pyqtSignal()
    window1_3 = pyqtSignal()
    action_exit = pyqtSignal()

    def __init__(self,parent=None):
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


#ONSTREAM WINDOW
class StreamWindow(QtWidgets.QMainWindow,Ui_MainWindow1):
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

#AFTERSTREAM WINDOW
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


#FILE TRANSFER WINDOW
class FileTransferWindow(QtWidgets.QMainWindow, Ui_fileTr):
    actionbtn = QtCore.pyqtSignal()
    action_exit = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(FileTransferWindow,self).__init__(parent)
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


paused = False # global var.
#ONSTREAM SIDE --------->>>
#Live Announcement on onstream -->
class live_announce(QtWidgets.QDialog, Ui_live_dialog):
    btn1 = pyqtSignal()
    btn2= pyqtSignal()
    btn3= pyqtSignal()
    btn4= pyqtSignal()
#   btn5= pyqtSignal()
    frames = []

    def __init__(self, parent = None):
        super(live_announce, self).__init__(parent)
        self.settings = QtCore.QSettings
        self.setupUi(self)
        self.toolButton_1.clicked.connect(self.switch1)
        self.toolButton_2.clicked.connect(self.switch2)
        self.toolButton_3.clicked.connect(self.switch3)
        self.pushButton7.clicked.connect(self.playing_stream)
        self.pushButton8.clicked.connect(self.stop_live)
        self.comboBox_2.setCurrentIndex(1)
        self.comboBox_3.setCurrentIndex(2)
        #self.comboBox_1.connect()
        #self.comboBox_1.currentIndexChanged[int].connect(self.changetext1)
        #self.comboBox_2.currentIndexChanged[int].connect(#)
        #self.comboBox_3.currentIndexChanged[int].connect()
        #self.comboBox_2.model().item(2).setEnabled(False)


    def stop_live(self):
        global paused
        paused = True


    def switch1(self):
        self.btn1.emit()
    def switch2(self):
        self.btn2.emit()
    def switch3(self):
        self.btn3.emit()
    def switch4(self):
        self.btn4.emit()
#    def switch5(self):
#        self.btn5.emit()

    def playing_stream(self):
        global paused
        paused = False
        CHUNK = 1024
        FORMAT = pyaudio.paInt16  # Audio Codec
        CHANNELS = 2  # Stereo or Mono
        RATE = 44100  # Sampling Rate
        self.Audio = pyaudio.PyAudio()

        self.stream = self.Audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK,
                                      )
        self.AudioThread = Thread(target=self.record, args=(self.stream, CHUNK,))
        self.udpThread = Thread(target=self.streaming)
        self.AudioThread.setDaemon(True)
        self.udpThread.setDaemon(True)
        self.AudioThread.start()
        self.udpThread.start()
        print('Successfully send a live audio announcement: opena ang live_announcement_receiver')


    def streaming(self):
        self.settings = QtCore.QSettings()
        get_ip1 = self.settings.value("readip")
        get_port1 = self.settings.value("readport")
        get_ip2 = self.settings.value("readip2")
        get_port2 = self.settings.value("readport2")
        get_ip3 = self.settings.value("readip3")
        get_port3 = self.settings.value("readport3")
        print("1 SUCCESSFULLY ESTABLISHED CONNECTION TO: " + get_ip1)
        print("\n1 SUCCESSFULLY ESTABLISHED CONNECTION TO: " + get_ip2)
        print("\n1 SUCCESSFULLY ESTABLISHED CONNECTION TO: " + get_ip3)
        #get_port1 = int(get_port1)
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.z1 = udp
        print(paused)
        while True:
            if paused:
                break
            if len(self.frames) > 0:
                frames_send = self.frames.pop(0)
                self.z1.sendto(frames_send, (get_ip1, int(get_port1)))
                self.z1.sendto(frames_send, (get_ip2, int(get_port2)))
                self.z1.sendto(frames_send, (get_ip3, int(get_port3)))
        udp.close()

    def record(self, stream, CHUNK):
        while True:
            if paused:
                break
            read_data = stream.read(CHUNK)
            self.frames.append(read_data)

    def closeEvent(self, event):
        print("Closing...")
        self.settings = QSettings()
        self.settings.setValue("closeEvent_1", 2)
        self.settings.remove("readip")
        self.settings.remove("readport")
        self.settings.remove("readip2")
        self.settings.remove("readport2")
        self.settings.remove("readip3")
        self.settings.remove("readport3")
        self.settings.remove("readtext")
        self.settings.remove("readtext2")
        self.settings.remove("readtext3")
        keys = self.settings.allKeys()
        print(keys)



#FireDrill ---->
class FireDrill1(QtWidgets.QDialog, Ui_fire_dialog):
    swt1 = pyqtSignal()
    swt2 = pyqtSignal()
    swt3 = pyqtSignal()

    def __init__(self, parent = None):
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
        self.read_setting()
        #self.show()


    def switch1(self):
        self.swt1.emit()
    def switch2(self):
        self.swt2.emit()
    def switch3(self):
        self.swt3.emit()

    def read_setting(self):
        for i in self.songs_list:
            self.file_name = Path(i).stem
            self.song_list_loc.append(self.file_name)
            #print(self.song_list_loc)
            self.comboBox.insertItem(0, QIcon("12.png"), self.file_name)

    def open_file(self,name):
        self.settings = QSettings()
        if name == "Add more":
            dialog_title = "Choose a Sound File"
            sound_file = QtWidgets.QFileDialog.getOpenFileName(self, dialog_title, os.path.expanduser('~'),
                                                               "Sound files (*.mp3 *.wav *.ogg)")
            self.directory_path = sound_file[0]
            self.name_file = Path(self.directory_path).stem #set the filename

            if self.name_file !=  "" and  not self.name_file in [self.comboBox.itemText(i) for i in range(self.comboBox.count())] :
                self.comboBox.insertItem(0, QIcon("12.png"), self.name_file)
                self.comboBox.setCurrentText(self.name_file)
                self.location_song = (self.directory_path)

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
                song_selected = os.path.expanduser('~/'+name)
                self.settings.setValue("songplay", song_selected)
            else:
                pass




    def closeEvent(self, event):
        close_message = "Save changes on config and drop-down sound list?"
        QMessageBox.setStyleSheet(self, "QMessageBox {background-color: rgb(226, 226, 226);}")
        create_reply = QMessageBox.question(self, 'Warning', close_message, QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if create_reply == QMessageBox.Yes:
            event.accept()
        elif create_reply == QMessageBox.No:
            self.settings.remove("songplay")
            self.settings.remove("songlist")
            print("Remove changes!")
            event.accept
        else:
            event.ignore()




#Earthquake Drill ---->
class EarthDrill1(QtWidgets.QDialog, Ui_earthquake_dialog):
    swt1 = pyqtSignal()
    swt2 = pyqtSignal()
    swt3 = pyqtSignal()
    def __init__(self, parent = None):
        super(EarthDrill1, self).__init__(parent)
        self.setupUi(self)
        self.toolButton_1.clicked.connect(self.switch1)
        self.toolButton_2.clicked.connect(self.switch2)
        self.toolButton_3.clicked.connect(self.switch3)

    def switch1(self):
        self.swt1.emit()
    def switch2(self):
        self.swt2.emit()
    def switch3(self):
        self.swt3.emit()


class config1_1(QtWidgets.QDialog, Ui_conf1_dialog):

    #setbtn1_1 = pyqtSignal()
    def __init__(self, parent =None):
        super(config1_1, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.input_ip= self.lineEdit_1
        self.input_ip.setValidator(ipValidator)

        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.ok_pressed1)
        self.buttonBox.rejected.connect(self.reject)



    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext =self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                 "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext", self.text1 )
        self.settings.setValue("readip",self.ip_addr1)
        self.settings.setValue('readport',self.ip_port1)
        print(self.text1)

        #=====>Save ip to *.txt
        ipsavetxt = (self.ip_addr1 +'\n'+ self.ip_port1)
        with open("saveip.txt", 'w') as f:
            f.write(ipsavetxt)



    def ok_pressed1(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext")
        readip1 = self.settings.value("readip")
        readip2 = self.settings.value('readport')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)


    def closeEvent(self, event):
        self.settings= QSettings()
        self.settings.remove("readtext")
        self.settings.remove("readip")
        self.settings.remove("readport")




class config1_2(QtWidgets.QDialog, Ui_conf2_dialog):
    #setbtn1_2 = pyqtSignal()

    def __init__(self, parent =None):
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
        #------------------------------
        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext2")
        if readtext1 == None:
            readtext1="Connect to \nIP address:\nPort:"
        readip1 = self.settings.value("readip2")
        readip2 = self.settings.value('readport2')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)
        self.buttonBox.rejected.connect(self.reject)

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

        # =====>
        ipsavetxt = (self.ip_addr1 + '\n' + self.ip_port1)
        with open("saveip2.txt", 'w') as f:
            f.write(ipsavetxt)

    def closeEvent(self, event):
        self.settings = QSettings()
        readtext1 = self.settings.value("readtext2")
        readip1 = self.settings.value("readip2")
        readip2 = self.settings.value('readport2')
        self.settings.remove("readtext2")
        self.settings.remove("readip2")
        self.settings.remove("readport2")
        print('closing conf2')



class config1_3(QtWidgets.QDialog, Ui_conf3_dialog):
    #setbtn1_3 = pyqtSignal()
    def __init__(self, parent =None):
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


        self.buttonBox.accepted.connect(self.ok_button)
        self.buttonBox.rejected.connect(self.reject)

        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext3")
        print(readtext1)
        if readtext1 == None:
            readtext1 = "Connect to \nIP address:\nPort:"
        readip1 = self.settings.value("readip3")
        readip2 = self.settings.value('readport3')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)


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
        # =====>
        ipsavetxt = (self.ip_addr1 + '\n' + self.ip_port1)
        with open("saveip3.txt", 'w') as f:
            f.write(ipsavetxt)

    def closeEvent(self, event):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext3")
        readip1 = self.settings.value("readip3")
        readip2 = self.settings.value('readport3')
        self.settings.remove("readtext3")
        self.settings.remove("readip3")
        self.settings.remove("readport3")
        super(config1_3).__init__()


    def ok_button(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext3")
        readip1 = self.settings.value("readip3")
        readip2 = self.settings.value('readport3')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)
        print("ok button was pressed")


class config2_1(QtWidgets.QDialog, Ui_conf1_dialog):
    #setbtn1_1 = pyqtSignal()
    def __init__(self, parent =None):
        super(config2_1, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.input_ip= self.lineEdit_1
        self.input_ip.setValidator(ipValidator)

        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.ok_pressed1)
        self.buttonBox.rejected.connect(self.reject)



    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext =self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                 "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext00", self.text1 )
        self.settings.setValue("readip00",self.ip_addr1)
        self.settings.setValue('readport00',self.ip_port1)
        print(self.text1)



    def ok_pressed1(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext00")
        readip1 = self.settings.value("readip00")
        readip2 = self.settings.value('readport00')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)


    def closeEvent(self, event):
        self.settings= QSettings()
        self.settings.remove("readtext00")
        self.settings.remove("readip00")
        self.settings.remove("readport00")


class config2_2(QtWidgets.QDialog, Ui_conf2_dialog):
    #setbtn1_2 = pyqtSignal()

    def __init__(self, parent =None):
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
        #------------------------------
        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext01")
        if readtext1 == None:
            readtext1="Connect to \nIP address:\nPort:"
        readip1 = self.settings.value("readip01")
        readip2 = self.settings.value('readport01')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)
        self.buttonBox.rejected.connect(self.reject)

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


    def closeEvent(self, event):
        self.settings = QSettings()
        readtext1 = self.settings.value("readtext01")
        readip1 = self.settings.value("readip01")
        readip2 = self.settings.value('readport01')
        self.settings.remove("readtext01")
        self.settings.remove("readip01")
        self.settings.remove("readport01")



class config2_3(QtWidgets.QDialog, Ui_conf3_dialog):
    #setbtn1_3 = pyqtSignal()
    def __init__(self, parent =None):
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


        self.buttonBox.accepted.connect(self.ok_button)
        self.buttonBox.rejected.connect(self.reject)

        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext02")
        print(readtext1)
        if readtext1 == None:
            readtext1 = "Connect to \nIP address:\nPort:"
        readip1 = self.settings.value("readip02")
        readip2 = self.settings.value('readport02')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)


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


    def closeEvent(self, event):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext02")
        readip1 = self.settings.value("readip02")
        readip2 = self.settings.value('readport02')
        self.settings.remove("readtext02")
        self.settings.remove("readip02")
        self.settings.remove("readport02")
        super(config2_3).__init__()


    def ok_button(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext02")
        readip1 = self.settings.value("readip02")
        readip2 = self.settings.value('readport02')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)
        print("ok button was pressed")



class config3_1(QtWidgets.QDialog, Ui_conf1_dialog):
    #setbtn1_1 = pyqtSignal()
    def __init__(self, parent =None):
        super(config3_1, self).__init__(parent)
        self.setupUi(self)

        self.setWindowModality(QtCore.Qt.ApplicationModal)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)
        self.input_ip= self.lineEdit_1
        self.input_ip.setValidator(ipValidator)

        self.input_port = self.lineEdit_2
        self.input_port.setValidator((QIntValidator()))
        self.input_port.setMaxLength(5)

        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.buttonBox.accepted.connect(self.ok_pressed1)
        self.buttonBox.rejected.connect(self.reject)



    def setbutton_click(self):
        self.settings = QtCore.QSettings()
        self.ip_addr1 = self.input_ip.text()
        self.ip_port1 = self.input_port.text()
        self.showtext =self.textEdit
        self.text1 = ("Connect to \nIP address: " + self.ip_addr1 +
                 "\nPort: \n" + self.ip_port1)
        showtext1 = self.showtext.setPlainText(self.text1)
        self.settings.setValue("readtext03", self.text1 )
        self.settings.setValue("readip03",self.ip_addr1)
        self.settings.setValue('readport03',self.ip_port1)
        print(self.text1)



    def ok_pressed1(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext03")
        readip1 = self.settings.value("readip03")
        readip2 = self.settings.value('readport03')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)


    def closeEvent(self, event):
        self.settings= QSettings()
        self.settings.remove("readtext03")
        self.settings.remove("readip03")
        self.settings.remove("readport03")


class config3_2(QtWidgets.QDialog, Ui_conf2_dialog):
    #setbtn1_2 = pyqtSignal()

    def __init__(self, parent =None):
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
        #------------------------------
        setbutton1 = self.pushButton_1
        setbutton1.clicked.connect(self.setbutton_click)

        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext04")
        if readtext1 == None:
            readtext1="Connect to \nIP address:\nPort:"
        readip1 = self.settings.value("readip04")
        readip2 = self.settings.value('readport04')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)
        self.buttonBox.rejected.connect(self.reject)

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


    def closeEvent(self, event):
        self.settings = QSettings()
        readtext1 = self.settings.value("readtext04")
        readip1 = self.settings.value("readip04")
        readip2 = self.settings.value('readport04')
        self.settings.remove("readtext04")
        self.settings.remove("readip04")
        self.settings.remove("readport04")




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

        self.buttonBox.accepted.connect(self.ok_button)
        self.buttonBox.rejected.connect(self.reject)

        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext05")
        print(readtext1)
        if readtext1 == None:
            readtext1 = "Connect to \nIP address:\nPort:"
        readip1 = self.settings.value("readip05")
        readip2 = self.settings.value('readport05')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)

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
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext05")
        readip1 = self.settings.value("readip05")
        readip2 = self.settings.value('readport05')
        self.settings.remove("readtext05")
        self.settings.remove("readip05")
        self.settings.remove("readport05")
        super(config3_3).__init__()

    def ok_button(self):
        self.settings = QtCore.QSettings()
        readtext1 = self.settings.value("readtext05")
        readip1 = self.settings.value("readip05")
        readip2 = self.settings.value('readport05')
        self.textEdit.setPlainText(readtext1)
        self.lineEdit_1.setText(readip1)
        self.lineEdit_2.setText(readip2)
        print("ok button was pressed")


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


#--------------*_*_*_*_*_*------------

#Manage windows
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


if __name__ =="__main__":

    import sys
    QtCore.QCoreApplication.setOrganizationName("Electorscit")
    QtCore.QCoreApplication.setOrganizationDomain("electorscit.com")
    QtCore.QCoreApplication.setApplicationName("MyApp")
    mainrun()
