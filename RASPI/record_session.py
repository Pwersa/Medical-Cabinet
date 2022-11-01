# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'record_session.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
#from CABINET import *

class Ui_record_session(object):
    def setupUi(self, record_session):
        self.record_session_window = record_session
        record_session.setObjectName("record_session")
        record_session.resize(1024, 600)
        record_session.setMinimumSize(QtCore.QSize(1024, 600))
        record_session.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(record_session)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 0, 1021, 71))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(24)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.label_responder = QtWidgets.QLabel(self.centralwidget)
        self.label_responder.setGeometry(QtCore.QRect(110, 131, 141, 41))
        self.label_responder.setObjectName("label_responder")
        self.qr_responder_name = QtWidgets.QLabel(self.centralwidget)
        self.qr_responder_name.setGeometry(QtCore.QRect(229, 105, 791, 81))
        self.qr_responder_name.setObjectName("qr_responder_name")
        self.label_responder_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_responder_3.setGeometry(QtCore.QRect(110, 201, 141, 41))
        self.label_responder_3.setObjectName("label_responder_3")
        self.qr_patient_name = QtWidgets.QLabel(self.centralwidget)
        self.qr_patient_name.setGeometry(QtCore.QRect(225, 175, 801, 81))
        self.qr_patient_name.setObjectName("qr_patient_name")
        self.label_responder_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_responder_5.setGeometry(QtCore.QRect(60, 301, 141, 41))
        self.label_responder_5.setObjectName("label_responder_5")
        self.date_session = QtWidgets.QLabel(self.centralwidget)
        self.date_session.setGeometry(QtCore.QRect(102, 342, 331, 41))
        self.date_session.setObjectName("date_session")
        self.label_responder_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_responder_6.setGeometry(QtCore.QRect(510, 301, 141, 41))
        self.label_responder_6.setObjectName("label_responder_6")
        self.label_responder_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_responder_8.setGeometry(QtCore.QRect(510, 350, 141, 41))
        self.label_responder_8.setObjectName("label_responder_8")
        self.body_injured = QtWidgets.QLabel(self.centralwidget)
        self.body_injured.setGeometry(QtCore.QRect(700, 301, 261, 41))
        self.body_injured.setObjectName("body_injured")
        self.type_of_injury = QtWidgets.QLabel(self.centralwidget)
        self.type_of_injury.setGeometry(QtCore.QRect(699, 350, 261, 41))
        self.type_of_injury.setObjectName("type_of_injury")
        self.fiinish_session = QtWidgets.QPushButton(self.centralwidget, clicked = self.close_window)
        self.fiinish_session.setGeometry(QtCore.QRect(355, 430, 311, 151))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.fiinish_session.setFont(font)
        self.fiinish_session.setObjectName("fiinish_session")
        record_session.setCentralWidget(self.centralwidget)

        self.retranslateUi(record_session)
        QtCore.QMetaObject.connectSlotsByName(record_session)

    def retranslateUi(self, record_session):
        _translate = QtCore.QCoreApplication.translate
        record_session.setWindowTitle(_translate("record_session", "MainWindow"))
        self.TITLE.setText(_translate("record_session", "Session Record"))
        self.label_responder.setText(_translate("record_session", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">QR Responder: </span></p></body></html>"))
        self.label_responder_3.setText(_translate("record_session", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">QR Patient: </span></p></body></html>"))
        self.label_responder_5.setText(_translate("record_session", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Date and Time:</span></p></body></html>"))
        self.label_responder_6.setText(_translate("record_session", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Body Injured:</span></p></body></html>"))
        self.label_responder_8.setText(_translate("record_session", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:600;\">Type of injury:</span></p></body></html>"))
        self.fiinish_session.setText(_translate("record_session", "CONFIRM"))

    def close_window(self):
        self.record_session_window.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    record_session = QtWidgets.QMainWindow()
    ui = Ui_record_session()
    ui.setupUi(record_session)
    record_session.show()
    sys.exit(app.exec_())

