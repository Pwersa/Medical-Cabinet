# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'step_1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Step_2 import Ui_step_2

class Ui_step_1(object):

    def open_step_2_window(self):
        self.window_step_2 = QtWidgets.QMainWindow()
        self.ui = Ui_step_2()
        self.ui.setupUi(self.window_step_2)
        self.window_step_2.show()

    def setupUi(self, step_1):
        step_1.setObjectName("step_1")
        step_1.resize(1024, 600)
        step_1.setMinimumSize(QtCore.QSize(1024, 600))
        step_1.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(step_1)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 0, 1021, 71))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(24)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.TITLE_2 = QtWidgets.QLabel(self.centralwidget)
        self.TITLE_2.setGeometry(QtCore.QRect(330, 70, 361, 31))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE_2.setFont(font)
        self.TITLE_2.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE_2.setObjectName("TITLE_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 260, 981, 211))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.TITLE_3 = QtWidgets.QLabel(self.centralwidget)
        self.TITLE_3.setGeometry(QtCore.QRect(410, 110, 201, 141))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE_3.setFont(font)
        self.TITLE_3.setText("")
        self.TITLE_3.setPixmap(QtGui.QPixmap("../1st step bandagign a wound.jpg"))
        self.TITLE_3.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE_3.setObjectName("TITLE_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.open_step_2_window)
        self.pushButton.setGeometry(QtCore.QRect(790, 480, 221, 111))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 480, 221, 111))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        step_1.setCentralWidget(self.centralwidget)

        self.retranslateUi(step_1)
        QtCore.QMetaObject.connectSlotsByName(step_1)

    def retranslateUi(self, step_1):
        _translate = QtCore.QCoreApplication.translate
        step_1.setWindowTitle(_translate("step_1", "Step 1 Procedure"))
        self.TITLE.setText(_translate("step_1", "Bandaging a Wound"))
        self.TITLE_2.setText(_translate("step_1", "Step 1: Clean the Wound"))
        self.label.setText(_translate("step_1", " A) Put on gloves or use other protection to avoid contact with the victim\'s blood.\n"
"\n"
" B) Clean the wound with mild soap and water.\n"
"\n"
" C) Apply a small layer of topical antibiotic if desired.\n"
"\n"
" D) Place a clean dressing over the entire wound. Gauze dressings let in air for faster healing. Nonstick dressings have a special surface that won\'t cling to the wound.\n"
"\n"
" E) If blood soaks through the dressing, place another dressing over the first one."))
        self.pushButton.setText(_translate("step_1", "NEXT STEP"))
        self.pushButton_2.setText(_translate("step_1", "GO BACK TO \n"
" BODY PARTS"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    step_1 = QtWidgets.QMainWindow()
    ui = Ui_step_1()
    ui.setupUi(step_1)
    step_1.show()
    sys.exit(app.exec_())

