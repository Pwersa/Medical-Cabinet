# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cabinet_opened_notif.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep

class Ui_cabinet_notif(object):
    def setupUi(self, cabinet_notif):
        self.cabinet_notif_window = cabinet_notif
        cabinet_notif.setObjectName("cabinet_notif")
        cabinet_notif.resize(800, 600)
        cabinet_notif.setMinimumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(cabinet_notif)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.label.setMinimumSize(QtCore.QSize(1024, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pictures/program_pictures/main_wallpaper.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 741, 231))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(72)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.close_window)
        self.pushButton.setGeometry(QtCore.QRect(250, 420, 301, 141))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton:hover:!pressed\n"
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
                                        "}")
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 320, 581, 61))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        cabinet_notif.setCentralWidget(self.centralwidget)

        self.retranslateUi(cabinet_notif)
        QtCore.QMetaObject.connectSlotsByName(cabinet_notif)
        
        #self.auto_close()

    def retranslateUi(self, cabinet_notif):
        _translate = QtCore.QCoreApplication.translate
        cabinet_notif.setWindowTitle(_translate("cabinet_notif", "CABINET IS OPENED!"))
        self.label_2.setText(_translate("cabinet_notif", "<html><head/><body><p align=\"center\">CABINET IS</p><p align=\"center\">NOW <span style=\" text-decoration: underline; color:#00aa7f;\">OPEN!</span></p></body></html>"))
        self.pushButton.setText(_translate("cabinet_notif", "DISMISS"))
        self.label_3.setText(_translate("cabinet_notif", "<html><head/><body><p align=\"center\"></p></body></html>"))
        
        

    def auto_close(self):
       print("ASDASD")
   
    def close_window(self):
        self.cabinet_notif_window.close()
        
    def open_window(self):
        self.cabinet_notif_window.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    cabinet_notif = QtWidgets.QMainWindow()
    ui = Ui_cabinet_notif()
    ui.setupUi(cabinet_notif)
    cabinet_notif.show()
    sys.exit(app.exec_())
