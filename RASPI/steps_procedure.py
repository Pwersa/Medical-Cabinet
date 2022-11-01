from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie

traverse = []

class Ui_procedure_window(object):
    def setupUi(self, procedure_window):
        self.procedure_window_window = procedure_window
        procedure_window.setObjectName("procedure_window")
        procedure_window.resize(1024, 600)
        procedure_window.setMinimumSize(QtCore.QSize(1024, 600))
        procedure_window.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(procedure_window)
        self.centralwidget.setObjectName("centralwidget")
        self.title_step = QtWidgets.QLabel(self.centralwidget)
        self.title_step.setGeometry(QtCore.QRect(10, 0, 1011, 71))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.title_step.setFont(font)
        self.title_step.setAlignment(QtCore.Qt.AlignCenter)
        self.title_step.setObjectName("title_step")
        self.text_steps = QtWidgets.QLabel(self.centralwidget)
        self.text_steps.setGeometry(QtCore.QRect(20, 330, 981, 91))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.text_steps.setFont(font)
        self.text_steps.setObjectName("text_steps")
        self.gif_player_label = QtWidgets.QLabel(self.centralwidget)
        self.gif_player_label.setGeometry(QtCore.QRect(330, 80, 360, 240))
        self.gif_player_label.setMinimumSize(QtCore.QSize(360, 240))
        self.gif_player_label.setMaximumSize(QtCore.QSize(360, 240))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.gif_player_label.setFont(font)
        self.gif_player_label.setLineWidth(1)
        self.gif_player_label.setText("")
        self.gif_player_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gif_player_label.setObjectName("gif_player_label")
        self.next_step_button = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.next_procedure_2(traverse[0]))
        self.next_step_button.setGeometry(QtCore.QRect(760, 470, 251, 121))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.next_step_button.setFont(font)
        self.next_step_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.next_step_button.setObjectName("next_step_button")
        #self.go_back_injury_type = QtWidgets.QPushButton(self.centralwidget, clicked = self.setcurrent)
        self.go_back_injury_type.setGeometry(QtCore.QRect(10, 470, 251, 121))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.go_back_injury_type.setFont(font)
        self.go_back_injury_type.setObjectName("go_back_injury_type")
        self.injury_type_label = QtWidgets.QLabel(self.centralwidget)
        self.injury_type_label.setGeometry(QtCore.QRect(268, 500, 481, 71))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.injury_type_label.setFont(font)
        self.injury_type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.injury_type_label.setObjectName("injury_type_label")
        procedure_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(procedure_window)
        QtCore.QMetaObject.connectSlotsByName(procedure_window)
        
        self.doc = QtGui.QTextDocument()
        self.doc.setHtml(self.injury_type_label.text())
        self.text_injury = self.doc.toPlainText()
    
    def next_procedure(self, injury_type_selection):
        print(injury_type_selection)
        traverse.append(injury_type_selection)
        print(traverse[0])
        if injury_type_selection == "Cut":
            self.title_step.setText("STEP 1: Stop The Bleeding")
            self.text_steps.setText("Apply pressure with a clean bandage or cloth, and keep that part of your body elevated above the heart, if possible")
            self.cut_gif = QMovie("GIFs/cuts-1.gif")
            self.gif_player_label.setMovie(self.cut_gif)
            self.cut_gif.start()

        elif self.text_injury == "Wound":
            pass
        
        elif self.text_injury == "Burn":
            pass
        
        elif self.text_injury == "Puncture":
            pass
    
    def next_procedure_2(self, traverse):
        print("TEST")
        if traverse == "Cut":
            print("TEST1")
            self.title_step.setText("STEP 2: Clean the wound")
            self.text_steps.setText("Rinse the wound with water. Keeping the wound under running tap water will reduce the risk of infection. If water is not available, use betadine solution to clean the wound.")
            self.next_step_button.setText("")
            
            self.cut_gif = QMovie("GIFs/cuts-2.gif")
            self.gif_player_label.setMovie(self.cut_gif)
            self.cut_gif.start()
        
        elif traverse[0] == "Wound":
            pass
        
        elif traverse[0] == "Burn":
            pass
        
        elif traverse[0] == "Puncture":
            pass

    def retranslateUi(self, procedure_window):
        _translate = QtCore.QCoreApplication.translate
        procedure_window.setWindowTitle(_translate("procedure_window", "Step 1 Procedure"))
        self.title_step.setText(_translate("procedure_window", "<html><head/><body><p><br/></p></body></html>"))
        self.text_steps.setText(_translate("procedure_window", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.next_step_button.setText(_translate("procedure_window", "NEXT STEP"))
        self.go_back_injury_type.setText(_translate("procedure_window", "GO BACK TO \n"
" BODY PARTS"))
        self.injury_type_label.setText(_translate("procedure_window", "<html><head/><body><p><br/></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    procedure_window = QtWidgets.QMainWindow()
    ui = Ui_procedure_window()
    ui.setupUi(procedure_window)
    procedure_window.show()
    sys.exit(app.exec_())
