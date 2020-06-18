# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(730, 639)
        MainWindow.setMinimumSize(QtCore.QSize(730, 639))
        MainWindow.setMouseTracking(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/icons/ecelogo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_1 = QtWidgets.QLabel(self.widget)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.pushButton_1 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_1.setStyleSheet("background-color: rgb(226, 226, 226);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/newPrefix/sample/New folder/2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_1.setIcon(icon1)
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_2.setStyleSheet("background-color: rgb(226, 226, 226);")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/newPrefix/sample/New folder/2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.splitter)
        self.pushButton_3.setStyleSheet("background-color: rgb(226, 226, 226);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/newPrefix/icons/icons8-document-50-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon3)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.splitter, 4, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 3, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 730, 21))
        self.menubar.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/newPrefix/icons/icons8-cancel-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon4)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/newPrefix/icons/icons8-info-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon5)
        self.actionAbout.setObjectName("actionAbout")
        self.menuMenu.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Audio Sender"))
        self.label_1.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:28pt; font-weight:600; color:#ffd700;\">Audio Sender</span></p></body></html>"))
        self.pushButton_1.setText(_translate("MainWindow", "on Stream"))
        self.pushButton_2.setText(_translate("MainWindow", "after Stream"))
        self.pushButton_3.setText(_translate("MainWindow", "File Transfer"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
import resources.icons_rc
import resources.new_rc

'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
'''