# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirmation_again.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_confirmation_again(object):
    def setupUi(self, confirmation_again):
        confirmation_again.setObjectName("confirmation_again")
        confirmation_again.resize(1024, 600)
        confirmation_again.setMinimumSize(QtCore.QSize(1024, 600))
        confirmation_again.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(confirmation_again)
        self.centralwidget.setObjectName("centralwidget")
        self.TITLE = QtWidgets.QLabel(self.centralwidget)
        self.TITLE.setGeometry(QtCore.QRect(0, 40, 1021, 191))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.review_procedure = QtWidgets.QPushButton(self.centralwidget)
        self.review_procedure.setGeometry(QtCore.QRect(120, 350, 331, 181))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.review_procedure.setFont(font)
        self.review_procedure.setObjectName("review_procedure")
        self.injury_again = QtWidgets.QPushButton(self.centralwidget)
        self.injury_again.setGeometry(QtCore.QRect(590, 350, 311, 181))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.injury_again.setFont(font)
        self.injury_again.setObjectName("injury_again")
        confirmation_again.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(confirmation_again)
        self.statusbar.setObjectName("statusbar")
        confirmation_again.setStatusBar(self.statusbar)

        self.retranslateUi(confirmation_again)
        QtCore.QMetaObject.connectSlotsByName(confirmation_again)

    def retranslateUi(self, confirmation_again):
        _translate = QtCore.QCoreApplication.translate
        confirmation_again.setWindowTitle(_translate("confirmation_again", "Confirmation Procedure"))
        self.TITLE.setText(_translate("confirmation_again", "Review procedure \n"
" or\n"
" another inujury again?"))
        self.review_procedure.setText(_translate("confirmation_again", "REVIEW  \n"
" PROCEDURE \n"
" (GOING BACK \n"
" TO STEP 1)"))
        self.injury_again.setText(_translate("confirmation_again", "ANOTHER \n"
" INJURY \n"
" AGAIN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    confirmation_again = QtWidgets.Qconfirmation_again()
    ui = Ui_confirmation_again()
    ui.setupUi(confirmation_again)
    confirmation_again.show()
    sys.exit(app.exec_())

