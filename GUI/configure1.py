# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configure1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator



class Ui_conf1_dialog(object):

    def setupUi(self, conf1_dialog):
        conf1_dialog.setObjectName("conf1_dialog")
        conf1_dialog.resize(393, 198)
        conf1_dialog.setMinimumSize(QtCore.QSize(393, 198))
        conf1_dialog.setMaximumSize(QtCore.QSize(393, 198))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/icons/ecelogo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        conf1_dialog.setWindowIcon(icon)
        conf1_dialog.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.buttonBox = QtWidgets.QDialogButtonBox(conf1_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(190, 150, 181, 41))
        self.buttonBox.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(conf1_dialog)
        self.widget.setGeometry(QtCore.QRect(30, 30, 341, 121))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 47, 13))
        self.label_3.setObjectName("label_3")
        self.lineEdit_1 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_1.setGeometry(QtCore.QRect(20, 30, 131, 20))
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 80, 131, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setValidator(QIntValidator())
        self.lineEdit_2.setMaxLength(5)
        self.pushButton_1 = QtWidgets.QPushButton(self.widget)
        self.pushButton_1.setGeometry(QtCore.QRect(160, 30, 51, 71))
        self.pushButton_1.setStyleSheet("background-color: rgb(226, 226, 226);\n"
"color: rgb(0, 0, 255);")
        self.pushButton_1.setObjectName("pushButton_1")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(230, 10, 104, 91))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setAcceptRichText(False)
        self.textEdit.setReadOnly(True)
        self.label = QtWidgets.QLabel(conf1_dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 181, 16))
        self.label.setStyleSheet("")
        self.label.setObjectName("label")
        self.retranslateUi(conf1_dialog)
        self.buttonBox.accepted.connect(conf1_dialog.accept)
        self.buttonBox.rejected.connect(conf1_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(conf1_dialog)

    def retranslateUi(self, conf1_dialog):
        _translate = QtCore.QCoreApplication.translate
        conf1_dialog.setWindowTitle(_translate("conf1_dialog", "Configure stream 1"))
        self.label_2.setText(_translate("conf1_dialog", "IP address:"))
        self.label_3.setText(_translate("conf1_dialog", "Port:"))
        self.lineEdit_1.setPlaceholderText(_translate("conf1_dialog", "192.168.0.1"))
        self.lineEdit_2.setPlaceholderText(_translate("conf1_dialog", "8080"))
        self.pushButton_1.setText(_translate("conf1_dialog", "Set"))
        self.textEdit.setHtml(_translate("conf1_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Connect to</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">IP address:  </p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Port: </p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("conf1_dialog", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffd700;\">Configure Stream 1:</span></p></body></html>"))
import resources.icons_rc


