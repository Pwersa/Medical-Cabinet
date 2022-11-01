# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'request_nurse.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from select_body_part import *
from select_injury_type import *
from search_injury import *
from scan_qr_code import *


class nurse_request_window(object):
    
    def open_main_window_qr(self):
        body_parts_window.hide()
        injury_type_window.hide()
        search_injur_window.hide()
        qr_window_app.show()
        #nurse_request_window.hide()
    
    def setupUi(self, nurse_request_window):
        nurse_request_window.setObjectName("nurse_request_window")
        nurse_request_window.resize(1024, 600)
        nurse_request_window.setMinimumSize(QtCore.QSize(1024, 600))
        nurse_request_window.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(nurse_request_window)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 50, 1021, 311))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.open_main_window_qr)
        self.pushButton.setGeometry(QtCore.QRect(330, 420, 361, 131))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        nurse_request_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(nurse_request_window)
        self.statusbar.setObjectName("statusbar")
        nurse_request_window.setStatusBar(self.statusbar)

        self.retranslateUi(nurse_request_window)
        QtCore.QMetaObject.connectSlotsByName(nurse_request_window)

    def retranslateUi(self, nurse_request_window):
        _translate = QtCore.QCoreApplication.translate
        nurse_request_window.setWindowTitle(_translate("nurse_request_window", "nurse_request_window"))
        self.TITLE.setText(_translate("nurse_request_window", "Please wait for a \n"
" Clinic Staff to arrive."))
        self.pushButton.setText(_translate("nurse_request_window", "End Procedure"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    nurse_request_window = QtWidgets.QMainWindow()
    ui = nurse_request_window()
    ui.setupUi(nurse_request_window)
    nurse_request_window.show()
    sys.exit(app.exec_())