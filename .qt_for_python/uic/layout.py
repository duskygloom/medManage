# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/duskygloom/Desktop/medManage/layout.ui'
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
        self.topframe.setGeometry(QtCore.QRect(17, 15, 1170, 60))
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
        self.frame.setGeometry(QtCore.QRect(200, 200, 800, 450))
        self.frame.setStyleSheet("QFrame {\n"
"    background-color: white;\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(100, 50, 600, 100))
        self.label.setStyleSheet("font-size: 75pt;")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(100, 300, 200, 75))
        self.pushButton.setStyleSheet("background-color: yellow;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 300, 200, 75))
        self.pushButton_2.setStyleSheet("background-color: yellow;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(100, 190, 200, 75))
        self.pushButton_3.setStyleSheet("background-color: yellow;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(500, 190, 200, 75))
        self.pushButton_4.setStyleSheet("background-color: yellow;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.frame_2 = QtWidgets.QFrame(mainwindow)
        self.frame_2.setGeometry(QtCore.QRect(50, 130, 1100, 570))
        self.frame_2.setStyleSheet("background-color: pink;")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(200, 20, 700, 50))
        self.label_3.setStyleSheet("font-size: 40pt;")
        self.label_3.setObjectName("label_3")
        self.frame_11 = QtWidgets.QFrame(mainwindow)
        self.frame_11.setGeometry(QtCore.QRect(0, 755, 1200, 40))
        self.frame_11.setStyleSheet("background-color: transparent;")
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.label_11 = QtWidgets.QLabel(self.frame_11)
        self.label_11.setGeometry(QtCore.QRect(0, 10, 1155, 30))
        self.label_11.setStyleSheet("background-color: rgb(240, 223, 175);\n"
"padding-left: 10;\n"
"padding-right: 10;")
        self.label_11.setObjectName("label_11")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_11)
        self.pushButton_6.setGeometry(QtCore.QRect(1155, 0, 40, 40))
        self.pushButton_6.setStyleSheet("border-radius: 20;\n"
"background-color: rgb(255, 0, 0);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.frame_2.raise_()
        self.topframe.raise_()
        self.frame.raise_()
        self.frame_11.raise_()

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("mainwindow", "Search"))
        self.pushButton.setText(_translate("mainwindow", "dealer"))
        self.pushButton_2.setText(_translate("mainwindow", "customer"))
        self.pushButton_3.setText(_translate("mainwindow", "batch number"))
        self.pushButton_4.setText(_translate("mainwindow", "name"))
        self.label_3.setText(_translate("mainwindow", "Search"))
        self.label_11.setText(_translate("mainwindow", "notificationlabel"))
        self.pushButton_6.setText(_translate("mainwindow", "x"))
