# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_injury.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Request_Nurse import Ui_request_nurse

class Ui_search_injury(object):

    def open_request_nurse(self):
        self.window_search_injury= QtWidgets.QMainWindow()
        self.ui = Ui_request_nurse()
        self.ui.setupUi(self.window_search_injury)
        self.window_search_injury.show()

    def setupUi(self, search_injury):
        search_injury.setObjectName("search_injury")
        search_injury.resize(1024, 600)
        search_injury.setMinimumSize(QtCore.QSize(1024, 600))
        search_injury.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(search_injury)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 0, 1021, 91))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 110, 731, 51))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.open_request_nurse)
        self.pushButton.setGeometry(QtCore.QRect(750, 110, 261, 121))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-10, 340, 1071, 271))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("1024x222 keyboard pi.png"))
        self.label.setObjectName("label")
        search_injury.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(search_injury)
        self.statusbar.setObjectName("statusbar")
        search_injury.setStatusBar(self.statusbar)

        self.retranslateUi(search_injury)
        QtCore.QMetaObject.connectSlotsByName(search_injury)

    def retranslateUi(self, search_injury):
        _translate = QtCore.QCoreApplication.translate
        search_injury.setWindowTitle(_translate("search_injury", "Search Injury"))
        self.TITLE.setText(_translate("search_injury", "Enter the type of Injury"))
        self.pushButton.setText(_translate("search_injury", "Enter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    search_injury = QtWidgets.QMainWindow()
    ui = Ui_search_injury()
    ui.setupUi(search_injury)
    search_injury.show()
    sys.exit(app.exec_())

