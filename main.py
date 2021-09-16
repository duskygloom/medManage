### imports

import sys
import time
import os
from PyQt5.QtWidgets import QPlainTextEdit as qtxt
from PyQt5.QtWidgets import QApplication as qapp
from PyQt5.QtWidgets import QMainWindow as qwin
from PyQt5.QtWidgets import QPushButton as qbut
from PyQt5.QtWidgets import QShortcut as qsho
from PyQt5.QtWidgets import QLineEdit as qlin
from PyQt5.QtWidgets import QWidget as qwig
from PyQt5.QtWidgets import QFrame as qfra
from PyQt5.QtWidgets import QLabel as qlab
from PyQt5.QtGui import QIcon as qico
from PyQt5.QtGui import QFont as qfon
from PyQt5.QtGui import QTextCursor as qcur
from PyQt5.QtGui import QFontDatabase as qfdb
from PyQt5.QtGui import QKeyEvent as qkev
from PyQt5.QtGui import QKeySequence as qkey
from PyQt5.QtCore import Qt as qt
from PyQt5.QtCore import QSize as qsiz
import mysql.connector as sql
from datetime import date
import configuration as conf

handcursor = qt.PointingHandCursor
centeralign = qt.AlignCenter
if "dark" in conf.qsheet:
    theme = "dark"
else:
    theme = "light"

### functions

def log(message: str, category: str = "log"):
    '''logs message to terminal'''
    if conf.concise:
        ## printing on console
        text = f">>> {time.asctime()}\n{category}: {message}"
        print(text)
        ## writing on file
        if not logfile.closed:
            logfile.write(f"{text}\n")

def applyqsheet(sheet: str = conf.qsheet):
    '''selects qsheet for application'''
    with open(sheet, "r") as qs:
        app.setStyleSheet(qs.read())
    log(f"{sheet} applied")

def closefunction(status: int = 0):
    '''closes application'''
    log("closing application")
    if conf.concise:
        logfile.close()
    app.exit(status)

def refreshtopframe(tabname: str):
    '''clicks and unclicks topbuttons'''
    for i in ui.alltopbuttons:
        if i.text == tabname:
            i.setChecked(True)
        else:
            i.setChecked(False)
    log("topframe refreshed")

def refreshwindow(*required):
    '''shows and hides widgets'''
    for i in ui.allwidgets:
        if i in required:
            i.setVisible(True)
        else:
            i.setVisible(False)
    log("window refreshed")

def notify(message: str):
    '''notifies user in notificationwidget'''
    label = ui.notificationwidget.label
    label.setText(message)
    log(f"notified user '{message}'")

def iconconvert(iconname: str):
    '''converts blackicons to whiteicons'''
    black = f"resources/blackicons/{iconname}.svg"
    white = f"resources/whiteicons/{iconname}.svg"
    with open(black, "r") as rfile:
        content = rfile.read()
    with open(white, "w") as wfile:
        wfile.write(content.replace("#212121", "#e9e9e9"))

def iconize(iconname: str) -> str:
    '''changes colour of icon'''
    if theme == "dark":
        filename = f"resources/blackicons/{iconname}.svg"
    elif theme == "light":
        if "whiteicons" not in os.listdir("resources"):
            os.mkdir("resources/whiteicons")
        if f"{iconname}.svg" not in os.listdir("resources/whiteicons"):
            iconconvert(iconname)
        filename = f"resources/whiteicons/{iconname}.svg"
    return filename

def switchtab():
    '''switches tabs'''
    tabs = ui.alltopbuttons
    for i in range(len(tabs)):
        if tabs[i].isChecked():
            index = i + 1
            break
    if index >= len(tabs):
        index = 0
    tabs[index].animateClick()

### classes

