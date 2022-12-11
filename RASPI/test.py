import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, \
                            QGridLayout, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        app.focusChanged.connect(self.on_focusChaned)

        self.lineEditFocused = None
        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()

        self.layout.addWidget(self.lineEdit1, 0, 0, 1, 1)
        self.layout.addWidget(self.lineEdit2, 0, 1, 1, 1)
        self.layout.addWidget(self.lineEdit3, 0, 2, 1, 1)

        self.button = QPushButton('set')
        self.button.clicked.connect(self.setFocusText)
        self.layout.addWidget(self.button, 1, 0, 1, 1)

    def setFocusText(self):
        self.lineEditFocused.setText('My Text')

    def on_focusChaned(self, widget):
        # print(widget)
        self.lineEditFocused = widget # <-- This is going to be a QLineEdit object


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 17px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')