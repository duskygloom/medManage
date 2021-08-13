# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/duskygloom/Desktop/medManage/recreated/new.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(1200, 800)
        mainwindow.setStyleSheet("background-color: rgb(33, 33, 33);")
        self.topframe = QtWidgets.QFrame(mainwindow)
        self.topframe.setGeometry(QtCore.QRect(17, 10, 1170, 60))
        self.topframe.setStyleSheet("QFrame {\n"
"    border-radius: 30;\n"
"    background-color: transparent;\n"
"    border-style: solid;\n"
"    border-width: 3;\n"
"    border-color: rgb(255, 100, 125);\n"
"}")
        self.topframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.topframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topframe.setObjectName("topframe")
        self.frame = QtWidgets.QFrame(mainwindow)
        self.frame.setGeometry(QtCore.QRect(100, 120, 1000, 600))
        self.frame.setStyleSheet("QFrame {\n"
"    background-color: white;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(100, 150, 800, 100))
        self.label.setStyleSheet("font-size: 75pt;")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(150, 400, 200, 75))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 400, 200, 75))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("mainwindow", "medManage"))
        self.pushButton.setText(_translate("mainwindow", "new purchase"))
        self.pushButton_2.setText(_translate("mainwindow", "new sell"))