class interface(qwig):

    def __init__(self):
        '''creates interface class'''
        super().__init__(mainwindow)
        self.configurewindow()
        self.configure()
        self.topframe = topframe(self)
        self.configuretopbuttons()
        self.alltopbuttons = [
            self.topframe.new,
            self.topframe.search,
            self.topframe.stats,
            self.topframe.chart,
            self.topframe.note,
            self.topframe.settings
        ]
        self.newstage = newstage(self)
        self.purchasewidget = purchasewidget(self)
        self.sellwidget = sellwidget(self)
        self.notificationwidget = notificationwidget(self)
        self.searchstage = searchstage(self)
        self.searchbatch = searchbatch(self)
        self.searchname = searchname(self)
        self.searchdealer = searchdealer(self)
        self.searchcustomer = searchcustomer(self)
        self.settingstage = settingstage(self)
        self.notestage = notestage(self)
        self.chartstage = chartstage(self)
        self.statstage = statstage(self)
        self.allwidgets = [ self.newstage, self.purchasewidget, self.sellwidget, self.searchstage, self.searchbatch, self.searchname, self.searchdealer, self.searchcustomer, self.settingstage, self.notestage, self.chartstage, self.statstage ]

    def configure(self):
        '''configures main widget'''
        self.setGeometry(0, 0, 1200, 800)
        self.setObjectName("stagewidget")
        log("configured topframe")

    def configurewindow(self):
        '''configures mainwindow'''
        window = mainwindow
        window.setObjectName("mainwindow")
        window.setWindowTitle("medManage")
        window.setWindowIcon(qico("resources/icon.svg"))
        window.setFixedSize(1200, 800)
        log("mainwindow configured")

    def configuretopbuttons(self):
        '''configures topbuttons'''
        frame = self.topframe
        frame.new.clicked.connect(self.setupnew)
        frame.search.clicked.connect(self.setupsearch)
        frame.stats.clicked.connect(self.setupstats)
        frame.chart.clicked.connect(self.setupchart)
        frame.note.clicked.connect(self.setupnote)
        frame.settings.clicked.connect(self.setupsettings)
        log("topbuttons configured")

    def setupnew(self):
        '''sets up New tab'''
        refreshtopframe("New")
        refreshwindow(self.newstage)
        log("New tab setup")

    def setupsearch(self):
        '''sets up Search tab'''
        refreshtopframe("Search")
        refreshwindow(self.searchstage)
        log("Search tab set up")

    def setupstats(self):
        '''sets up Stats tab'''
        refreshtopframe("Stats")
        refreshwindow(self.statstage)
        log("Stats tab set up")

    def setupchart(self):
        '''sets up Charts tab'''
        refreshtopframe("Chart")
        refreshwindow(self.chartstage)
        log("Chart tab set up")

    def setupnote(self):
        '''sets up Note tab'''
        refreshtopframe("Note")
        refreshwindow(self.notestage)
        self.notestage.textbox.setFocus()
        log("Note tab set up")
    
    def setupsettings(self):
        '''sets up Settings tab'''
        refreshtopframe("Settings")
        refreshwindow(self.settingstage)
        log("Settings tab set up")

### custom widgets

class topbutton(qbut):

    def __init__(self, text: str, position: int, parent: qfra):
        super().__init__(parent)
        self.text = text
        self.position = position
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures topbutton'''
        self.setObjectName("topbutton")
        self.setText(self.text)
        self.setCursor(handcursor)
        x = 33 + 160 * self.position
        self.setGeometry(x, 10, 140, 40)
        self.setCheckable(True)
        log(f"{self} configured")

class topframe(qfra):

    def __init__(self, stage: qfra):
        '''creates topframe'''
        super().__init__(stage)
        self.new = topbutton("New", 0, self)
        self.search = topbutton("Search", 1, self)
        self.stats = topbutton("Stats", 2, self)
        self.chart = topbutton("Chart", 3, self)
        self.note = topbutton("Note", 5, self)
        self.settings = topbutton("Settings", 6, self)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures topframe'''
        self.setObjectName("topframe")
        self.setGeometry(17, 10, 1170, 60)
        log("topframe configured")

class tabstage(qwig):

    def __init__(self, stage: qwig):
        '''creates tabstage'''
        super().__init__(stage)
        self.label = qlab(self)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures tabstage'''
        # self
        self.setGeometry(50, 120, 1100, 600)
        self.setObjectName("transparentwidget")
        # label
        self.label.setGeometry(250, 50, 600, 100)
        self.label.setObjectName("tabstagelabel")
        self.label.setAlignment(centeralign)
        # log
        log(f"{self} configured")

# new

class newbutton(qbut):

    def __init__(self, text: str, position: tuple, parent: qwig):
        '''creates newbutton'''
        super().__init__(parent)
        self.position = position
        self.text = text
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures newbutton'''
        x = 250 + 400 * self.position[0]
        y = 250 + 110 * self.position[1]
        self.setObjectName("duskybutton")
        self.setText(self.text)
        self.setGeometry(x, y, 200, 75)
        self.setStyleSheet("border-radius: 37; font-size: 25pt;")
        log(f"{self} configured")

class newstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates newstage'''
        super().__init__(stage)
        self.purchasebutton = newbutton("Purchase", (0, 1), self)
        self.sellbutton = newbutton("Sell", (1, 1), self)
        self.configurenew()
        log(f"{self} created")

    def configurenew(self):
        '''configures newstage'''
        # label
        self.label.setText("medManage")
        # buttons
        button = self.purchasebutton
        button.clicked.connect(self.purchasebuttonfunction)
        button = self.sellbutton
        button.clicked.connect(self.sellbuttonfunction)
        # log
        log(f"{self} configured")

    def purchasebuttonfunction(self):
        '''function of purchase button'''
        ui.purchasewidget.setVisible(True)
        self.setVisible(False)
        log("purchasewidget opened")

    def sellbuttonfunction(self):
        '''function of sell button'''
        ui.sellwidget.setVisible(True)
        self.setVisible(False)
        log("sellwidget opened")

class addfield(qwig):

    def __init__(self, name: str, position: int, stage: qwig):
        '''creates addfield'''
        super().__init__(stage)
        self.name = name
        self.position = position
        self.linedit = qlin(self)
        self.label = qlab(self)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''''configures addfield'''
        # self
        self.setObjectName("transparentwidget")
        y = 90 + 50 * self.position
        self.setGeometry(20, y, 1050, 50)
        # linedit
        line = self.linedit
        line.setObjectName("addfieldline")
        line.setGeometry(5, 5, 400, 40)
        # label
        label = self.label
        label.setObjectName("transparentlabel")
        label.setGeometry(420, 5, 620, 40)
        label.setText(self.name)
        # log
        log(f"{self} configured")

class addnewbutton(qbut):

    def __init__(self, name: str, position: int, parent: qwig):
        '''creates addnewbutton'''
        super().__init__(parent)
        self.name = name
        self.position = position
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures addnewbutton'''
        x = 30 + 150 * self.position
        self.setGeometry(x, 520, 130, 50)
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 25")
        self.setText(self.name)
        log(f"{self} configured")

class searchoptbutton(newbutton):

    def __init__(self, text: str, position: tuple, parent: qwig):
        '''creates searchoptbutton'''
        super().__init__(text, position, parent)
        self.configuresearchoptbutton()
        log(f"{self} created")

    def configuresearchoptbutton(self):
        '''configures searchoptbutton'''
        self.setStyleSheet("border-radius: 35; font-size: 20pt;")
        log(f"{self} configured")

class notificationwidget(qwig):

    def __init__(self, stage: qwig):
        '''creates notificationwidget'''
        super().__init__(stage)
        self.label = qlab(self)
        self.button = qbut(self)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures notificationlabel'''
        # self
        self.setObjectName("transparentwidget")
        self.setGeometry(0, 755, 1200, 40)
        # label
        label = self.label
        label.setGeometry(0, 10, 1155, 30)
        label.setObjectName("transparentlabel")
        # button
        button = self.button
        button.setGeometry(1155, 0, 40, 40)
        button.setObjectName("duskybutton")
        button.setStyleSheet("border-radius: 20")
        button.setIcon(qico(iconize("clear")))
        button.setIconSize(qsiz(30, 30))
        button.clicked.connect(self.clearnotification)
        # log
        log(f"{self} configured")

    def clearnotification(self):
        '''clears notificationlabel'''
        self.label.setText("")
        log("notification cleared")

