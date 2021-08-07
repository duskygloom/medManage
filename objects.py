from PyQt5.QtWidgets import QFrame as qfra
from PyQt5.QtWidgets import QMainWindow as qwin
from PyQt5.QtWidgets import QPushButton as qbut
from PyQt5.QtWidgets import QLineEdit as qlin
from PyQt5.QtWidgets import QLabel as qlab
from PyQt5.QtCore import Qt as qt
from functions import log
from stylesheets import *

hand = qt.PointingHandCursor


class topbutton(qbut):

    def __init__(self, name: str, parent):
        super().__init__(parent)
        self.name = name
        self.setObjectName(name)
        self.setCursor(hand)
        self.setStyleSheet(topbuttonboth)
        log(f"{name} created")

    def isselected(self, status: bool):
        if status:
            self.setStyleSheet(topbuttonselectedboth)
            log(f"{self.name} selected")
        else:
            self.setStyleSheet(topbuttonboth)
            log(f"{self.name} unselected")


class topbar(qfra):

    def __init__(self, window: qwin):
        super().__init__(window)
        self.new = topbutton("newbutton", window)
        self.search = topbutton("searchbutton", window)
        self.stats = topbutton("statsbutton", window)
        self.chart = topbutton("chartbutton", window)
        self.note = topbutton("notebutton", window)
        self.configure()
        log("topbar created")

    def configure(self):
        self.setGeometry(17, 10, 1170, 60)
        self.setStyleSheet(topbarboth)
        # new button
        button = self.new
        button.setGeometry(160, 20, 140, 40)
        button.setText("New")
        # search button
        button = self.search
        button.setGeometry(320, 20, 140, 40)
        button.setText("Search")
        # stats button
        button = self.stats
        button.setGeometry(480, 20, 140, 40)
        button.setText("Stats")
        # chart button
        button = self.chart
        button.setGeometry(640, 20, 140, 40)
        button.setText("Chart")
        # note button
        button = self.note
        button.setGeometry(880, 20, 140, 40)
        button.setText("Note")
        #log
        log("topbar configured")


class addfield(qlin):

    def __init__(self, parent: qfra, placeholdertext: str, coords: tuple):
        super().__init__(parent)
        self.setPlaceholderText(placeholdertext)
        self.setStyleSheet(addfielddark)
        x = 150 + coords[0] * 490
        y = 150 + coords[1] * 50
        self.setGeometry(x, y, 340, 40)


class addbox(qfra):

    def __init__(self, window: qwin):
        '''adds new purchases and sells'''
        super().__init__(window)
        self.purchaselabel = qlab(self)
        self.selllabel = qlab(self)
        self.configure()
        self.purchasebatch = addfield(self, "batch number", (0, 0))
        self.sellbatch = addfield(self, "batch number", (1, 0))
        self.purchasename = addfield(self, "name", (0, 1))
        self.sellname = addfield(self, "name", (1, 1))
        self.purchaseamount = addfield(self, "quantity", (0, 2))
        self.sellamount = addfield(self, "quantity", (1, 2))
        self.purchaseprice = addfield(self, "price per piece", (0, 3))
        self.sellprice = addfield(self, "price per piece", (1, 3))
        self.dealer = addfield(self, "dealer", (0, 4))
        self.customer = addfield(self, "customer", (1, 4))
        self.purchasedate = addfield(self, "purchsed on", (0, 5))
        self.selldate = addfield(self, "sold on", (1, 5))
        self.mfgdate = addfield(self, "manufacture date", (0, 6))
        self.expdate = addfield(self, "expiry date", (0, 7))
        log("addbox created")

    def configure(self):
        '''configures addbox'''
        self.setGeometry(10, 80, 1180, 800)
        self.setStyleSheet(addboxboth)
        # purchase label
        label = self.purchaselabel
        label.setGeometry(150, 50, 300, 100)
        label.setText("Purchase")
        label.setStyleSheet(addlabelboth)
        # sell label
        label = self.selllabel
        label.setGeometry(640, 50, 300, 100)
        label.setText("Sell")
        label.setStyleSheet(addlabelboth)
        # log
        log("addbox configured")
