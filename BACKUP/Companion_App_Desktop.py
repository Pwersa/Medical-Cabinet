# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Companion_App.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CompanionApp(object):
    def setupUi(self, CompanionApp):
        CompanionApp.setObjectName("CompanionApp")
        CompanionApp.resize(1130, 1059)
        self.widget = QtWidgets.QWidget(CompanionApp)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frameTitle = QtWidgets.QFrame(self.widget)
        self.frameTitle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTitle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTitle.setObjectName("frameTitle")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.frameTitle)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.Title = QtWidgets.QLabel(self.frameTitle)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.gridLayout_8.addWidget(self.Title, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frameTitle, 0, 0, 1, 1)
        self.framesSecond = QtWidgets.QFrame(self.widget)
        self.framesSecond.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.framesSecond.setFrameShadow(QtWidgets.QFrame.Raised)
        self.framesSecond.setObjectName("framesSecond")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.framesSecond)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label = QtWidgets.QLabel(self.framesSecond)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1)
        self.frameTable = QtWidgets.QFrame(self.framesSecond)
        self.frameTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTable.setObjectName("frameTable")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frameTable)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frameTableList = QtWidgets.QFrame(self.frameTable)
        self.frameTableList.setMaximumSize(QtCore.QSize(700, 16777215))
        self.frameTableList.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameTableList.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameTableList.setObjectName("frameTableList")
        self.gridLayout = QtWidgets.QGridLayout(self.frameTableList)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(self.frameTableList)
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.frameTableList)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 45))
        self.pushButton.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frameTableList)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 45))
        self.pushButton_2.setMaximumSize(QtCore.QSize(16777215, 45))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.gridLayout_5.addWidget(self.frameTableList, 1, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.frameTable)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableTitle_1 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.tableTitle_1.setFont(font)
        self.tableTitle_1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.tableTitle_1.setObjectName("tableTitle_1")
        self.gridLayout_3.addWidget(self.tableTitle_1, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_3, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.frameTable, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.framesSecond, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setMinimumSize(QtCore.QSize(110, 110))
        self.label_7.setMaximumSize(QtCore.QSize(110, 110))
        self.label_7.setText("")
        self.label_7.setPixmap(QtGui.QPixmap("110x110 TUP LOGO.png"))
        self.label_7.setObjectName("label_7")
        self.gridLayout_9.addWidget(self.label_7, 0, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setMinimumSize(QtCore.QSize(110, 110))
        self.label_5.setMaximumSize(QtCore.QSize(110, 110))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("110x110 CROSS.png"))
        self.label_5.setObjectName("label_5")
        self.gridLayout_9.addWidget(self.label_5, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setMinimumSize(QtCore.QSize(86, 110))
        self.label_6.setMaximumSize(QtCore.QSize(86, 110))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("86x110 raspie.png"))
        self.label_6.setObjectName("label_6")
        self.gridLayout_9.addWidget(self.label_6, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 3, 0, 1, 1)
        CompanionApp.setCentralWidget(self.widget)

        self.retranslateUi(CompanionApp)
        QtCore.QMetaObject.connectSlotsByName(CompanionApp)

    def retranslateUi(self, CompanionApp):
        _translate = QtCore.QCoreApplication.translate
        CompanionApp.setWindowTitle(_translate("CompanionApp", "Interactive First Aid Cabinet - Companion App for Desktop"))
        self.Title.setText(_translate("CompanionApp", "Interactive First Aid Cabinet"))
        self.label.setText(_translate("CompanionApp", "The Companion App"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("CompanionApp", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("CompanionApp", "ID Number"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("CompanionApp", "Date"))
        self.pushButton.setText(_translate("CompanionApp", "Export"))
        self.pushButton_2.setText(_translate("CompanionApp", "Refresh"))
        self.tableTitle_1.setText(_translate("CompanionApp", "Accessed Users"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CompanionApp = QtWidgets.QMainWindow()
    ui = Ui_CompanionApp()
    ui.setupUi(CompanionApp)
    CompanionApp.show()
    sys.exit(app.exec_())