class addnewidget(qwig):

    def __init__(self, stage: qwig):
        '''creates addnewidget'''
        super().__init__(stage)
        self.label = qlab(self)
        self.batch = addfield("Batch Number", 0, self)
        self.name = addfield("Medicine Name", 1, self)
        self.quantity = addfield("Quantity", 2, self)
        self.price = addfield("Price per Item", 3, self)
        self.addbutton = addnewbutton("Add", 0, self)
        self.clearbutton = addnewbutton("Clear", 1, self)
        self.closebutton = addnewbutton("Close", 6, self)        
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures addnewidget'''
        # self
        self.setObjectName("transparentwidget")
        self.setGeometry(50, 130, 1100, 590)
        # label
        label = self.label
        label.setGeometry(200, 15, 700, 55)
        label.setObjectName("addnewidgetlabel")
        label.setAlignment(centeralign)
        # log
        log(f"{self} configured")

    def closefunction(self):
        '''function of close button'''
        ui.newstage.setVisible(True)
        self.setVisible(False)
        log("newstage closed")

class purchasewidget(addnewidget):

    def __init__(self, stage: qwig):
        '''creates purchasewidget'''
        super().__init__(stage)
        self.dealer = addfield("Manufacturer", 4, self)
        self.buydate = addfield("Purchase Date: YYYY-MM-DD", 5, self)
        self.mfgdate = addfield("Manufacture Date: YYYY-MM(-DD)", 6, self)
        self.expdate = addfield("Expiry Date: YYYY-MM(-DD)", 7, self)
        self.configurepurchasebutton()
        log(f"{self} created")

    def configurepurchasebutton(self):
        '''configures purchasewidget'''
        self.batch.setFocus()
        # label
        label = self.label
        label.setText("New Purchase")
        # buttons
        button = self.closebutton
        button.clicked.connect(self.closefunction)
        button = self.clearbutton
        button.clicked.connect(self.clearfunction)
        button = self.addbutton
        button.clicked.connect(self.addfunction)
        # log
        log(f"{self} configured")

    def clearfunction(self):
        '''function of clear button'''
        allfields = [ self.batch, self.name, self.quantity, self.price, self.dealer, self.buydate, self.mfgdate, self.expdate ]
        for i in allfields:
            i.linedit.setText("")
        log("all fields cleared")

    def addfunction(self):
        '''function of add button'''
        batch = ui.purchasewidget.batch.linedit.text()
        name = ui.purchasewidget.name.linedit.text()
        quantity = ui.purchasewidget.quantity.linedit.text()
        price = ui.purchasewidget.price.linedit.text()
        dealer = ui.purchasewidget.dealer.linedit.text()
        buydate = ui.purchasewidget.buydate.linedit.text()
        mfgdate = ui.purchasewidget.mfgdate.linedit.text()
        expdate = ui.purchasewidget.expdate.linedit.text()
        info = [ batch, name, quantity, price, dealer, buydate, mfgdate, expdate ]
        addpurchase(info)

    def keyPressEvent(self, event: qkev):
        '''sets up keyboard functions'''
        lines = [ self.batch.linedit, self.name.linedit, self.quantity.linedit, self.price.linedit, self.dealer.linedit, self.buydate.linedit, self.mfgdate.linedit, self.expdate.linedit ]
        if event.key() == qt.Key_Up:
            focusedline = self.focusWidget()
            tofocus = lines[lines.index(focusedline) - 1]
            tofocus.setFocus()
        elif event.key() == qt.Key_Down:
            focusedline = self.focusWidget()
            index = lines.index(focusedline) + 1
            if index >= len(lines):
                index = 0
            tofocus = lines[index]
            tofocus.setFocus()
        elif event.key() == qt.Key_Return:
            self.addbutton.animateClick()
        elif event.key() == qt.Key_PageDown:
            self.clearbutton.animateClick()
        elif event.key() == qt.Key_Escape:
            self.closebutton.animateClick()

class sellwidget(addnewidget):

    def __init__(self, stage: qwig):
        '''creates sellwidget'''
        super().__init__(stage)
        self.customer = addfield("Customer", 4, self)
        self.selldate = addfield("Sell Date (YYYY-MM-DD)", 5, self)
        self.configuresellwidget()
        log(f"{self} created")

    def configuresellwidget(self):
        '''configures sellwidget'''
        self.batch.setFocus()
        # label
        label = self.label
        label.setText("New Sell")
        # buttons
        button = self.closebutton
        button.clicked.connect(self.closefunction)
        button = self.clearbutton
        button.clicked.connect(self.clearfunction)
        button = self.addbutton
        button.clicked.connect(self.addfunction)
        # log
        log(f"{self} configured")

    def clearfunction(self):
        '''function of clear button'''
        allfields = [ self.batch, self.name, self.quantity, self.price, self.customer, self.selldate ]
        for i in allfields:
            i.linedit.setText("")
        log("all fields cleared")

    def addfunction(self):
        '''function of add button'''
        batch = ui.sellwidget.batch.linedit.text()
        name = ui.sellwidget.name.linedit.text()
        quantity = ui.sellwidget.quantity.linedit.text()
        price = ui.sellwidget.price.linedit.text()
        customer = ui.sellwidget.customer.linedit.text()
        selldate = ui.sellwidget.selldate.linedit.text()
        info = [ batch, name, quantity, price, customer, selldate ]
        addsell(info)

    def keyPressEvent(self, event):
        '''sets up keyboard functions'''
        lines = [ self.batch.linedit, self.name.linedit, self.quantity.linedit, self.customer.linedit, self.selldate.linedit ]
        if event.key() == qt.Key_Up:
            focusedline = self.focusWidget()
            tofocus = lines[lines.index(focusedline) - 1]
            tofocus.setFocus()
        elif event.key() == qt.Key_Down:
            focusedline = self.focusWidget()
            index = lines.index(focusedline) + 1
            if index >= len(lines):
                index = 0
            tofocus = lines[index]
            tofocus.setFocus()
        elif event.key() == qt.Key_Return:
            self.addbutton.animateClick()
        elif event.key() == qt.Key_PageDown:
            self.clearbutton.animateClick()
        elif event.key() == qt.Key_Escape:
            self.closebutton.animateClick()

# search

class searchstage(newstage):

    def __init__(self, stage: qwig):
        '''creates searchstage'''
        super().__init__(stage)
        self.batchbutton = searchoptbutton("Batch Number", (0, 0), self)
        self.namebutton = searchoptbutton("Med Name", (0, 1), self)
        self.dealerbutton = searchoptbutton("Manufacturer", (1, 0), self)
        self.customerbutton = searchoptbutton("Customer", (1, 1), self)
        self.configuresearchstage()
        log(f"{self} created")

    def configuresearchstage(self):
        '''configures searchstage'''
        # label
        self.label.setText("Search")
        # buttons
        self.purchasebutton.setParent(None)
        self.sellbutton.setParent(None)
        self.batchbutton.clicked.connect(self.batchfunction)
        self.namebutton.clicked.connect(self.namefunction)
        self.dealerbutton.clicked.connect(self.dealerfunction)
        self.customerbutton.clicked.connect(self.customerfunction)
        # log
        log(f"{self} configured")

    def batchfunction(self):
        '''function of batchbutton'''
        stage = ui.searchbatch
        stage.setVisible(True)
        self.setVisible(False)
        log("searchbatch set visible")

    def namefunction(self):
        '''function of namebutton'''
        stage = ui.searchname
        stage.setVisible(True)
        self.setVisible(False)
        log("searchname set visible")

    def dealerfunction(self):
        '''function of dealerbutton'''
        stage = ui.searchdealer
        stage.setVisible(True)
        self.setVisible(False)
        log("searchdealer set visible")

    def customerfunction(self):
        '''function of customerbutton'''
        stage = ui.searchcustomer
        stage.setVisible(True)
        self.setVisible(False)
        log("searchcustomer set visible")

class searchwidget(qwig):

    def __init__(self, stage: qwig):
        '''creates searchwidget'''
        super().__init__(stage)
        self.label = searchlabel(self)
        self.inputline = searchinput(self)
        self.searchbutton = searchbutton("Search", 0, self)
        self.backbutton = searchbutton("Back", 1, self)
        self.previcon = qico(iconize("prev"))
        self.nexticon = qico(iconize("next"))
        self.prevbutton = qbut(self)
        self.nextbutton = qbut(self)
        self.searchresult0 = searchresultframe(self, "batchnumber", "tablename", 0)
        self.searchresult1 = searchresultframe(self, "batchnumber", "tablename", 1)
        self.searchresult2 = searchresultframe(self, "batchnumber", "tablename", 2)
        self.searchresult3 = searchresultframe(self, "batchnumber", "tablename", 3)
        self.searchresult4 = searchresultframe(self, "batchnumber", "tablename", 4)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures searchwidget'''
        # self
        self.setGeometry(25, 100, 1150, 650)
        self.setObjectName("transparentwidget")
        # label
        self.label.setGeometry(225, 15, 700, 55)
        # prevbutton
        self.prevbutton.setObjectName("duskybutton")
        self.prevbutton.setStyleSheet("border-radius: 25")
        self.prevbutton.setGeometry(230, 190, 50, 50)
        self.prevbutton.setIcon(self.previcon)
        self.prevbutton.setIconSize(qsiz(30, 30))
        # nextbutton
        self.nextbutton.setObjectName("duskybutton")
        self.nextbutton.setStyleSheet("border-radius: 25")
        self.nextbutton.setGeometry(870, 190, 50, 50)
        self.nextbutton.setIcon(self.nexticon)
        self.nextbutton.setIconSize(qsiz(30, 30))
        # buttons
        self.searchbutton.clicked.connect(self.searchfunction)
        self.backbutton.clicked.connect(self.backfunction)
        # log
        log(f"{self} configured")

    def searchfunction(self):
        '''function for searchbutton'''

        log("searchbutton pressed")

    def backfunction(self):
        '''function for backbutton'''
        ui.searchwidget.setVisible(True)
        self.setVisible(False)
        log("backbutton pressed")

    def keyPressEvent(self, event: qkev):
        if event.key() == qt.Key_Return:
            self.searchbutton.animateClick()
        if event.key() == qt.Key_Escape:
            self.backbutton.animateClick()

