# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'step_3.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Confirmation import Ui_confirmation

class Ui_step_3(object):

    def confirmation_window(self):
        self.window_confirmation = QtWidgets.QMainWindow()
        self.ui = Ui_confirmation()
        self.ui.setupUi(self.window_confirmation)
        self.window_confirmation.show()

    def setupUi(self, step_3):
        step_3.setObjectName("step_3")
        step_3.resize(1024, 600)
        step_3.setMinimumSize(QtCore.QSize(1024, 600))
        step_3.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(step_3)
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
        self.TITLE_2.setGeometry(QtCore.QRect(310, 70, 401, 31))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE_2.setFont(font)
        self.TITLE_2.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE_2.setObjectName("TITLE_2")
        self.TITLE_3 = QtWidgets.QLabel(self.centralwidget)
        self.TITLE_3.setGeometry(QtCore.QRect(410, 130, 201, 141))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE_3.setFont(font)
        self.TITLE_3.setText("")
        self.TITLE_3.setPixmap(QtGui.QPixmap("../3rd step bandagign a wound.jpg"))
        self.TITLE_3.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE_3.setObjectName("TITLE_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 290, 761, 151))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.confirmation_window)
        self.pushButton.setGeometry(QtCore.QRect(790, 470, 221, 111))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 470, 221, 111))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        step_3.setCentralWidget(self.centralwidget)

        self.retranslateUi(step_3)
        QtCore.QMetaObject.connectSlotsByName(step_3)

    def retranslateUi(self, step_3):
        _translate = QtCore.QCoreApplication.translate
        step_3.setWindowTitle(_translate("step_3", "Step 3 Procedure"))
        self.TITLE.setText(_translate("step_3", "Bandaging a Wound"))
        self.TITLE_2.setText(_translate("step_3", "Step 3: Secure the bandage"))
        self.label.setText(_translate("step_3", " A) Tie or tape the bandage in place.\n"
"\n"
" B) Don\'t secure the bandage so tight that fingers or toes become pale or blue."))
        self.pushButton.setText(_translate("step_3", "Finish Step"))
        self.pushButton_3.setText(_translate("step_3", "Go back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    step_3 = QtWidgets.QMainWindow()
    ui = Ui_step_3()
    ui.setupUi(step_3)
    step_3.show()
    sys.exit(app.exec_())

