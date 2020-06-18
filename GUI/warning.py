# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'warning.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_warn(object):
    def setupUi(self, warn):
        warn.setObjectName("warn")
        warn.resize(337, 306)
        warn.setStyleSheet("background-color: rgb(170, 0, 0);")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(warn)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(warn)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("color: rgb(255, 215, 0);")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout_2.addWidget(self.frame)
        self.label_2 = QtWidgets.QLabel(warn)
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/newPrefix/guide.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(warn)
        self.buttonBox.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(warn)
        self.buttonBox.accepted.connect(warn.accept)
        self.buttonBox.rejected.connect(warn.reject)
        QtCore.QMetaObject.connectSlotsByName(warn)

    def retranslateUi(self, warn):
        _translate = QtCore.QCoreApplication.translate
        warn.setWindowTitle(_translate("warn", "Warning"))
        self.label.setText(_translate("warn", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\"> IP Address &amp; Port are Not Set!</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Configure first the following</span></p><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">before proceeding...</span></p></body></html>"))
import new_rc