class searchlabel(qlab):

    def __init__(self, parent: searchwidget):
        '''creates searchlabel'''
        super().__init__(parent)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures searchlabel'''
        self.setGeometry(400, 35, 350, 45)
        self.setObjectName("searchlabel")
        self.setAlignment(centeralign)
        log(f"{self} configured")

class searchinput(qlin):

    def __init__(self, parent: searchwidget):
        '''creates searchinput'''
        super().__init__(parent)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures searchinput'''
        self.setGeometry(400, 100, 350, 40)
        self.setObjectName("addfieldline")
        log(f"{self} configured")

class searchbatch(searchwidget):

    def __init__(self, stage: qwig):
        '''creates searchbatch'''
        super().__init__(stage)
        self.label.setText("Batch Number")
        log(f"{self} created")

class searchbutton(qbut):

    def __init__(self, text: str, position: int, parent: searchwidget):
        '''creates searchbutton'''
        super().__init__(parent)
        self.text = text
        self.position = position
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures searchbutton'''
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 20")
        x = 410 + 180 * self.position
        self.setGeometry(x, 150, 150, 40)
        self.setText(self.text)
        log(f"{self} configured")

class searchname(searchwidget):

    def __init__(self, stage: qwig):
        '''creates searchname'''
        super().__init__(stage)
        self.label.setText("Medicine Name")
        log(f"{self} created")

class searchdealer(searchwidget):

    def __init__(self, stage: qwig):
        '''creates searchdealer'''
        super().__init__(stage)
        self.label.setText("Manufacturer")
        log(f"{self} created")

class searchcustomer(searchwidget):

    def __init__(self, stage: qwig):
        '''creates searchcustomer'''
        super().__init__(stage)
        self.label.setText("Customer")
        log(f"{self} created")

class searchresultframe(qfra):

    def __init__(self, stage: searchwidget, batch: str, table: str, position: int):
        '''creates searchresultframe'''
        super().__init__(stage)
        self.batch = batch
        self.table = table
        self.position = position
        self.label = qlab(self)
        self.button = searchresultbutton(self)
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures searchresultframe'''
        y = 260 + self.position * 80
        self.setGeometry(10, y, 1130, 60)
        self.setObjectName("searchresultframe")
        self.label.setGeometry(30, 10, 980, 40)
        self.label.setText(f"'{self.batch}' from '{self.table}'")
        self.label.setObjectName("searchresultlabel")
        log(f"{self} configured")

