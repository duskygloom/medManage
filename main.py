### imports

import sys
import time
import os
from PyQt5.QtWidgets import QPlainTextEdit as qtxt
from PyQt5.QtWidgets import QApplication as qapp
from PyQt5.QtWidgets import QMainWindow as qwin
from PyQt5.QtWidgets import QPushButton as qbut
from PyQt5.QtWidgets import QScrollArea as qscr
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



### variables

handcursor = qt.PointingHandCursor
centeralign = qt.AlignCenter
middlealign = qt.AlignVCenter

if "dark" in conf.qsheet:
    theme = "dark"
else:
    theme = "light"

logging = conf.concise



### global functions


def log(message: str, category: str = "log"):
    '''logs message to terminal'''
    if logging:
        # printing on console
        text = f">>> {time.asctime()}\n{category}: {message}"
        print(text)
        # writing on file
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


def refreshcheckedbuttons(buttontext: str, allbuttons: list):
    '''clicks and unclicks topbuttons'''
    for i in allbuttons:
        if i.text == buttontext:
            i.setChecked(True)
        else:
            i.setChecked(False)
    log("topbuttons refreshed")


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
    black = os.path.join("resources", "blackicons", f"{iconname}.svg")
    white = os.path.join("resources", "whiteicons", f"{iconname}.svg")
    with open(black, "r") as rfile:
        content = rfile.read()
    with open(white, "w") as wfile:
        wfile.write(content.replace("#212121", "#e9e9e9"))


def iconize(iconname: str) -> str:
    '''changes colour of icon'''
    if theme == "dark":
        filename = os.path.join("resources", "blackicons", f"{iconname}.svg")
    elif theme == "light":
        dirname = os.path.join("resources", "whiteicons")
        if "whiteicons" not in os.listdir("resources"):
            os.mkdir(dirname)
        if f"{iconname}.svg" not in os.listdir(dirname):
            iconconvert(iconname)
        filename = os.path.join("resources", "whiteicons", f"{iconname}.svg")
    return filename


def switchtab(style: int = 0):
    '''switches tabs
       style 0 is left to right
       style 1 is right to left'''
    tabs = ui.alltopbuttons
    for i in range(len(tabs)):
        if tabs[i].isChecked():
            if style == 0:
                index = i + 1
                if index >= len(tabs):
                    index = 0
                break
            elif style == 1:
                index = i - 1
                if index <= -1:
                    index = len(tabs) - 1
                break        
    tabs[index].animateClick()



### main interface class


class interface(qwig):

    def __init__(self):
        '''creates interface class'''
        super().__init__(mainwindow)
        self.configurewindow()
        self.configure()
        self.topframe = topframe(self)
        self.configuretopbuttons()
        self.alltopbuttons = [self.topframe.new, self.topframe.search, self.topframe.stats, self.topframe.chart, self.topframe.note, self.topframe.settings]
        self.newstage = newstage(self)
        self.purchasewidget = purchasewidget(self)
        self.sellwidget = sellwidget(self)
        self.notificationwidget = notificationwidget(self)
        self.searchstage = searchstage(self)
        self.searchwidget = searchwidget(self)
        self.settingstage = settingstage(self)
        self.notestage = notestage(self)
        self.chartstage = chartstage(self)
        self.statstage = statstage(self)
        self.allwidgets = [ self.newstage, self.purchasewidget, self.sellwidget, self.searchstage, self.searchwidget, self.settingstage, self.notestage, self.chartstage, self.statstage ]

    def configure(self):
        '''configures main widget'''
        self.setGeometry(0, 0, 1200, 800)
        self.setObjectName("stagewidget")
        log("created topframe")

    def configurewindow(self):
        '''configures mainwindow'''
        window = mainwindow
        window.setObjectName("mainwindow")
        window.setWindowTitle("medManage")
        window.setWindowIcon(qico(os.path.join("resources", "icon.svg")))
        window.setFixedSize(1200, 800)
        log("mainwindow created")

    def configuretopbuttons(self):
        '''configures topbuttons'''
        frame = self.topframe
        frame.new.clicked.connect(self.setupnew)
        frame.search.clicked.connect(self.setupsearch)
        frame.stats.clicked.connect(self.setupstats)
        frame.chart.clicked.connect(self.setupchart)
        frame.note.clicked.connect(self.setupnote)
        frame.settings.clicked.connect(self.setupsettings)
        log("topbuttons created")

    def setupnew(self):
        '''sets up New tab'''
        refreshcheckedbuttons("New", ui.alltopbuttons)
        refreshwindow(self.newstage)
        log("New tab setup")

    def setupsearch(self):
        '''sets up Search tab'''
        refreshcheckedbuttons("Search", ui.alltopbuttons)
        refreshwindow(self.searchstage)
        log("Search tab set up")

    def setupstats(self):
        '''sets up Stats tab'''
        refreshcheckedbuttons("Stats", ui.alltopbuttons)
        refreshwindow(self.statstage)
        self.statstage.updatestage()
        log("Stats tab set up")

    def setupchart(self):
        '''sets up Charts tab'''
        refreshcheckedbuttons("Chart", ui.alltopbuttons)
        refreshwindow(self.chartstage)
        log("Chart tab set up")

    def setupnote(self):
        '''sets up Note tab'''
        refreshcheckedbuttons("Note", ui.alltopbuttons)
        refreshwindow(self.notestage)
        self.notestage.textbox.setFocus()
        log("Note tab set up")
    
    def setupsettings(self):
        '''sets up Settings tab'''
        refreshcheckedbuttons("Settings", ui.alltopbuttons)
        refreshwindow(self.settingstage)
        log("Settings tab set up")



