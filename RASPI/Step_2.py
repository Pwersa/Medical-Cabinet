# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'step_2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Step_3 import Ui_step_3

class Ui_step_2(object):

    def open_step_3_window(self):
        self.window_step_3 = QtWidgets.QMainWindow()
        self.ui = Ui_step_3()
        self.ui.setupUi(self.window_step_3)
        self.window_step_3.show()

    def setupUi(self, step_2):
        step_2.setObjectName("step_2")
        step_2.resize(1024, 600)
        step_2.setMinimumSize(QtCore.QSize(1024, 600))
        step_2.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(step_2)
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
        self.TITLE_2.setGeometry(QtCore.QRect(320, 70, 381, 31))
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
        self.TITLE_3.setPixmap(QtGui.QPixmap("../2nd step bandagign a wound.jpg"))
        self.TITLE_3.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE_3.setObjectName("TITLE_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(120, 280, 801, 171))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.open_step_3_window)
        self.pushButton.setGeometry(QtCore.QRect(780, 470, 221, 111))
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
        step_2.setCentralWidget(self.centralwidget)

        self.retranslateUi(step_2)
        QtCore.QMetaObject.connectSlotsByName(step_2)

    def retranslateUi(self, step_2):
        _translate = QtCore.QCoreApplication.translate
        step_2.setWindowTitle(_translate("step_2", "Step 2 Procedure"))
        self.TITLE.setText(_translate("step_2", "Bandaging a Wound"))
        self.TITLE_2.setText(_translate("step_2", "Step 2: Cover the Bandage"))
        self.label.setText(_translate("step_2", " A) Wrap roller gauze or cloth strips over the dressing and around the wound several times.\n"
"\n"
" B) Extend the bandage at least an inch beyond both sides of the dressing.\n"
"\n"
" C) Don\'t wrap the bandage so tight that it interferes with blood flow to healthy tissue."))
        self.pushButton.setText(_translate("step_2", "Next Step"))
        self.pushButton_3.setText(_translate("step_2", "Go back"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    step_2 = QtWidgets.QMainWindow()
    ui = Ui_step_2()
    ui.setupUi(step_2)
    step_2.show()
    sys.exit(app.exec_())

