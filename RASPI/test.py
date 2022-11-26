from PyQt5.QtWidgets import *

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    f = QFrame()
    f.setLayout(QVBoxLayout())
    for i in range(4):
        r = QRadioButton("opt{}".format(i), f)
        r.setStyleSheet('QRadioButton{font: 30pt Helvetica MS;} QRadioButton::indicator { width: 30px; height: 30px;};')
        f.layout().addWidget(r)
    f.show()
    sys.exit(app.exec_())
    