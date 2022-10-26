# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_injury_type.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Step_1 import Ui_step_1
from Search_Injury import *

injury_type = ["Cut", "Wound", "Puncture", "Burn", "Others", "Go back to window"]

class Ui_select_injury_type(object):

    def open_procedure_window(self, injury_type):
        if injury_type == "Cut":
            self.window_step_1= QtWidgets.QMainWindow()
            self.ui = Ui_step_1()
            self.ui.setupUi(self.window_step_1)
            self.window_step_1.show()
        
        elif injury_type == "Wound":
            select_injury_type.close()
            print("Wound")
        
        elif injury_type == "Puncture":
            print("Puncture")

        elif injury_type == "Burn":
            print("Burn")
        
        elif injury_type == "Others":
            self.window_search_injury = QtWidgets.QMainWindow()
            self.ui = Ui_search_injury()
            self.ui.setupUi(self.window_search_injury)
            self.window_search_injury.show()
        
        elif injury_type == "Go back to window":
            print("Go back to window")

    def setupUi(self, select_injury_type):
        select_injury_type.setObjectName("select_injury_type")
        select_injury_type.resize(1024, 600)
        select_injury_type.setMinimumSize(QtCore.QSize(1024, 600))
        select_injury_type.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(select_injury_type)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 10, 1021, 91))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")

        # Button for Wound
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_procedure_window(injury_type[1]))
        self.pushButton_2.setGeometry(QtCore.QRect(360, 120, 311, 191))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        #Button for CUT
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_procedure_window(injury_type[0]))
        self.pushButton_3.setGeometry(QtCore.QRect(20, 120, 311, 191))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        #BUTTON FOR BURN
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_procedure_window(injury_type[3]))
        self.pushButton_4.setGeometry(QtCore.QRect(20, 350, 311, 191))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        #BUTTON FOR PUNCTURE
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_procedure_window(injury_type[2]))
        self.pushButton_5.setGeometry(QtCore.QRect(700, 120, 301, 191))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        #BUTTON FOR OTHERS
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_procedure_window(injury_type[4]))
        self.pushButton_6.setGeometry(QtCore.QRect(360, 350, 311, 191))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")

        #BUTTON FOR GOING BACK
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_procedure_window(injury_type[5]))
        self.pushButton_7.setGeometry(QtCore.QRect(700, 350, 311, 191))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        select_injury_type.setCentralWidget(self.centralwidget)

        self.retranslateUi(select_injury_type)
        QtCore.QMetaObject.connectSlotsByName(select_injury_type)

    def retranslateUi(self, select_injury_type):
        _translate = QtCore.QCoreApplication.translate
        select_injury_type.setWindowTitle(_translate("select_injury_type", "Select Type of Injury"))
        self.TITLE.setText(_translate("select_injury_type", "Select type of Injury"))
        self.pushButton_2.setText(_translate("select_injury_type", "WOUND"))
        self.pushButton_3.setText(_translate("select_injury_type", "CUT"))
        self.pushButton_4.setText(_translate("select_injury_type", "BURN"))
        self.pushButton_5.setText(_translate("select_injury_type", "PUNCTURE"))
        self.pushButton_6.setText(_translate("select_injury_type", "OTHERS"))
        self.pushButton_7.setText(_translate("select_injury_type", "GO BACK TO \n"
"BODY PARTS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    select_injury_type = QtWidgets.QMainWindow()
    ui = Ui_select_injury_type()
    ui.setupUi(select_injury_type)
    select_injury_type.show()
    sys.exit(app.exec_())

