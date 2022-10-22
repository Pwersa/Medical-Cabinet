# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'request_nurse.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_request_nurse(object):
    def setupUi(self, request_nurse):
        request_nurse.setObjectName("request_nurse")
        request_nurse.resize(1024, 600)
        request_nurse.setMinimumSize(QtCore.QSize(1024, 600))
        request_nurse.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(request_nurse)
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
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(330, 420, 361, 131))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        request_nurse.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(request_nurse)
        self.statusbar.setObjectName("statusbar")
        request_nurse.setStatusBar(self.statusbar)

        self.retranslateUi(request_nurse)
        QtCore.QMetaObject.connectSlotsByName(request_nurse)

    def retranslateUi(self, request_nurse):
        _translate = QtCore.QCoreApplication.translate
        request_nurse.setWindowTitle(_translate("request_nurse", "Request Nurse Assistance"))
        self.TITLE.setText(_translate("request_nurse", "Please wait for a \n"
" Clinic Staff to arrive."))
        self.pushButton.setText(_translate("request_nurse", "End Procedure"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    request_nurse = QtWidgets.QMainWindow()
    ui = Ui_request_nurse()
    ui.setupUi(request_nurse)
    request_nurse.show()
    sys.exit(app.exec_())

