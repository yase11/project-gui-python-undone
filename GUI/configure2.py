# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configure2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_conf2_dialog(object):
    def setupUi(self, conf2_dialog):
        conf2_dialog.setObjectName("conf2_dialog")
        conf2_dialog.resize(400, 196)
        conf2_dialog.setMinimumSize(QtCore.QSize(400, 196))
        conf2_dialog.setMaximumSize(QtCore.QSize(400, 196))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/newPrefix/icons/ecelogo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        conf2_dialog.setWindowIcon(icon)
        conf2_dialog.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.buttonBox = QtWidgets.QDialogButtonBox(conf2_dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 160, 341, 32))
        self.buttonBox.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(conf2_dialog)
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
        self.pushButton_1 = QtWidgets.QPushButton(self.widget)
        self.pushButton_1.setGeometry(QtCore.QRect(160, 30, 51, 71))
        self.pushButton_1.setStyleSheet("background-color: rgb(226, 226, 226);\n"
"color: rgb(0, 0, 255);")
        self.pushButton_1.setObjectName("pushButton_1")
        self.textEdit = QtWidgets.QTextEdit(self.widget)
        self.textEdit.setGeometry(QtCore.QRect(220, 10, 104, 91))
        self.textEdit.setObjectName("textEdit")
        self.label_1 = QtWidgets.QLabel(conf2_dialog)
        self.label_1.setGeometry(QtCore.QRect(20, 10, 181, 16))
        self.label_1.setStyleSheet("")
        self.label_1.setObjectName("label_1")

        self.retranslateUi(conf2_dialog)
        self.buttonBox.accepted.connect(conf2_dialog.accept)
        self.buttonBox.rejected.connect(conf2_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(conf2_dialog)

    def retranslateUi(self, conf2_dialog):
        _translate = QtCore.QCoreApplication.translate
        conf2_dialog.setWindowTitle(_translate("conf2_dialog", "Configure stream 2"))
        self.label_2.setText(_translate("conf2_dialog", "IP address:"))
        self.label_3.setText(_translate("conf2_dialog", "Port:"))
        self.lineEdit_1.setPlaceholderText(_translate("conf2_dialog", "192.168.0.1"))
        self.lineEdit_2.setPlaceholderText(_translate("conf2_dialog", "8080"))
        self.pushButton_1.setText(_translate("conf2_dialog", "Set"))
        self.textEdit.setHtml(_translate("conf2_dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Connected to</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Ip address:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Port:</p></body></html>"))
        self.label_1.setText(_translate("conf2_dialog", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#ffd700;\">Configure Stream 2:</span></p></body></html>"))
import resources.icons_rc

