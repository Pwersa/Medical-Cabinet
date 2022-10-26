# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirmation.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_confirmation(object):
    def setupUi(self, confirmation):
        confirmation.setObjectName("confirmation")
        confirmation.resize(1024, 600)
        confirmation.setMinimumSize(QtCore.QSize(1024, 600))
        confirmation.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(confirmation)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 40, 1021, 91))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(170, 250, 291, 161))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(560, 250, 271, 161))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        confirmation.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(confirmation)
        self.statusbar.setObjectName("statusbar")
        confirmation.setStatusBar(self.statusbar)

        self.retranslateUi(confirmation)
        QtCore.QMetaObject.connectSlotsByName(confirmation)

    def retranslateUi(self, confirmation):
        _translate = QtCore.QCoreApplication.translate
        confirmation.setWindowTitle(_translate("confirmation", "Confirmation Procedure"))
        self.TITLE.setText(_translate("confirmation", "End procedure?"))
        self.pushButton_2.setText(_translate("confirmation", "No"))
        self.pushButton_3.setText(_translate("confirmation", "Yes"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    confirmation = QtWidgets.QMainWindow()
    ui = Ui_confirmation()
    ui.setupUi(confirmation)
    confirmation.show()
    sys.exit(app.exec_())