### default widgets


class topbutton(qbut):

    def __init__(self, text: str, position: int, parent: qfra):
        '''buttons in the topbar'''
        super().__init__(parent)
        self.text = text
        self.position = position
        self.setObjectName("topbutton")
        self.setText(self.text)
        self.setCursor(handcursor)
        x = 33 + 160 * self.position
        self.setGeometry(x, 10, 140, 40)
        self.setCheckable(True)
        log(f"{self} created")


class topframe(qfra):

    def __init__(self, stage: qfra):
        '''topbar containing tabs'''
        super().__init__(stage)
        self.new = topbutton("New", 0, self)
        self.search = topbutton("Search", 1, self)
        self.stats = topbutton("Stats", 2, self)
        self.chart = topbutton("Chart", 3, self)
        self.note = topbutton("Note", 5, self)
        self.settings = topbutton("Settings", 6, self)
        self.setObjectName("topframe")
        self.setGeometry(17, 10, 1170, 60)
        log(f"{self} created")


class tabstage(qwig):

    def __init__(self, stage: qwig):
        '''general stage for all tabs'''
        super().__init__(stage)
        self.label = qlab(self)
        # self
        self.setGeometry(50, 120, 1100, 600)
        self.setObjectName("transparentwidget")
        # label
        self.label.setGeometry(250, 50, 600, 100)
        self.label.setObjectName("tabstagelabel")
        self.label.setAlignment(centeralign)
        # log
        log(f"{self} created")



# widgets in new tab


class duskybutton(qbut):

    def __init__(self, text: str, position: tuple, parent: qwig):
        '''default type of button'''
        super().__init__(parent)
        self.position = position
        self.text = text
        x = 250 + 400 * self.position[0]
        y = 250 + 110 * self.position[1]
        self.setObjectName("duskybutton")
        self.setText(self.text)
        self.setCursor(handcursor)
        self.setGeometry(x, y, 200, 75)
        log(f"{self} created")


class newstage(tabstage):

    def __init__(self, stage: qwig):
        '''stage for new tab'''
        super().__init__(stage)
        self.purchasebutton = duskybutton("Purchase", (0, 1), self)
        self.sellbutton = duskybutton("Sell", (1, 1), self)
        # label
        self.label.setText("medManage")
        # buttons
        button = self.purchasebutton
        button.clicked.connect(self.purchasebuttonfunction)
        button = self.sellbutton
        button.clicked.connect(self.sellbuttonfunction)
        # log
        log(f"{self} created")

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
        '''input box'''
        super().__init__(stage)
        self.name = name
        self.position = position
        self.linedit = qlin(self)
        self.label = qlab(self)
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
        log(f"{self} created")

