# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan_qr_code.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2, datetime, time, re, csv, socket, tqdm, os
from Select_Body_Part import Ui_select_body_part

class Ui_scan_qr_code(object):

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


            cv2.imshow("Scan QR CODE", img)

            key="TUPC"
            key_index = data.find(key)
            lkey=int(4)

            if data:
                if key_index < 0:
                    error_text = "NOT A VALID ID from TUPC"
                    for i in range(len(bbox)):
                        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
                        cv2.putText(img, error_text, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)

                else:
                    identifier= data[key_index:key_index+lkey]
                    asdasd = datetime.datetime.now()
                    print(asdasd)

                    regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                    parsed_text = regexp.findall(data)
                    fullname = str(parsed_text[1]+" "+ parsed_text[2])

                    print("student id is: " + parsed_text[0])
                    print("full name is: " + fullname)

                    data_qr = []
                    data_qr.append(str(parsed_text[0]))
                    data_qr.append(str(parsed_text[1]+ " " + parsed_text[2]))
                    data_qr.append(str(parsed_text[3]+ " " + parsed_text[4]))
                    data_qr.append(datetime.datetime.now())

                    with open('student_id.csv', 'w', encoding='UTF8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(data_qr)
                        
                    time.sleep(2)
                    
                    self.send_to_companion()
                    break
            
            if (cv2.waitKey(1) == ord("q")):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.select_body_part_window()
    
    def select_body_part_window(self):
        self.window_select_body_parts = QtWidgets.QMainWindow()
        self.ui = Ui_select_body_part()
        self.ui.setupUi(self.window_select_body_parts)
        self.window_select_body_parts.show()
    
    def send_to_companion(self):

        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # the ip address or hostname of the server, the receiver
        host = "192.168.254.104"
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = "student_id.csv"
        # get the file size
        filesize = os.path.getsize(filename)

        # create the client socket
        s = socket.socket()

        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")

        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break

                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
            
                # update the progress bar
                progress.update(len(bytes_read))

        # close the socket
        s.close()

    def setupUi(self, scan_qr_code):
        scan_qr_code.setObjectName("scan_qr_code")
        scan_qr_code.resize(1024, 600)
        scan_qr_code.setMinimumSize(QtCore.QSize(0, 0))
        scan_qr_code.setMaximumSize(QtCore.QSize(1024, 600))
        self.centralwidget = QtWidgets.QWidget(scan_qr_code)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 9, 1011, 171))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TITLE = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.TITLE.setFont(font)
        self.TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.TITLE.setObjectName("TITLE")
        self.gridLayout_2.addWidget(self.TITLE, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(9, 348, 1001, 241))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.TUPC = QtWidgets.QLabel(self.frame_2)
        self.TUPC.setMinimumSize(QtCore.QSize(192, 192))
        self.TUPC.setMaximumSize(QtCore.QSize(192, 192))
        self.TUPC.setText("")
        self.TUPC.setPixmap(QtGui.QPixmap("../tuplogo (1).png"))
        self.TUPC.setObjectName("TUPC")
        self.gridLayout.addWidget(self.TUPC, 0, 0, 1, 1)
        self.TUPC_2 = QtWidgets.QLabel(self.frame_2)
        self.TUPC_2.setMinimumSize(QtCore.QSize(194, 194))
        self.TUPC_2.setMaximumSize(QtCore.QSize(194, 194))
        self.TUPC_2.setText("")
        self.TUPC_2.setPixmap(QtGui.QPixmap("../first-aid-logo-png-png-image-762531.png"))
        self.TUPC_2.setObjectName("TUPC_2")
        self.gridLayout.addWidget(self.TUPC_2, 0, 1, 1, 1)
        self.rasberry = QtWidgets.QLabel(self.frame_2)
        self.rasberry.setMinimumSize(QtCore.QSize(156, 200))
        self.rasberry.setMaximumSize(QtCore.QSize(156, 200))
        self.rasberry.setText("")
        self.rasberry.setPixmap(QtGui.QPixmap("../Raspberry logo.png"))
        self.rasberry.setObjectName("rasberry")
        self.gridLayout.addWidget(self.rasberry, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget, clicked = self.qr_camera)
        self.pushButton.setGeometry(QtCore.QRect(331, 187, 351, 151))
        font = QtGui.QFont()
        font.setFamily("Unispace")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        scan_qr_code.setCentralWidget(self.centralwidget)

        self.retranslateUi(scan_qr_code)
        QtCore.QMetaObject.connectSlotsByName(scan_qr_code)

    def retranslateUi(self, scan_qr_code):
        _translate = QtCore.QCoreApplication.translate
        scan_qr_code.setWindowTitle(_translate("scan_qr_code", "Interactive First Aid Cabinet"))
        self.TITLE.setText(_translate("scan_qr_code", "Scan QR Code to Continue"))
        self.pushButton.setText(_translate("scan_qr_code", "SCAN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    scan_qr_code = QtWidgets.QMainWindow()
    ui = Ui_scan_qr_code()
    ui.setupUi(scan_qr_code)
    scan_qr_code.show()
    sys.exit(app.exec_())