class searchresultbutton(qbut):

    def __init__(self, parent: searchresultframe):
        '''creates searchresultbutton'''
        super().__init__(parent)
        self.expand = qico(iconize("expand"))
        self.collapse = qico(iconize("collapse"))
        self.collapsed = True
        self.setIconSize(qsiz(40, 40))
        self.setIcon(self.expand)
        self.configure()
        log(f"{self} created")
        
    def configure(self):
        '''configures searchresultbutton'''
        self.setGeometry(1030, 0, 100, 60)
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 30")
        self.clicked.connect(self.selfclick)
        log(f"{self} created")

    def selfclick(self):
        '''function when button is clicked'''
        if self.collapsed:
            self.setIcon(self.collapse)
            self.collapsed = False
            log("medicine details expanded")
            return
        self.collapsed = True
        self.setIcon(self.expand)
        log("medicine details collapsed")

# settings

class settingstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates searchstage'''
        super().__init__(stage)
        self.frame = qfra(self)
        self.framelabel = qlab(self.frame)
        self.dark = settingsbutton(self.frame, (0, 0))
        self.light = settingsbutton(self.frame, (1, 0))
        self.themeoption = settingsoption(self, 0)
        self.configuresettings()
        log(f"{self} created")

    def configuresettings(self):
        '''configures searchstage'''
        # self
        self.setGeometry(50, 120, 1100, 600)
        self.setObjectName("transparentwidget")
        # hiding buttons
        buttons = [ self.dark, self.light ]
        for i in buttons:
            i.setVisible(False)
        # label
        self.label.setText("Settings")
        # frame
        self.frame.setGeometry(470, 180, 600, 400)
        self.frame.setObjectName("settingsframe")
        self.frame.setVisible(False)
        self.framelabel.setGeometry(200, 40, 200, 50)
        self.framelabel.setObjectName("settingsframelabel")
        self.framelabel.setAlignment(centeralign)
        # theme
        self.themeoption.setText("Theme")
        self.themeoption.clicked.connect(self.showthemes)
        # buttons
        self.dark.setText("dark")
        self.dark.clicked.connect(self.switchtodark)
        self.light.setText("light")
        self.light.clicked.connect(self.switchtolight)
        # log
        log(f"{self} configured")

    def showthemes(self):
        '''function to change theme'''
        self.framelabel.setText("Themes")
        check = self.themeoption.isChecked()
        widgets = [ self.frame, self.framelabel, self.dark, self.light ]
        for i in widgets:
            i.setVisible(check)
        log("themes shown")

    def switchtodark(self):
        '''changes to dark theme'''
        global theme
        with open("configuration.py", "r") as rfile:
            lines = rfile.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("qsheet"):
                lines[i] = "qsheet = 'darksheet.qss'"
        with open("configuration.py", "w") as wfile:
            wfile.writelines(lines)
        applyqsheet("darksheet.qss")
        theme = "dark"
        notify("switched to dark theme")
        log("switched to dark theme")

    def switchtolight(self):
        '''changes to light theme'''
        global theme
        with open("configuration.py", "r") as rfile:
            lines = rfile.readlines()
        for i in range(len(lines)):
            if lines[i].startswith("qsheet"):
                lines[i] = "qsheet = 'lightsheet.qss'"
        with open("configuration.py", "w") as wfile:
            wfile.writelines(lines)
        applyqsheet("lightsheet.qss")
        theme = "light"
        notify("switched to light theme")
        log("switched to light theme")

class settingsbutton(qbut):

    def __init__(self, parent: qfra, position: tuple):
        '''creates settingsbutton'''
        super().__init__(parent)
        self.x = position[0]
        self.y = position[1]
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures settingsbutton'''
        x = 100 + self.x * 250
        y = 170 + self.y * 90
        self.setGeometry(x, y, 150, 50)
        self.setObjectName("duskybutton")
        log(f"{self} configured")

