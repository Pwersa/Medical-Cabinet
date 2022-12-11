# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keyboard.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
alphabet = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "-", "Backspace"], 
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', "Spacebar"]]

input_text = []

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(320, 160, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setStrikeOut(True)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        
        #alphabet = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "-"], 
            #['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            #['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            #['Z', 'X', 'C', 'V', 'B', 'N', 'M', "Backspace"]]
            
        #self.cut_button.clicked.connect(lambda: self.injuries(injury_type_selection[0]))
        
        self.a_letter = QtWidgets.QPushButton(self.centralwidget, clicked = (lambda: self.keyboard(alphabet[1][0])))
        self.a_letter.setGeometry(QtCore.QRect(290, 310, 71, 61))
        self.a_letter.setObjectName("a_letter")
        self.b_letter = QtWidgets.QPushButton(self.centralwidget, clicked = (lambda: self.keyboard(alphabet[1][1])))
        self.b_letter.setGeometry(QtCore.QRect(370, 310, 71, 61))
        self.b_letter.setObjectName("b_letter")
        self.c_letter = QtWidgets.QPushButton(self.centralwidget, clicked = (lambda: self.keyboard(alphabet[0][11])))
        self.c_letter.setGeometry(QtCore.QRect(450, 310, 71, 61))
        self.c_letter.setObjectName("c_letter")
        self.d_letter = QtWidgets.QPushButton(self.centralwidget, clicked = self.check_pos)
        self.d_letter.setGeometry(QtCore.QRect(530, 310, 71, 61))
        self.d_letter.setObjectName("d_letter")
        self.e_letter = QtWidgets.QPushButton(self.centralwidget)
        self.e_letter.setGeometry(QtCore.QRect(610, 310, 71, 61))
        self.e_letter.setObjectName("e_letter")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def keyboard(self, alphabet):
        if alphabet == "Q":
            
            print("CURSOR POSITION")
            print(self.lineEdit.cursorPosition())
            check = self.lineEdit.cursorPosition()
            print("Q")
            
            input_text.append(alphabet)
            new_string = "".join(input_text)
            print(new_string)
    
            self.lineEdit.setText(new_string)
            
        elif alphabet == "W":
            check = self.lineEdit.cursorPosition()

            if self.lineEdit.cursorPosition() == self.lineEdit.cursorPosition():
                #subtract = check - 1
                input_text.insert(check, alphabet)
                new_string = "".join(input_text)
                print("ASDASD" + new_string)

                self.lineEdit.setText(new_string)
                self.lineEdit.setCursorPosition(check + 1 )

            else:
                pass
            
        elif alphabet == "Backspace":
            print("Backspace")
            #self.lineEdit.setText(alphabet)
            check = self.lineEdit.cursorPosition()
            subtract = check - 1
            
            print("CHECK IF LIST IS EMPTY")
            if len(input_text) >= 1:
                input_text.pop(subtract)
                new_string = "".join(input_text)
                print(new_string)
                print(self.lineEdit.cursorPosition())
                self.lineEdit.setText(new_string)
                self.lineEdit.setCursorPosition(subtract)
                self.lineEdit.hasFocus()

            else:
                print("NO MORE ITEMS")
            
        else:
            print("NOT WORKING")
            print(alphabet[0][0])
            #input_text.pop(subtract)
            
    def check_list(self, subtract):
        if len(input_text) == 0:
            print("NO MORE ITEMS")
            
        else:
            input_text.pop(subtract)
            
    def check_pos(self):
        check = self.lineEdit.cursorPosition() - 1
        print(self.lineEdit.cursorPosition())
        print(check)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.a_letter.setText(_translate("MainWindow", "A"))
        self.b_letter.setText(_translate("MainWindow", "B"))
        self.c_letter.setText(_translate("MainWindow", "C"))
        self.d_letter.setText(_translate("MainWindow", "D"))
        self.e_letter.setText(_translate("MainWindow", "E"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())