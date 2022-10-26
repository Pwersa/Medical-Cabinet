import sys, cv2, time
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi

class Ui_scan_qr_code(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_code, self).__init__()
        loadUi("scan_qr_code.ui", self)
        self.scan_button.clicked.connect(self.qr_camera)
    
    def qr_camera(self):
        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        while True:
            _, img = cap.read()
            data, bbox, _ = detector.detectAndDecode(img)
    
            if(bbox is not None):
                for i in range(len(bbox)):
                    cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
                    cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)
    
            if data:
                print("data found: ", data)
            cv2.imshow("Scan QR CODE", img)

            if data == 'TUPC-19-0155 DURAN, ROGIE BET-COET-4A 1234':
                time.sleep(2)
                break
            
            if (cv2.waitKey(1) == ord("q")):
                break

        cap.release()
        cv2.destroyAllWindows()
        #window.setCurrentIndex(window.currentIndex()-1)
        window.setCurrentIndex(window.currentIndex()+1)
      
class Ui_select_body_part(QMainWindow):
    def __init__(self):
        super(Ui_select_body_part, self).__init__()
        loadUi("select_body_part.ui", self)
        self.hand_button.clicked.connect(self.open_close_window)
        #window.setWindowTitle("asdasdasdasdasdasd")
        
    def open_close_window(self):
        window.setCurrentIndex(window.currentIndex()+1)
        
class Ui_select_injury_type(QMainWindow):
    def __init__(self):
        super(Ui_select_injury_type, self).__init__()
        loadUi("select_injury_type.ui", self)
        self.go_back_button.clicked.connect(self.go_back)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)  



app = QApplication(sys.argv)
window = QtWidgets.QStackedWidget()


############################ ADD CLASS HERE ######################
main_window = Ui_scan_qr_code()
window_select_body_part = Ui_select_body_part()
window_select_injury_type = Ui_select_injury_type()

window.addWidget(main_window)
window.addWidget(window_select_body_part)
window.addWidget(window_select_injury_type)

####################### PARAMETERS FOR THE WINDOW ################
window.setMaximumHeight(600)
window.setMinimumHeight(600)
window.setMinimumWidth(1024)
window.setMaximumWidth(1024)
window.setWindowTitle("Interactive First Aid Cabinet - BET COET 4A - Build 2022")

window.show()
sys.exit(app.exec_())