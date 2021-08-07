from PyQt5.QtWidgets import QApplication as qapp
concise = True

def log(message: str):
    '''logs messages to console if concise mode is on'''
    if concise:
        print("log:", message)

def closefunction(app: qapp):
    '''logs and closes the application'''
    log("closing application")
    app.exit(0)

def refreshtopbar(tab: str, bar):
    '''selects and unselects topbuttons'''
    buttons = [ bar.new, bar.search, bar.chart, bar.note ]
    for i in buttons:
        if i.objectName().startswith(tab):
            i.isselected(True)
        else:
            i.isselected(False)
    log("topbar refreshed")

def refreshwidgets(requiredwidgets: list, allwidgets: list):
    '''hides and shows widgets'''
    for i in allwidgets:
        if i in requiredwidgets:
            i.setVisible(True)
        else:
            i.setVisible(False)