class addduskybutton(qbut):

    def __init__(self, name: str, position: int, parent: qwig):
        '''creates addduskybutton'''
        super().__init__(parent)
        self.name = name
        self.position = position
        x = 30 + 150 * self.position
        self.setGeometry(x, 520, 130, 50)
        self.setObjectName("duskybutton")
        self.setCursor(handcursor)
        self.setStyleSheet("border-radius: 25")
        self.setText(self.name)
        log(f"{self} created")

class searchoptbutton(duskybutton):

    def __init__(self, text: str, position: tuple, parent: qwig):
        '''creates searchoptbutton'''
        super().__init__(text, position, parent)
        log(f"{self} created")

class notificationwidget(qwig):

    def __init__(self, stage: qwig):
        '''creates notificationwidget'''
        super().__init__(stage)
        self.label = qlab(self)
        self.button = qbut(self)
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
        button.setCursor(handcursor)
        button.clicked.connect(self.clearnotification)
        # log
        log(f"{self} created")

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
        self.addbutton = addduskybutton("Add", 0, self)
        self.clearbutton = addduskybutton("Clear", 1, self)
        self.closebutton = addduskybutton("Close", 6, self)
        # self
        self.setObjectName("transparentwidget")
        self.setGeometry(50, 130, 1100, 590)
        # label
        label = self.label
        label.setGeometry(200, 15, 700, 55)
        label.setObjectName("addnewidgetlabel")
        label.setAlignment(centeralign)
        # log
        log(f"{self} created")

    def closefunction(self):
        '''function of close button'''
        ui.newstage.setVisible(True)
        self.setVisible(False)
        log("newstage closed")

class purchasewidget(addnewidget):

    def __init__(self, stage: qwig):
        '''creates purchasewidget'''
        super().__init__(stage)
        self.cp = addfield("Cost Price per Item", 3, self)
        self.dealer = addfield("Manufacturer", 4, self)
        self.buydate = addfield("Purchase Date: YYYY-MM-DD", 5, self)
        self.mfgdate = addfield("Manufacture Date: YYYY-MM(-DD)", 6, self)
        self.expdate = addfield("Expiry Date: YYYY-MM(-DD)", 7, self)
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
        log(f"{self} created")

    def clearfunction(self):
        '''function of clear button'''
        allfields = [ self.batch, self.name, self.quantity, self.cp, self.dealer, self.buydate, self.mfgdate, self.expdate ]
        for i in allfields:
            i.linedit.setText("")
        log("all fields cleared")

    def addfunction(self):
        '''function of add button'''
        batch = ui.purchasewidget.batch.linedit.text()
        name = ui.purchasewidget.name.linedit.text()
        quantity = ui.purchasewidget.quantity.linedit.text()
        cp = ui.purchasewidget.cp.linedit.text()
        dealer = ui.purchasewidget.dealer.linedit.text()
        buydate = ui.purchasewidget.buydate.linedit.text()
        mfgdate = ui.purchasewidget.mfgdate.linedit.text()
        expdate = ui.purchasewidget.expdate.linedit.text()
        info = [ batch, name, quantity, cp, dealer, buydate, mfgdate, expdate ]
        addpurchase(info)

    def keyPressEvent(self, event: qkev):
        '''sets up keyboard functions'''
        lines = [ self.batch.linedit, self.name.linedit, self.quantity.linedit, self.cp.linedit, self.dealer.linedit, self.buydate.linedit, self.mfgdate.linedit, self.expdate.linedit ]
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
        self.batch.deleteLater()
        self.quantity.deleteLater()
        self.name.deleteLater()
        self.batch = addfield("Batch number", 2, self)
        self.sp = addfield("Sell Price per Item", 3, self)
        self.customer = addfield("Customer", 4, self)
        self.selldate = addfield("Sell Date (YYYY-MM-DD)", 5, self)
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
        log(f"{self} created")

    def clearfunction(self):
        '''function of clear button'''
        allfields = [ self.batch, self.sp, self.customer, self.selldate ]
        for i in allfields:
            i.linedit.setText("")
        log("all fields cleared")

    def addfunction(self):
        '''function of add button'''
        batch = self.batch.linedit.text()
        sp = self.sp.linedit.text()
        customer = self.customer.linedit.text()
        selldate = self.selldate.linedit.text()
        info = [ batch, sp, customer, selldate ]
        addsell(info)

    def keyPressEvent(self, event):
        '''sets up keyboard functions'''
        lines = [ self.batch.linedit, self.sp.linedit, self.customer.linedit, self.selldate.linedit ]
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
        super().__init__(stage) #flag2
        self.batchbutton = searchoptbutton("Batch Number", (0, 0), self)
        self.namebutton = searchoptbutton("Med Name", (0, 1), self)
        self.dealerbutton = searchoptbutton("Manufacturer", (1, 0), self)
        self.customerbutton = searchoptbutton("Customer", (1, 1), self)
        # label
        self.label.setText("Search")
        # buttons
        self.purchasebutton.deleteLater()
        self.sellbutton.deleteLater()
        self.batchbutton.clicked.connect(self.batchfunction)
        self.namebutton.clicked.connect(self.namefunction)
        self.dealerbutton.clicked.connect(self.dealerfunction)
        self.customerbutton.clicked.connect(self.customerfunction)
        # log
        log(f"{self} created")

    def batchfunction(self):
        '''function of batchbutton'''
        ui.searchwidget.updatewidget("batch")
        ui.searchwidget.setVisible(True)
        self.setVisible(False)
        log("searchwidget set visible")

    def namefunction(self):
        '''function of namebutton'''
        ui.searchwidget.updatewidget("medname")
        ui.searchwidget.setVisible(True)
        self.setVisible(False)
        log("searchwidget set visible")

    def dealerfunction(self):
        '''function of dealerbutton'''
        ui.searchwidget.updatewidget("dealer")
        ui.searchwidget.setVisible(True)
        self.setVisible(False)
        log("searchwidget set visible")

    def customerfunction(self):
        '''function of customerbutton'''
        ui.searchwidget.updatewidget("customer")
        ui.searchwidget.setVisible(True)
        self.setVisible(False)
        log("searchwidget set visible")

