import sys
from PyQt5.QtWidgets import QApplication as qapp
from PyQt5.QtWidgets import QMainWindow as qwin
from PyQt5.QtWidgets import QShortcut as qsho
from PyQt5.QtGui import QKeySequence as qkes
from interface import interface
from functions import *


if __name__ == "__main__":
    app = qapp(sys.argv)
    log("application created")
    window = qwin()
    ui = interface(window)
    ui.setupnew()
    window.show()
    # close with Ctrl+Q
    close = qsho(qkes("Ctrl+Q"), window)
    close.activated.connect(lambda: closefunction(app))
    log("close shortcut created")
    sys.exit(app.exec_())
