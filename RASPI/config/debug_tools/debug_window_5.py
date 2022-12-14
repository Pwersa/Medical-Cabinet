# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debug_window_5.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 600))
        MainWindow.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.yes_button = QtWidgets.QPushButton(self.centralwidget)
        self.yes_button.setGeometry(QtCore.QRect(640, 360, 271, 141))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.yes_button.setFont(font)
        self.yes_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.yes_button.setStyleSheet("QPushButton:hover:!pressed\n"
"{\n"
"  background-color: rgb(195,30,60);\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"  background-color: white;\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 3px;\n"
"border-radius:10px;\n"
"border-color: black;\n"
"}\n"
"")
        self.yes_button.setObjectName("yes_button")
        self.no_button = QtWidgets.QPushButton(self.centralwidget)
        self.no_button.setGeometry(QtCore.QRect(110, 360, 271, 141))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.no_button.setFont(font)
        self.no_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.no_button.setStyleSheet("QPushButton:hover:!pressed\n"
"{\n"
"  background-color: rgb(195,30,60);\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"  background-color: white;\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 3px;\n"
"border-radius:10px;\n"
"border-color: black;\n"
"}\n"
"")
        self.no_button.setObjectName("no_button")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 1001, 101))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.name_whitelist = QtWidgets.QLabel(self.centralwidget)
        self.name_whitelist.setGeometry(QtCore.QRect(10, 150, 1001, 121))
        font = QtGui.QFont()
        font.setPointSize(48)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.name_whitelist.setFont(font)
        self.name_whitelist.setObjectName("name_whitelist")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Interactive First Aid Cabinet"))
        self.yes_button.setText(_translate("MainWindow", "Yes"))
        self.no_button.setText(_translate("MainWindow", "No"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">ARE YOU SURE YOU WANT TO ADD?</p></body></html>"))
        self.name_whitelist.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