class searchwidget(qwig):

    def __init__(self, stage: qwig):
        '''creates searchwidget'''
        super().__init__(stage)
        self.label = searchlabel(self)
        self.inputline = searchinput(self)
        self.searchbutton = searchbutton("Search", 0, self)
        self.backbutton = searchbutton("Back", 1, self)
        self.resultbox = searchresultbox(self)
        # self
        self.setGeometry(25, 100, 1150, 650)
        self.setObjectName("transparentwidget")
        # label
        self.label.setGeometry(225, 15, 700, 55)
        # buttons
        self.searchbutton.clicked.connect(self.searchfunction)
        self.backbutton.clicked.connect(self.backfunction)
        log(f"{self} created")

    def updatewidget(self, type: str):
        '''updates searchwidget'''
        self.type = type
        self.inputline.setText("")
        for i in ui.searchwidget.resultbox.children():
            i.setVisible(False)
        if type == "batch":
            self.label.setText("Batch Number")
        elif type == "medname":
            self.label.setText("Med Name")
        elif type == "dealer":
            self.label.setText("Manufacturer")
        elif type == "customer":
            self.label.setText("Customer")
        log(f"{self} updated")

    def searchfunction(self):
        '''searches medicine'''
        info = searchdb(self.type, self.inputline.text())
        self.resultbox.showresults(info)

    def backfunction(self):
        '''function for backbutton'''
        ui.searchstage.setVisible(True)
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
        self.setGeometry(400, 35, 350, 45)
        self.setObjectName("searchlabel")
        self.setAlignment(centeralign)
        log(f"{self} created")


class searchinput(qlin):

    def __init__(self, parent: searchwidget):
        '''creates searchinput'''
        super().__init__(parent)
        self.setGeometry(400, 100, 350, 40)
        self.setObjectName("addfieldline")
        log(f"{self} created")


class searchbutton(qbut):

    def __init__(self, text: str, position: int, parent: searchwidget):
        '''creates searchbutton'''
        super().__init__(parent)
        self.text = text
        self.position = position
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 20")
        x = 410 + 180 * self.position
        self.setGeometry(x, 150, 150, 40)
        self.setText(self.text)
        self.setCursor(handcursor)
        log(f"{self} created")


