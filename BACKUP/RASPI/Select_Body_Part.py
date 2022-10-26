# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_body_part.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Select_Injury_Type import *

class Ui_select_body_part(object):
    
    def select_injury_type_window(self):
        self.window_select_injury_type = QtWidgets.QMainWindow()
        self.ui = Ui_select_injury_type()
        self.ui.setupUi(self.window_select_injury_type)
        self.window_select_injury_type.show()

    def setupUi(self, select_body_part):
        select_body_part.setObjectName("select_body_part")
        select_body_part.resize(1024, 600)
        select_body_part.setMinimumSize(QtCore.QSize(1024, 600))
        select_body_part.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(select_body_part)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 0, 1021, 91))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(24)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.body_part = QtWidgets.QLabel(self.centralwidget)
        self.body_part.setGeometry(QtCore.QRect(10, 60, 1001, 521))
        self.body_part.setText("")
        self.body_part.setTextFormat(QtCore.Qt.PlainText)
        self.body_part.setPixmap(QtGui.QPixmap("../test/body_part.png"))
        self.body_part.setObjectName("body_part")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.select_injury_type_window)
        self.pushButton.setGeometry(QtCore.QRect(761, 308, 171, 71))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(36)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        select_body_part.setCentralWidget(self.centralwidget)

        self.retranslateUi(select_body_part)
        QtCore.QMetaObject.connectSlotsByName(select_body_part)

    def retranslateUi(self, select_body_part):
        _translate = QtCore.QCoreApplication.translate
        select_body_part.setWindowTitle(_translate("select_body_part", "Select Body Part"))
        self.TITLE.setText(_translate("select_body_part", "Select body Part"))
        self.pushButton.setText(_translate("select_body_part", "HAND"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    select_body_part = QtWidgets.QMainWindow()
    ui = Ui_select_body_part()
    ui.setupUi(select_body_part)
    select_body_part.show()
    sys.exit(app.exec_())