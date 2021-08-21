### imports

import sys
import time
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

def iconize(iconname: str) -> str:
    '''changes colour of icon'''
    if conf.qsheet.startswith("light"):
        filename = f"resources/whiteicons/{iconname}.svg"
    elif conf.qsheet.startswith("dark"):
        filename = f"resources/blackicons/{iconname}.svg"
    return filename

def switchtab():
    '''switches tabs'''
    tabs = [ ui.topframe.new, ui.topframe.search, ui.topframe.stats, ui.topframe.chart, ui.topframe.note ]
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
            self.topframe.note
        ]
        self.newidget = newidget(self)
        self.purchasewidget = purchasewidget(self)
        self.sellwidget = sellwidget(self)
        self.notificationwidget = notificationwidget(self)
        self.searchoptwidget = searchoptwidget(self)
        self.searchbatch = searchbatch(self)
        self.searchname = searchname(self)
        self.searchdealer = searchdealer(self)
        self.searchcustomer = searchcustomer(self)
        self.allwidgets = [ self.newidget, self.purchasewidget, self.sellwidget, self.searchoptwidget, self.searchbatch, self.searchname, self.searchdealer, self.searchcustomer ]

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
        log("topbuttons configured")

    def setupnew(self):
        '''sets up New tab'''
        refreshtopframe("New")
        refreshwindow(self.newidget)
        log("New tab setup")

    def setupsearch(self):
        '''sets up Search tab'''
        refreshtopframe("Search")
        refreshwindow(self.searchoptwidget)
        log("Search tab set up")

    def setupstats(self):
        '''sets up Stats tab'''
        refreshtopframe("Stats")
        refreshwindow()
        log("Stats tab set up")

    def setupchart(self):
        '''sets up Charts tab'''
        refreshtopframe("Chart")
        refreshwindow()
        log("Chart tab set up")

    def setupnote(self):
        '''sets up Note tab'''
        refreshtopframe("Note")
        refreshwindow()
        log("Note tab set up")

### custom widgets

class topbutton(qbut):

    def __init__(self, text: str, position: int, parent: qfra):
        super().__init__(parent)
        self.text = text
        self.position = position
        self.configure()
        log("topbutton created")

    def configure(self):
        '''configures topbutton'''
        self.setObjectName("topbutton")
        self.setText(self.text)
        self.setCursor(handcursor)
        x = 100 + 160 * self.position
        self.setGeometry(x, 10, 140, 40)
        self.setCheckable(True)
        log("topbutton configured")

class topframe(qfra):

    def __init__(self, stage: qfra):
        '''creates topframe'''
        super().__init__(stage)
        self.new = topbutton("New", 0, self)
        self.search = topbutton("Search", 1, self)
        self.stats = topbutton("Stats", 2, self)
        self.chart = topbutton("Chart", 3, self)
        self.note = topbutton("Note", 5, self)
        self.configure()
        log("topframe created")

    def configure(self):
        '''configures topframe'''
        self.setObjectName("topframe")
        self.setGeometry(17, 10, 1170, 60)
        log("topframe configured")

class newbutton(qbut):

    def __init__(self, text: str, position: tuple, parent: qwig):
        '''creates newbutton'''
        super().__init__(parent)
        self.position = position
        self.text = text
        self.configure()
        log("newbutton created")

    def configure(self):
        '''configures newbutton'''
        x = 100 + 400 * self.position[0]
        y = 190 + 110 * self.position[1]
        self.setObjectName("duskybutton")
        self.setText(self.text)
        self.setGeometry(x, y, 200, 75)
        self.setStyleSheet("border-radius: 37; font-size: 25pt;")
        log("newbutton configured")

class newidget(qwig):

    def __init__(self, stage: qwig):
        '''creates newidget'''
        super().__init__(stage)
        self.label = qlab(self)
        self.purchasebutton = newbutton("Purchase", (0, 1), self)
        self.sellbutton = newbutton("Sell", (1, 1), self)
        self.configure()
        log("newidget created")

    def configure(self):
        '''configures newidget'''
        # widget
        self.setGeometry(200, 200, 800, 425)
        self.setObjectName("transparentwidget")
        # label
        label = self.label
        label.setObjectName("newlabel")
        label.setText("medManage")
        label.setAlignment(centeralign)
        label.setGeometry(100, 50, 600, 100)
        # buttons
        button = self.purchasebutton
        button.clicked.connect(self.purchasebuttonfunction)
        button = self.sellbutton
        button.clicked.connect(self.sellbuttonfunction)
        # log
        log("newidget configured")

    def purchasebuttonfunction(self):
        '''function of purchase button'''
        ui.purchasewidget.setVisible(True)
        self.setVisible(False)
        log("addpurchasewidget opened")

    def sellbuttonfunction(self):
        '''function of sell button'''
        ui.sellwidget.setVisible(True)
        self.setVisible(False)
        log("addsellwidget opened")

