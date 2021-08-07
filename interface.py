from PyQt5.QtWidgets import QMainWindow as qwin
from PyQt5.QtCore import QSize as qsiz
from PyQt5.QtGui import QIcon as qico
from PyQt5.QtGui import QFont as qfon
from stylesheets import *
from functions import *
from objects import *


class interface:

    def __init__(self, window: qwin):
        log("interface class created")
        self.window = window
        self.configurewindow()
        self.topbar = topbar(window)
        self.configuretopbuttons()
        self.addbox = addbox(window)
        # all widgets
        self.all = [self.addbox]

    def configurewindow(self):
        '''configures main window'''
        window = self.window
        window.setWindowTitle("medManage")
        iconfile = "resources/icon.svg"
        icon = qico(iconfile)
        window.setWindowIcon(icon)
        window.setFixedSize(1200, 800)
        window.setFont(qfon("Josefin Sans", 20))
        window.setStyleSheet(windowdark)
        log("window configured")

    def configuretopbuttons(self):
        '''configures topbuttons'''
        self.topbar.new.clicked.connect(self.setupnew)
        self.topbar.search.clicked.connect(self.setupsearch)
        self.topbar.stats.clicked.connect(self.setupstats)
        self.topbar.chart.clicked.connect(self.setupchart)
        self.topbar.note.clicked.connect(self.setupnote)
        log("topbuttons configured")

    def setupnew(self):
        '''sets up new tab'''
        refreshtopbar("new", self.topbar)
        reqd = [self.addbox]
        refreshwidgets(reqd, self.all)
        log("setup new tab")

    def setupsearch(self):
        '''sets up search tab'''
        refreshtopbar("search", self.topbar)
        reqd = []
        refreshwidgets(reqd, self.all)
        log("setup search tab")

    def setupstats(self):
        '''sets up stats tab'''
        refreshtopbar("stats", self.topbar)
        reqd = []
        refreshwidgets(reqd, self.all)
        log("setup stats tab")

    def setupchart(self):
        '''sets up chart tab'''
        refreshtopbar("chart", self.topbar)
        reqd = []
        refreshwidgets(reqd, self.all)
        log("setup chart tab")

    def setupnote(self):
        '''sets up note tab'''
        refreshtopbar("note", self.topbar)
        reqd = []
        refreshwidgets(reqd, self.all)
        log("setup note tab")