class searchresultbox(qscr):

    def __init__(self, stage: searchwidget):
        '''creates searchresultbox'''
        super().__init__(stage)
        # not found label
        self.nflabel = qlab(self)
        self.nflabel.setGeometry(400, 70, 300, 30)
        self.nflabel.setObjectName("noresultlabel")
        self.nflabel.setText("No Result Found")
        self.nflabel.setAlignment(centeralign)
        self.nflabel.setVisible(False)
        # self
        self.setGeometry(25, 225, 1100, 400)
        self.setObjectName("transparentscrollarea")
        log(f"{self} created")

    def showresults(self, matches: list):
        '''shows results'''
        noresult = True
        for i in self.children():
            i.setVisible(False)
        for i in range(len(matches)):
            info = {}
            for j in matches[i]:
                if j != "table":
                    if matches[i][j] != "":
                        info[j] = matches[i][j]
            searchresultwidget(self, info, i, matches[i]["Batch Number"], matches[i]["table"]).show()
            self.nflabel.setVisible(False)
            log("search results shown")
            noresult = False
        if noresult:
            self.nflabel.setVisible(True)


class searchresultwidget(qfra):

    def __init__(self, box: searchresultbox, info: dict, position: int, batchnumber:str, tablename: str):
        '''creates searchresultwidget'''
        super().__init__(box)
        y = 10 + position * 50
        self.setGeometry(10, y, 1065, 40)
        self.setObjectName("topframe")
        self.setStyleSheet("border-radius: 20;")
        # label
        self.label = qlab(self)
        self.label.setText(f"{batchnumber} from {tablename}")
        self.label.setObjectName("transparentlabel")
        self.label.setGeometry(20, 5, 920, 30)
        # button
        self.button = qbut(self)
        self.button.setObjectName("duskybutton")
        self.button.setStyleSheet("border-radius: 20")
        self.button.setGeometry(965, 0, 100, 40)
        self.button.setIconSize(qsiz(30, 30))
        self.button.setIcon(qico(iconize("expand")))
        self.button.setCursor(handcursor)
        self.button.clicked.connect(self.buttonclick)
        # info label
        self.infolabel = qlab(ui.searchwidget.resultbox)
        self.infolabel.setGeometry(250, 25, 600, 350)
        self.infolabel.setObjectName("infolabel")
        text = ""
        for i in info:
            text += f"{i}: {info[i]}\n"
        self.infolabel.setText(text)
        self.infolabel.setVisible(False)
        log(f"{self} created")

    def buttonclick(self):
        '''function for button click'''
        if self.infolabel.isVisible():
            self.infolabel.setVisible(False)
            self.button.setIcon(qico(iconize("expand")))
        else:
            self.infolabel.setVisible(True)
            self.infolabel.raise_()
            self.button.setIcon(qico(iconize("collapse")))
        log(f"{self} clicked")


# settings

class settingstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates searchstage'''
        super().__init__(stage)
        self.frame = qfra(self)
        self.framelabel = qlab(self.frame)
        self.dark  = settingsbutton(self.frame, (0, 0))
        self.light = settingsbutton(self.frame, (1, 0))
        self.themeoption = settingsoption(self, 0)
        self.logoption   = settingsoption(self, 1)
        self.logyes = settingsbutton(self.frame, (0, 0))
        self.logno  = settingsbutton(self.frame, (1, 0))
        self.alloptions = [ self.themeoption, self.logoption ]
        self.allbuttons = [ self.dark, self.light, self.logyes, self.logno ]
        self.themeoption.animateClick()
        # self
        self.setGeometry(50, 120, 1100, 600)
        self.setObjectName("transparentwidget")
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
        # log
        self.logoption.setText("Logging")
        self.logoption.clicked.connect(self.showlogging)
        # buttons
        self.dark.setText("dark")
        self.dark.clicked.connect(lambda: self.switchtheme("dark"))
        self.light.setText("light")
        self.light.clicked.connect(lambda: self.switchtheme("light"))
        self.logyes.setText("Yes")
        self.logyes.clicked.connect(lambda: self.createlog(True))
        self.logno.setText("No")
        self.logno.clicked.connect(lambda: self.createlog(False))
        # log
        log(f"{self} created")

    def showthemes(self):
        '''function to change theme'''
        self.framelabel.setText("Themes")
        widgets = [ self.frame, self.framelabel, self.dark, self.light ]
        for i in widgets:
            i.setVisible(True)
        for i in self.allbuttons:
            if i not in widgets:
                i.setVisible(False)
        log("themes shown")

    def switchtheme(self, themename: str):
        '''changes to dark theme'''
        global theme
        with open("configuration.py", "r") as rfile:
            lines = rfile.readlines()
        lines[7] = f"qsheet = '{themename}sheet.qss'\n"
        with open("configuration.py", "w") as wfile:
            wfile.writelines(lines)
        applyqsheet(f"{themename}sheet.qss")
        theme = themename
        notify(f"switched to {themename} theme... restart to update icons")
        log(f"switched to {themename} theme")

    def showlogging(self):
        '''function to change logginig status'''
        self.framelabel.setText("Logging")
        widgets = [ self.frame, self.framelabel, self.logyes, self.logno ]
        for i in widgets:
            i.setVisible(True)
        for i in self.allbuttons:
            if i not in widgets:
                i.setVisible(False)
        log("logging shown")

    def createlog(self, status: bool = True):
        '''toggles the option for logging'''
        global logging
        with open("configuration.py", "r") as rfile:
            lines = rfile.readlines()
        lines[5] = f"concise = {status}\n"
        with open("configuration.py", "w") as wfile:
            wfile.writelines(lines)
        logging = status
        log(f"logging set to {status}")
        notify(f"logging set to {status}")

class settingsbutton(qbut):

    def __init__(self, parent: qfra, position: tuple):
        '''creates settingsbutton'''
        super().__init__(parent)
        self.x = position[0]
        self.y = position[1]
        x = 100 + self.x * 250
        y = 170 + self.y * 90
        self.setGeometry(x, y, 150, 50)
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 25")
        self.setCursor(handcursor)
        log(f"{self} created")

class settingsoption(qbut):

    def __init__(self, parent: settingstage, position: int):
        '''creates settingsoption'''
        super().__init__(parent)
        self.position = position
        y = 220 + self.position * 70
        self.setGeometry(-20, y, 275, 40)
        self.setObjectName("duskybutton")
        self.setStyleSheet('''border-radius: 20; padding-left: 25; padding-right: 5;''')
        self.setCursor(handcursor)
        log(f"{self} created")

# note

class notestage(tabstage):

    def __init__(self, stage: qwig):
        '''creates notestage'''
        super().__init__(stage)
        self.textbox = qtxt(self)
        self.clear = notebutton(self, 0)
        self.save  = notebutton(self, 1)
        self.load  = notebutton(self, 2)
        # label
        self.label.setText("Note")
        # plain textedit
        self.textbox.setGeometry(10, 190, 1080, 400)
        self.textbox.setObjectName("notebox")
        if "note.txt" in os.listdir("resources"):
            with open(os.path.join("resources", "note.txt"), "r") as rfile:
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
        log(f"{self} created")

    def savefunction(self):
        '''function for save button'''
        with open(os.path.join("resources", "note.txt"), "w") as wfile:
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
            with open(os.path.join("resources", "note.txt"), "r") as rfile:
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
        x = 1030 - self.position * 60
        self.setGeometry(x, 150, 50, 50)
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 25")
        self.setIconSize(qsiz(30, 30))
        self.setCursor(handcursor)
        log(f"{self} created")

# stats

class statstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates statstage'''
        super().__init__(stage)
        info = getstats()
        self.bought = statsbox(self, "Medicines Bought", info[0], 0)
        self.stocked = statsbox(self, "Medicines Stocked", info[1], 1)
        self.sold = statsbox(self, "Medicines Sold", info[2], 2)
        self.expired = statsbox(self, "Medicines Expired", info[3], 3)
        self.expenditure = statsbox(self, "Total Expenditure", info[4], 4)
        self.earning = statsbox(self, "Total Earning", info[5], 5)
        self.profit = statsbox(self, "Total Profit", info[6], 6)
        self.loss = statsbox(self, "Total Loss", info[7], 7)
        # label
        self.label.setText("Stats")
        # log
        log(f"{self} created")

    def updatestage(self):
        '''updates statstage'''
        info = getstats()
        labellist = [self.bought, self.stocked, self.sold, self.expired, self.expenditure, self.earning, self.profit, self.loss]
        for i in range(8):
            labellist[i].valuelabel.setText(str(info[i]))

