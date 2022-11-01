# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'step_1_gif.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_step_1_window(object):
    def setupUi(self, step_1_window):
        step_1_window.setObjectName("step_1_window")
        step_1_window.resize(1024, 600)
        step_1_window.setMinimumSize(QtCore.QSize(1024, 600))
        step_1_window.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(step_1_window)
        self.centralwidget.setObjectName("centralwidget")
        self.title_step = QtWidgets.QLabel(self.centralwidget)
        self.title_step.setGeometry(QtCore.QRect(10, 20, 1011, 71))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_step.setFont(font)
        self.title_step.setAlignment(QtCore.Qt.AlignCenter)
        self.title_step.setObjectName("title_step")
        self.text_steps = QtWidgets.QLabel(self.centralwidget)
        self.text_steps.setGeometry(QtCore.QRect(20, 350, 981, 91))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_steps.setFont(font)
        self.text_steps.setObjectName("text_steps")
        self.gif_player_label = QtWidgets.QLabel(self.centralwidget)
        self.gif_player_label.setGeometry(QtCore.QRect(330, 100, 360, 240))
        self.gif_player_label.setMinimumSize(QtCore.QSize(360, 240))
        self.gif_player_label.setMaximumSize(QtCore.QSize(360, 240))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.gif_player_label.setFont(font)
        self.gif_player_label.setLineWidth(1)
        self.gif_player_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gif_player_label.setObjectName("gif_player_label")
        self.next_step_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_step_button.setGeometry(QtCore.QRect(760, 480, 251, 111))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.next_step_button.setFont(font)
        self.next_step_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_step_button.setObjectName("next_step_button")
        self.go_back_injury_type = QtWidgets.QPushButton(self.centralwidget)
        self.go_back_injury_type.setGeometry(QtCore.QRect(10, 470, 251, 121))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.go_back_injury_type.setFont(font)
        self.go_back_injury_type.setObjectName("go_back_injury_type")
        step_1_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(step_1_window)
        QtCore.QMetaObject.connectSlotsByName(step_1_window)

    def retranslateUi(self, step_1_window):
        _translate = QtCore.QCoreApplication.translate
        step_1_window.setWindowTitle(_translate("step_1_window", "Step 1 Procedure"))
        self.title_step.setText(_translate("step_1_window", "<html><head/><body><p><span style=\" font-size:24pt;\">Example Injury Type</span></p></body></html>"))
        self.text_steps.setText(_translate("step_1_window", "<html><head/><body><p align=\"center\">PROCEDURE HERE</p></body></html>"))
        self.gif_player_label.setText(_translate("step_1_window", "GIF PLAYER HERE"))
        self.next_step_button.setText(_translate("step_1_window", "NEXT STEP"))
        self.go_back_injury_type.setText(_translate("step_1_window", "GO BACK TO \n"
" INJURY TYPE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    step_1_window = QtWidgets.QMainWindow()
    ui = Ui_step_1_window()
    ui.setupUi(step_1_window)
    step_1_window.show()
    sys.exit(app.exec_())