class addfield(qwig):

    def __init__(self, name: str, position: int, stage: qwig):
        '''creates addfield'''
        super().__init__(stage)
        self.name = name
        self.position = position
        self.linedit = qlin(self)
        self.label = qlab(self)
        self.configure()
        log("addfield created")

    def configure(self):
        '''''configures addfield'''
        # widget
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
        log("addfield configured")

class addnewbutton(qbut):

    def __init__(self, name: str, position: int, parent: qwig):
        '''creates addnewbutton'''
        super().__init__(parent)
        self.name = name
        self.position = position
        self.configure()
        log("addnewbutton created")

    def configure(self):
        '''configures addnewbutton'''
        x = 30 + 150 * self.position
        self.setGeometry(x, 520, 130, 50)
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 25")
        self.setText(self.name)
        log("addnewbutton configured")

class searchoptbutton(newbutton):

    def __init__(self, text: str, position: tuple, parent: qwig):
        '''creates searchoptbutton'''
        super().__init__(text, position, parent)
        self.configuresearchoptbutton()
        log("searchoptbutton created")

    def configuresearchoptbutton(self):
        '''configures searchoptbutton'''
        self.setStyleSheet("border-radius: 35; font-size: 20pt;")
        log("searchoptbutton configured")

class searchoptwidget(newidget):

    def __init__(self, stage: qwig):
        '''creates searchoptwidget'''
        super().__init__(stage)
        self.batchbutton = searchoptbutton("Batch Number", (0, 0), self)
        self.namebutton = searchoptbutton("Med Name", (0, 1), self)
        self.dealerbutton = searchoptbutton("Manufacturer", (1, 0), self)
        self.customerbutton = searchoptbutton("Customer", (1, 1), self)
        self.configuresearchoptwidget()
        log("searchoptwidget created")

    def configuresearchoptwidget(self):
        '''configures searchoptwidget'''
        self.purchasebutton.setParent(None)
        self.sellbutton.setParent(None)
        self.batchbutton.clicked.connect(self.batchfunction)
        self.namebutton.clicked.connect(self.namefunction)
        self.dealerbutton.clicked.connect(self.dealerfunction)
        self.customerbutton.clicked.connect(self.customerfunction)
        self.label.setText("Search")
        self.label.setGeometry(100, 0, 600, 100)
        log("searchoptwidget configured")

    def batchfunction(self):
        '''function of batchbutton'''
        stage = ui.searchbatch
        stage.setVisible(True)
        self.setVisible(False)

    def namefunction(self):
        '''function of namebutton'''
        stage = ui.searchname
        stage.setVisible(True)
        self.setVisible(False)

    def dealerfunction(self):
        '''function of dealerbutton'''
        stage = ui.searchdealer
        stage.setVisible(True)
        self.setVisible(False)

    def customerfunction(self):
        '''function of customerbutton'''
        stage = ui.searchcustomer
        stage.setVisible(True)
        self.setVisible(False)

class notificationwidget(qwig):

    def __init__(self, stage: qwig):
        '''creates notificationwidget'''
        super().__init__(stage)
        self.label = qlab(self)
        self.button = qbut(self)
        self.configure()
        log("notificationwidget created")

    def configure(self):
        '''configures notificationlabel'''
        # widget
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
        log("configured notificationwidget")

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
        log("adnewidget created")

    def configure(self):
        '''configures addnewidget'''
        # widget
        self.setObjectName("transparentwidget")
        self.setGeometry(50, 130, 1100, 590)
        # label
        label = self.label
        label.setGeometry(200, 15, 700, 55)
        label.setObjectName("addnewidgetlabel")
        label.setAlignment(centeralign)
        # log
        log("addnewidget configured")

    def closefunction(self):
        '''function of close button'''
        ui.newidget.setVisible(True)
        self.setVisible(False)
        log("addnewidget closed")

class purchasewidget(addnewidget):

    def __init__(self, stage: qwig):
        '''creates purchasewidget'''
        super().__init__(stage)
        self.dealer = addfield("Manufacturer", 4, self)
        self.buydate = addfield("Purchase Date (YYYY-MM-DD)", 5, self)
        self.mfgdate = addfield("Manufacture Date (YYYY-MM-DD)", 6, self)
        self.expdate = addfield("Expiry Date (YYYY-MM-DD)", 7, self)
        self.configurepurchasebutton()
        log("purchasewidget created")

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
        log("purchasewidget configured")

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

    def keyPressEvent(self, event):
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
        elif event.key() == qt.Key_Escape:
            self.closebutton.animateClick()

class sellwidget(addnewidget):

    def __init__(self, stage: qwig):
        '''creates sellwidget'''
        super().__init__(stage)
        self.customer = addfield("Customer", 4, self)
        self.selldate = addfield("Sell Date (YYYY-MM-DD)", 5, self)
        self.configuresellwidget()
        log("sellwidget created")

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
        log("sellwidget configured")

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
        elif event.key() == qt.Key_Escape:
            self.closebutton.animateClick()