class settingsoption(qbut):

    def __init__(self, parent: settingstage, position: int):
        '''creates settingsoption'''
        super().__init__(parent)
        self.position = position
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures settingsoption'''
        y = 220 + self.position * 70
        self.setGeometry(-20, y, 275, 40)
        self.setObjectName("duskybutton")
        self.setStyleSheet('''border-radius: 20; padding-left: 25; padding-right: 5;''')
        self.setCheckable(True)
        log(f"{self} configured")

# note

class notestage(tabstage):

    def __init__(self, stage: qwig):
        '''creates notestage'''
        super().__init__(stage)
        self.textbox = qtxt(self)
        self.clear = notebutton(self, 0)
        self.save  = notebutton(self, 1)
        self.load  = notebutton(self, 2)
        self.configurenote()
        log(f"{self} created")

    def configurenote(self):
        '''configures notestage'''
        # label
        self.label.setText("Note")
        # plain textedit
        self.textbox.setGeometry(10, 190, 1080, 400)
        self.textbox.setObjectName("notebox")
        if "note.txt" in os.listdir("resources"):
            with open("resources/note.txt", "r") as rfile:
                content = rfile.read()
                if content == "":
                    self.textbox.setPlaceholderText("Type note...")
                else:
                    self.textbox.setPlainText(content)
                    self.textbox.moveCursor(qcur.End)
        else:
            self.textbox.setPlaceholderText("Type note...")
        # save button
        self.save.setIcon(qico(iconize("save")))
        self.save.clicked.connect(self.savefunction)
        # clear button
        self.clear.setIcon(qico(iconize("delete")))
        self.clear.clicked.connect(self.clearfunction)
        # load button
        self.load.setIcon(qico(iconize("reload")))
        self.load.clicked.connect(self.loadfunction)
        # log
        log(f"{self} configured")

    def savefunction(self):
        '''function for save button'''
        with open("resources/note.txt", "w") as wfile:
            wfile.write(self.textbox.toPlainText())
        self.textbox.setFocus()
        self.textbox.moveCursor(qcur.End)
        notify("note saved")
        log("note saved")

    def clearfunction(self):
        '''function of clear button'''
        self.textbox.setPlaceholderText("Type note...")
        self.textbox.clear()
        self.textbox.setFocus()
        log("note textbox cleared")

    def loadfunction(self):
        '''function of clear button'''
        if "note.txt" in os.listdir("resources"):
            with open("resources/note.txt", "r") as rfile:
                self.textbox.setPlainText(rfile.read())
        else:
            notify("no saved note")
        self.textbox.setFocus()
        self.textbox.moveCursor(qcur.End)
        log("loaded note")

class notebutton(qbut):
    
    def __init__(self, stage: notestage, position: int):
        '''creates notebutton'''
        super().__init__(stage)
        self.position = position
        self.configure()
        log(f"{self} created")

    def configure(self):
        '''configures notebutton'''
        x = 1030 - self.position * 60
        self.setGeometry(x, 150, 50, 50)
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 25")
        self.setIconSize(qsiz(30, 30))
        log(f"{self} configured")

# stats

class statstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates statstage'''
        super().__init__(stage)
        self.configurestats()
        log(f"{self} created")

    def configurestats(self):
        '''configures statstage'''
        # label
        self.label.setText("Stats")
        # log
        log(f"{self} configured")

# chart

class chartstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates chartstage'''
        super().__init__(stage)
        self.configurechart()
        log(f"{self} created")

    def configurechart(self):
        '''configures chartstage'''
        # label
        self.label.setText("Chart")
        # log
        log(f"{self} configured")


### database connection

client = sql.connect(
    host = conf.host,
    username = conf.username,
    password = conf.password,
    database = conf.database
)
cursor = client.cursor()

### database related functions

def checkin(batch: str, tablename: str):
    '''checks if batch is available in table'''
    command = f'''select * from {tablename} where batch = "{batch}"'''
    cursor.execute(command)
    response = cursor.fetchone()
    if response is None:
        log(f"{batch} not found in {tablename}")
        return False
    log(f"{batch} found in {tablename}")
    return True

def isexpired(expdate: str = None, batch: str = None):
    '''returns True if medicine is expired'''

    # during selling
    if expdate is None:
        command = f'''select expdate from stock where batch = "{batch}"'''
        cursor.execute(command)
        expdate = cursor.fetchone()[0]
    
    # during buying
    else:
        year, month, day = tuple(expdate.split("-"))
        year, month, day = int(year), int(month), int(day)
        expdate = date(year, month, day)

    if expdate > date.today():
        log("medicine is not expired")
        return False
    log("medicine is expired")
    notify("medicine is expired")
    return True

def addpurchase(info: list):
    '''adds records to stock
       info = [ batch, name, quantity, price, dealer, buydate, mfgdate, expdate ]'''

    ## check if filled
    for i in info:
        if i == "" or i.isspace():
            notify("all fields are not filled")
            return

    ## converting info
    info[2] = eval(info[2])
    info[3] = eval(info[3])
    info[6] = info[6] + "-1"
    info[7] = info[7] + "-1"
    
    ## checking batch number

    # checking stock
    if checkin(info[0], "stock"):
        notify(f"'{info[0]}' already in stock")
        return
    else:

        # checking sold
        if checkin(info[0], "sold"):
            notify(f"'{info[0]}' already sold")
            return

        # checking expiry and adding
        else:
            if not isexpired(expdate=info[7]):
                command = f'''insert into stock values ("{info[0]}", "{info[1]}", {info[2]}, {info[3]}, "{info[4]}", "{info[5]}", "{info[6]}", "{info[7]}")'''
                cursor.execute(command)
                client.commit()
                notify(f"'{info[0]}' added to stock")

def addsell(info: list):
    '''adds record to sell
       info = [ batch, name, quantity, price, customer, selldate ]'''

    ## check if filled
    for i in info:
        if i == "" or i.isspace():
            notify("all fields are not filled")
            return

    ## converting info
    info[2] = int(info[2])
    info[3] = float(info[3])

    # checking batch
    if checkin(info[0], "stock"):
        
        # checking expiry
        if not isexpired(batch=info[0]):

            # moving from stock to sold
            command = f'''select * from stock where batch = "{info[0]}"'''
            cursor.execute(command)
            output = cursor.fetchone()
            command = f'''insert into sold values ("{info[0]}", "{info[1]}", {info[2]}, {info[3]}, "{output[4]}", "{info[4]}", "{output[5].isoformat()}", "{info[5].isoformat()}", "{output[6].isoformat()}", "{output[7].isoformat()}")'''
            cursor.execute(command)
            client.commit()
            command = f'''delete from stock where batch = "{info[0]}"'''
            cursor.execute(command)
            client.commit()

            # adding to sell
            command = f'''insert into sell values ("{info[0]}", "{info[1]}", {info[2]}, {info[3]}, "{info[4]}", "{info[5]}")'''
            cursor.execute(command)
            client.commit()
            notify(f"'{info[0]}' sold")

    else:
        log("could not sell expired medicine")
        notify(f"'{info[0]}' not in stock")

def dumpexpired():
    '''moves expired medicines to dumped'''
    today = date.today().isoformat()
    # copying from stock to dumped
    command = f'''insert into dumped select * from stock where expdate < "{today}"'''
    cursor.execute(command)
    client.commit()
    # deleting from stock
    command = f'''delete from stock where expdate < "{today}"'''
    cursor.execute(command)
    client.commit()
    # log
    log("expired medicines have been dumped")

def searchintables(table: str, column: str, value: str) -> list:
    '''returns records with matching values'''
    command = f'''select * from {table} where {column} = "{value}"'''
    cursor.execute(command)
    output = cursor.fetchall()
    return output

def searchdb(batch: str = None, name: str = None, dealer: str = None, customer: str = None) -> dict:
    '''returns infodict with matching parameters'''
    if customer is not None:
        infodict = dict()
        values = searchintables("sold", "customer", customer)
        infodict["sold"] = values
        return infodict
    if batch is None:
        if name is None:
            column, value = "dealer", dealer
        else:
            column, value = "medname", name
    else:
        column, value = "batch", batch
    tables = ["stock", "sold", "dumped"]
    infodict = dict()
    for i in tables:
        values = searchintables(i, column, value)
        infodict[i] = values
    return infodict

### main execution

if __name__ == "__main__":

    # try:

        ## creating new log file
        if conf.concise:
            logfile = open("log.txt", "w")

        ## creating app and main window
        app = qapp(sys.argv)
        log("appplication created")
        mainwindow = qwin()

        ## font
        qfdb.addApplicationFont("resources/Josefin Sans/JosefinSans-VariableFont_wght.ttf")
        app.setFont(qfon("Josefin Sans", 20, 450, False))
        log("font setup complete")

        ## creating interface
        ui = interface()
        ui.setupnew()
        mainwindow.show()
        log("interface created")

        ## switching tabs with tab
        shortkey = qkey("Ctrl+Tab")
        switch = qsho(shortkey, mainwindow)
        switch.activated.connect(switchtab)
        log("switch shortcut created")

        ## creating close shortcut
        shortkey = qkey("Ctrl+Q")
        close = qsho(shortkey, mainwindow)
        close.activated.connect(closefunction)
        log("close shortcut created")

        ## applying stylesheet
        applyqsheet()

        ## dumping expired medicines
        dumpexpired()

        ## closing application
        closefunction(app.exec_())

    # except Exception as error:
    #     log(error, "error")
