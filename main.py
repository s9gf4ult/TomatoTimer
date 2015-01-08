import sys
import time
from PySide import QtCore, QtGui

import state

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.st = state.LogicFMS()

        self.resize(130, 50)
        self.setWindowTitle('TomatoTimer')

        self.btn_start = QtGui.QPushButton("Start", self)
        self.btn_stop = QtGui.QPushButton("Stop", self)
        self.btn_lpause = QtGui.QPushButton("Long Pause", self)
        self.btn_spause = QtGui.QPushButton("Short Pause", self)
        self.widget = QtGui.QLabel(str("25:00"), self)
        self.countPomidoro = QtGui.QLabel(str("1"), self)

        # timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timerTicked)
        self.timer.start(1000)

        # self.control.btn_start_click(self)

        # lcd
        self.lcd = QtGui.QLCDNumber()
        self.lcd.display('15:20')

        # layout
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.countPomidoro)
        self.layoutVertical.addWidget(self.lcd)
        self.layoutVertical.addWidget(self.btn_start)
        self.layoutVertical.addWidget(self.btn_stop)
        self.layoutVertical.addWidget(self.btn_lpause)
        self.layoutVertical.addWidget(self.btn_spause)

        # tray
        self.create_tray_icon()
        self.trayIcon.activated.connect(self.on_trayicon_activated)
        self.trayIcon.show()

        self.btn_lpause.hide()
        self.btn_spause.hide()

        # connect
        self.btn_start.clicked.connect(self.startClicked)
        self.btn_stop.clicked.connect(self.stopClicked)
        self.btn_lpause.clicked.connect(self.lpClicked)
        self.btn_spause.clicked.connect(self.spClicked)

        self.update_windonw(time.time())

    def timerTicked(self):
        t = time.time()
        self.someEvt(state.TickEvent(t), t)

    def startClicked(self):
        t = time.time()
        self.someEvt(state.StartEvent(t), t)

    def stopClicked(self):
        t = time.time()
        self.someEvt(state.StopEvent(), t)

    def lpClicked(self):
        t = time.time()
        self.someEvt(state.LongEvent(t), t)

    def spClicked(self):
        t = time.time()
        self.someEvt(state.ShortEvent(t), t)

    def someEvt(self, evt, t):
        self.st.next_state(evt)
        self.update_windonw(t)

    def updateLCD(self, t):
        rem = self.st.remining_time(t)
        if rem:
            self.lcd.show()
            self.lcd.display(time.strftime("%M:%S", time.gmtime(rem)))
        else:
            self.lcd.hide()
            self.lcd.display("00:00")

    def update_windonw(self, t):
        if isinstance(self.st.state, state.InitState):
            self.btn_spause.hide()
            self.btn_lpause.hide()
            self.btn_stop.hide()
            self.btn_start.show()
            self.widget.setText("Press Start to starting pomidoro")
        elif isinstance(self.st.state, (state.TomatoState, state.ShortState, state.LongState)):
            self.btn_spause.hide()
            self.btn_lpause.hide()
            self.btn_stop.show()
            self.btn_start.hide()
            self.widget.setText("Counting suka")
        elif isinstance(self.st.state, state.SelectState):
            self.btn_spause.show()
            self.btn_lpause.show()
            self.btn_stop.hide()
            self.btn_start.hide()
            self.widget.setText("Select pause suka")

        self.updateLCD(t)

        # if isinstance(self.st.state, state.InitState):
        #     self.widget.setText('Press Start to starting pomidoro')
        # elif isinstance(self.st.state, state.TomatoState):
        #     label_time = self.st.remining_time(self.evt)
        #     self.widget.setText(str(label_time))
        #     self.lcd.display(str(label_time))

    def create_tray_icon(self):
        icon = QtGui.QIcon('images/black-tomat.png')
        menu = QtGui.QMenu(self)
        resetAction = menu.addAction("Reset Pomidoro")
        # resetAction.triggered.connect(self.resetPomidoro)
        settingAction = menu.addAction("Settings")
        # settingAction.triggered.connect(self.dialog)
        settingAction.setDisabled(True)
        menu.addSeparator()
        exitAction = menu.addAction("Quit")
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.setIcon(icon)

    def on_trayicon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()

    def change_event(self, event):
        if event.type() == QtCore.QEvent.Close:
            event.ignore()
            self.close()
            return
        super().changeEvent(event)

    def close_event(self, event):
        even.ignore()
        self.hide()

    def open_dialog(self):
        dialog = Dialog(self)
        dialog.show()


class Dialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setWindowModality(QtCore.Qt.WindowModal)

        self.ttime = QtGui.QLabel(self)
        self.ttime.setText("Tomato Time")
        self.lpause = QtGui.QLabel(self)
        self.lpause.setText("Long Pause")
        self.spause = QtGui.QLabel(self)
        self.spause.setText("Short Pause")

        self.tt_spin = QtGui.QSpinBox()
        self.lp_spin = QtGui.QSpinBox()
        self.sp_spin = QtGui.QSpinBox()

        btnOk = QtGui.QPushButton("Ok")
        btnCancel = QtGui.QPushButton("Cancel")

        layout = QtGui.QGridLayout()
        layout.addWidget(self.ttime, 0, 0)
        layout.addWidget(self.lpause, 1, 0)
        layout.addWidget(self.spause, 2, 0)
        layout.addWidget(self.tt_spin, 0, 1)
        layout.addWidget(self.lp_spin, 1, 1)
        layout.addWidget(self.sp_spin, 2, 1)
        layout.addWidget(btnOk)
        layout.addWidget(btnCancel)
        self.setLayout(layout)

        btnCancel.clicked.connect(self.hide)

    def change_event(self, event):
        if event.type() == QtCore.QEvent.Quit:
            event.ignore()
            self.close()
            return
        super().changeEvent(event)

    def close_event(self, event):
        event.ignore()
        self.hide()



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('TomatoTimer')

    main = MainWindow()
    main.show()

    sys.exit(app.exec_())