class searchstage(qwig):

    def __init__(self, stage: qwig):
        '''creates searchstage'''
        super().__init__(stage)
        self.label = searchlabel(self)
        self.inputline = searchinput(self)
        self.searchbutton = searchbutton("Search", 0, self)
        self.backbutton = searchbutton("Back", 1, self)
        self.configure()
        log("searchstage created")

    def configure(self):
        '''configures searchstage'''
        self.setGeometry(25, 100, 1150, 650)
        self.setObjectName("transparentwidget")
        self.searchbutton.clicked.connect(self.searchfunction)
        self.backbutton.clicked.connect(self.backfunction)
        log("searchstage configured")

    def searchfunction(self):
        '''function for searchbutton'''
        log("searchbutton pressed")

    def backfunction(self):
        '''function for backbutton'''
        ui.searchoptwidget.setVisible(True)
        self.setVisible(False)
        log("backbutton pressed")

    def keyPressEvent(self, event: qkev):
        if event.key() == qt.Key_Return:
            self.searchbutton.animateClick()
        if event.key() == qt.Key_Escape:
            self.backbutton.animateClick()

class searchlabel(qlab):

    def __init__(self, parent: searchstage):
        '''creates searchlabel'''
        super().__init__(parent)
        self.configure()
        log("searchlabel created")

    def configure(self):
        '''configures searchlabel'''
        self.setGeometry(400, 35, 350, 45)
        self.setObjectName("searchlabel")
        self.setAlignment(centeralign)
        log("searchlabel configured")

class searchinput(qlin):

    def __init__(self, parent: searchstage):
        '''creates searchinput'''
        super().__init__(parent)
        self.configure()
        log("searchinput created")

    def configure(self):
        '''configures searchinput'''
        self.setGeometry(400, 100, 350, 40)
        self.setObjectName("addfieldline")
        log("searchinput configured")

class searchbatch(searchstage):

    def __init__(self, stage: qwig):
        '''creates searchbatch'''
        super().__init__(stage)
        self.label.setText("Batch Number")
        log("searchbatch created")

class searchbutton(qbut):

    def __init__(self, text: str, position: int, parent: searchstage):
        '''creates searchbutton'''
        super().__init__(parent)
        self.text = text
        self.position = position
        self.configure()
        log("searchbutton created")

    def configure(self):
        '''configures searchbutton'''
        self.setObjectName("duskybutton")
        self.setStyleSheet("border-radius: 20")
        x = 410 + 180 * self.position
        self.setGeometry(x, 150, 150, 40)
        self.setText(self.text)
        log("searchbutton configured")

class searchname(searchstage):

    def __init__(self, stage: qwig):
        '''creates searchname'''
        super().__init__(stage)
        self.label.setText("Medicine Name")
        log("searchname created")

class searchdealer(searchstage):

    def __init__(self, stage: qwig):
        '''creates searchdealer'''
        super().__init__(stage)
        self.label.setText("Manufacturer")
        log("searchdealer created")

class searchcustomer(searchstage):

    def __init__(self, stage: qwig):
        '''creates searchcustomer'''
        super().__init__(stage)
        self.label.setText("Customer")
        log("searchcustomer created")

class searchresultframe(qfra):

    def __init__(self, stage: searchstage, batch: str, table: str, position: int):
        '''creates searchresultframe'''
        super().__init__(stage)
        self.batch = batch
        self.table = table
        self.position = position
        self.expand = qico(iconize("expand"))
        self.collapse = qico(iconize("collapse"))
        self.label = qlab(self)
        self.button = searchresultbutton(self)
        self.configure()
        log("searchresultframe created")

    def configure(self):
        '''configures searchresultframe'''
        self.setGeometry(10, 180, 1130, 60)
        self.setObjectName("searchresultframe")
        self.label.setGeometry(30, 10, 980, 40)
        self.label.setText(f"'{self.batch}' from '{self.table}'")
        self.label.setObjectName("searchresultlabel")
        self.button.setGeometry(1030, 0, 100, 60)
        self.button.setObjectName("searchresultbutton")
        log("searchresultframe configured")

class searchresultbutton(qbut):

    def __init__(self, parent: searchresultframe):
        '''creates searchresultbutton'''
        
    def configure(self):
        '''configures searchresultbutton'''

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

    try:

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
        shortkey = qkey("Tab")
        switch = qsho(shortkey, mainwindow)
        switch.activated.connect(switchtab)
        log("switch shortcut created")

        ## creating close shortcut
        shortkey = qkey("Ctrl+Q")
        close = qsho(shortkey, mainwindow)
        close.activated.connect(closefunction)
        log("close shortcut created")

        ## applying stylesheet
        with open(conf.qsheet, "r") as sheet:
            app.setStyleSheet(sheet.read())
        log(f"{conf.qsheet} applied")

        ## dumping expired medicines
        dumpexpired()

        ## closing application
        closefunction(app.exec_())

    except Exception as error:
        log(error, "error")