class statsbox(qwig):

    def __init__(self, stage: tabstage, title: str, value, position: int):
        '''creates statsbox'''
        super().__init__(stage)
        self.title = title
        self.value = str(value)
        self.position = position
        self.titlelabel = qlab(self)
        self.valuelabel = qlab(self)
        if self.position < 4:
            y = 180 + self.position * 50
        else:
            y = 400 + (self.position - 4) * 50
        self.setGeometry(100, y, 900, 40)
        self.setObjectName("transparentwidget")
        # title
        label = self.titlelabel
        label.setGeometry(10, 0, 430, 40)
        label.setText(self.title)
        label.setObjectName("statslabel")
        # value
        label = self.valuelabel
        label.setGeometry(460, 0, 430, 40)
        label.setText(self.value)
        label.setObjectName("statslabel")
        log(f"{self} created")


# chart

class chartstage(tabstage):

    def __init__(self, stage: qwig):
        '''creates chartstage'''
        super().__init__(stage)
        # label
        self.label.setText("Chart")
        # log
        log(f"{self} created")


class chartstage(newstage):

    def __init__(self, stage: qwig):
        '''select between finance and stocks charts'''
        super().__init__(stage)
        # label
        self.label.setText("Charts")
        # buttons
        self.purchasebutton.deleteLater()
        self.sellbutton.deleteLater()
        self.financebutton = searchoptbutton("Finance", (0, 1), self)
        self.financebutton.clicked.connect(self.financefunc)
        self.stocksbutton  = searchoptbutton("Stocks", (1, 1), self)
        self.stocksbutton.clicked.connect(self.stocksfunc)
        # log
        log(f"{self} created")

    def financefunc(self):
        '''displays finance chart'''

    def stocksfunc(self):
        '''displays stocks chart'''


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
       info = [ batch, name, quantity, cp, dealer, buydate, mfgdate, expdate ]'''

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
    '''adds record to sold
       info = [ batch, name, quantity, cp, sp, dealer, customer, buydate, selldate, mfg, exp ]'''

    ## check if filled
    for i in info:
        if i == "" or i.isspace():
            notify("all fields are not filled")
            return

    ## converting info
    info[1] = eval(info[1])

    # checking batch
    if checkin(info[0], "stock"):
        
        # checking expiry
        if not isexpired(batch=info[0]):

            # moving from stock to sold
            command = f'''select * from stock where batch = "{info[0]}"'''
            cursor.execute(command)
            output = cursor.fetchone()
            command = f'''insert into sold values ("{info[0]}", "{output[1]}", {output[2]}, {output[3]}, {info[1]}, "{output[4]}", "{info[2]}", "{output[5].isoformat()}", "{info[3]}", "{output[6].isoformat()}", "{output[7].isoformat()}")'''
            cursor.execute(command)
            client.commit()
            command = f'''delete from stock where batch = "{info[0]}"'''
            cursor.execute(command)
            client.commit()
            notify(f"'{info[0]}' sold")

    else:
        log("could not sell expired medicine")
        notify(f"'{info[0]}' has expired")

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

## matches[i] = {"table": <tablename>, "Batch Number": <batch>, "Name": <medname> "Quantity": <quantity>, "Cost Price per Item": <cp>, "Sell Price per Item": <sp>, "Manufacturer": <dealer>, "Customer": <customer>, "Date of Purchase": <buydate>, "Date of Sell": <selldate>, "Manufacture Date": <mfgdate>, "Expiry Date": <expdate>} if data not available -> empty string

def searchstock(column: str, value: str) -> list:
    '''returns list of matching results'''
    command = f"select * from stock where {column} = '{value}'"
    cursor.execute(command)
    output = cursor.fetchall()
    matches = []
    for i in output:
        match = {
            "table": "stock",
            "Batch Number": i[0],
            "Name": i[1],
            "Quantity": i[2],
            "Cost Price per Item": i[3],
            "Sell Price per Item": "",
            "Manufacturer": i[4],
            "Customer": "",
            "Date of Purchase": i[5].isoformat(),
            "Date of Sell": "",
            "Manufacture Date": i[6].isoformat(),
            "Expiry Date": i[7].isoformat()
        }
        matches.append(match)
    return matches

def searchsold(column: str, value: str) -> list:
    '''returns list of matching results'''
    command = f"select * from sold where {column} = '{value}'"
    cursor.execute(command)
    output = cursor.fetchall()
    matches = []
    for i in output:
        match = {
            "table": "sold",
            "Batch Number": i[0],
            "Name": i[1],
            "Quantity": i[2],
            "Cost Price per Item": i[3],
            "Sell Price per Item": i[4],
            "Manufacturer": i[5],
            "Customer": i[6],
            "Date of Purchase": i[7].isoformat(),
            "Date of Sell": i[8].isoformat(),
            "Manufacture Date": i[9].isoformat(),
            "Expiry Date": i[10].isoformat()
        }
        matches.append(match)
    return matches

def searchdumped(column: str, value: str) -> list:
    '''returns list of matching results'''
    command = f"select * from dumped where {column} = '{value}'"
    cursor.execute(command)
    output = cursor.fetchall()
    matches = []
    for i in output:
        match = {
            "table": "dumped",
            "Batch Number": i[0],
            "Name": i[1],
            "Quantity": i[2],
            "Cost Price per Item": i[3],
            "Sell Price per Item": "",
            "Manufacturer": i[4],
            "Customer": "",
            "Date of Purchase": i[5].isoformat(),
            "Date of Sell": "",
            "Manufacture Date": i[6].isoformat(),
            "Expiry Date": i[7].isoformat()
        }
        matches.append(match)
    return matches

def searchdb(column: str, value: str) -> list:
    '''returns list of matching value in column'''
    fromsold   = searchsold(column, value)
    if column == "customer":
        return fromsold
    fromdumped = searchdumped(column, value)
    fromstock  = searchstock(column, value)
    fromall    = fromstock + fromdumped + fromsold
    return fromall

def checklen(tablename: str) -> int:
    '''returns the length of tablename'''
    command = f"select batch from {tablename}"
    cursor.execute(command)
    length = len(cursor.fetchall())
    return length

def getcost(tablename: str, sp=False) -> float:
    '''returns total cost of tablename'''
    if sp:
        command = f"select quantity, sp from sold"
    else:
        command = f"select quantity, cp from {tablename}"
    cursor.execute(command)
    output = cursor.fetchall()
    cost = 0
    for i in output:
        cost += i[0] * i[1]
    return cost

def getstats() -> list:
    '''returns list of stats
       [bought, stocked, sold, expired, expenditure, earning, profit, loss]'''
    stocked = checklen("stock")
    sold = checklen("sold")
    bought = sold + stocked
    expired = checklen("dumped")
    soldcp = getcost("sold")
    soldsp = getcost("sold", sp=True)
    expenditure = getcost("stock") + soldcp
    earning = soldsp
    profit = 0
    loss = 0
    if soldsp > soldcp:
        profit = soldsp - soldcp
    else:
        loss = getcost("dumped") + soldcp - soldsp
    return [bought, stocked, sold, expired, expenditure, earning, profit, loss]

### main execution

if __name__ == "__main__":

    try:

        ## creating new log file
        if conf.concise:
            logfile = open("log.txt", "w")

        ## creating app and main window
        app = qapp(sys.argv)
        log("appplication created")
        mainwindow = qwin()

        ## font
        qfdb.addApplicationFont(os.path.join("resources", "Josefin Sans", "static", "JosefinSans-Regular.ttf"))
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
        shortkey = qkey("Ctrl+Shift+Tab")
        switch = qsho(shortkey, mainwindow)
        switch.activated.connect(lambda: switchtab(1))
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

    except Exception as error:
        log(error, "error")
