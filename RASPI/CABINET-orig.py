import sys, cv2, datetime, time, re, csv, socket, tqdm, os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from asdasd import *

# DATE AND TIME, RESPONDER NAME, ID, COURSE, PATIENT NAME, ID, COURSE, GENDER, INJURY TYPE
session = []
gender_types = ["Male", "Female", "N/A"]

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


            cv2.imshow("Scan QR CODE", img)
            

            if data:
                dt = datetime.datetime.now()
 
                # Format datetime string
                x = dt.strftime("%Y-%m-%d %H:%M:%S")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(data)
                fullname = str(parsed_text[1]+" "+ parsed_text[2])
                #print(parsed_text)
                # 1st QR CODE RESPONDER of COET
                session.append(str(x))
                # ID
                session.append(parsed_text[0])
                # NAME
                session.append(fullname)
                # COURSE
                session.append(parsed_text[-2])
                # CHECK IF ADDED DATA IN LIST IS CORRECT
                print("QR DATA")
                print(session)
                
                time.sleep(0.5)
                break
                       
            if (cv2.waitKey(1) == ord("r")):
                time.sleep(0.5)
                break

        cap.release()
        cv2.destroyAllWindows()
        window.setCurrentIndex(1)

class Ui_scan_qr_patient(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_patient, self).__init__()
        loadUi("scan_qr_code_again.ui", self)
        self.scan_qr_patient.clicked.connect(self.qr_camera)

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
            

            if data:
                dt = datetime.datetime.now()
 
                # Format datetime string
                x = dt.strftime("%Y-%m-%d %H:%M:%S")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(data)
                fullname = str(parsed_text[1]+" "+ parsed_text[2])
                #print(parsed_text)
                # 1st QR CODE RESPONDER of COET
                session.append(str(x))
                # ID
                session.append(parsed_text[0])
                # NAME
                session.append(fullname)
                # COURSE
                session.append(parsed_text[-2])
                # CHECK IF ADDED DATA IN LIST IS CORRECT
                print("QR DATA")
                print(session)
                
                time.sleep(0.5)
                break
                       
            if (cv2.waitKey(1) == ord("p")):
                time.sleep(0.5)
                break

        cap.release()
        cv2.destroyAllWindows()
        window.setCurrentIndex(11)
        
    def send_to_companion(self):
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # the ip address or hostname of the server, the receiver
        host = "26.98.239.158"
        # the port, let's use 5001
        port = 4899
        # the name of file we want to send, make sure it exists
        filename = "recorded_session.csv"
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

# OPEN select_body_part.ui file
class Ui_select_body_part(QMainWindow):
    def __init__(self):
        super(Ui_select_body_part, self).__init__()
        loadUi("select_body_part.ui", self)
        self.hand_button.clicked.connect(self.open_close_window)
        #window.setWindowTitle("TEST")
        
    def open_close_window(self):
        print("Selected Body Part: " + str(self.hand_button.text()))
        window.setCurrentIndex(2)

# OPEN select_injury_type.ui file        
class Ui_select_injury_type(QMainWindow):
    def __init__(self):
        super(Ui_select_injury_type, self).__init__()
        loadUi("select_injury_type.ui", self)
        self.others_button.clicked.connect(self.others)
        self.go_back_button.clicked.connect(self.go_back)
        self.cut_button.clicked.connect(self.cut_procedure)

    # OPEN CUT PROCEDURE
    def cut_procedure(self):
        session.append(str(self.cut_button.text()))
        window.setCurrentIndex(5)

    def others(self):
        window.setCurrentIndex(3)

    ## GO BACK TO THE LAST WINDOW
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)  

class Ui_enter_injury(QMainWindow):
    def __init__(self):
        super(Ui_enter_injury, self).__init__()
        loadUi("enter_injury.ui", self)
        self.enter_button.clicked.connect(self.enter_injury)
        self.enter_injury_go_back_button.clicked.connect(self.go_back)

    def enter_injury(self):
        window.setCurrentIndex(4)

    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)  

class Ui_request_nurse(QMainWindow):
    def __init__(self):
        super(Ui_request_nurse, self).__init__()
        loadUi("request_nurse.ui", self)
        self.end_procedure_button.clicked.connect(self.reset_program)

    def reset_program(self):
        window.setCurrentIndex(0)

class Ui_step_1(QMainWindow):
    def __init__(self):
        super(Ui_step_1, self).__init__()
        loadUi("step_1.ui", self)
        self.go_back_injury_type.clicked.connect(self.go_back)
        self.next_step_button.clicked.connect(self.next_procedure)

    def next_procedure(self):
        window.setCurrentIndex(6) 

    def go_back(self):
        window.setCurrentIndex(2) 

class Ui_step_2(QMainWindow):
    def __init__(self):
        super(Ui_step_2, self).__init__()
        loadUi("step_2.ui", self)
        self.go_back_procedure.clicked.connect(self.go_back)
        self.next_step_button.clicked.connect(self.next_procedure)

    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1) 

    def next_procedure(self):
        window.setCurrentIndex(7) 

class Ui_step_3(QMainWindow):
    def __init__(self):
        super(Ui_step_3, self).__init__()
        loadUi("step_3.ui", self)
        self.go_back_procedure.clicked.connect(self.go_back)
        self.finish_procedure.clicked.connect(self.finish_steps)

    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
    
    def finish_steps(self):
        window.setCurrentIndex(8)

class Ui_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_confirmation, self).__init__()
        loadUi("confirmation.ui", self)
        self.no_button.clicked.connect(self.no_confirmation)
        self.yes_button.clicked.connect(self.yes_confirmation)

    def no_confirmation(self):
        window.setCurrentIndex(5)

    def yes_confirmation(self):
        window.setCurrentIndex(9)

class Ui_confirmation_again(QMainWindow):
    def __init__(self):
        super(Ui_confirmation_again, self).__init__()
        loadUi("confirmation_again.ui", self)
        self.new_injury_button.clicked.connect(self.new_injury)
        self.finish_procedure.clicked.connect(self.done_procedure)

    def new_injury(self):
        window.setCurrentIndex(1)
    
    # GOING TO SCAN QR CODE AGAIN BUT FOR THE PATIENT
    def done_procedure(self):
        window.setCurrentIndex(10)
        
class Ui_gender_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_gender_patient_window, self).__init__()
        loadUi("patient_gender.ui", self)
        self.male_button.clicked.connect(lambda: self.gender_submit(gender_types[0]))
        self.female_button.clicked.connect(lambda: self.gender_submit(gender_types[1]))
        self.not_say_button.clicked.connect(lambda: self.gender_submit(gender_types[2]))
            
    def gender_submit(self, gender_types):
        if gender_types == "Male":
            session.append("MALE")
            window.setCurrentIndex(12)
        
        elif gender_types == "Female":
            session.append("FEMALE")
            window.setCurrentIndex(12)
            
        elif gender_types == "N/A":
            session.append("Not Said")
            window.setCurrentIndex(12)

class Ui_session_record(QMainWindow):
    def __init__(self):
        super(Ui_session_record, self).__init__()
        loadUi("record_session.ui", self)
        self.fiinish_session.clicked.connect(self.end_session)

    def end_session(self):
        print(session)
        session.clear()
        window.setCurrentIndex(0)

app = QApplication(sys.argv)
window = QtWidgets.QStackedWidget()

############################ ADD CLASS HERE ############################

main_window = Ui_scan_qr_code() 
window_select_body_part = Ui_select_body_part()
window_select_injury_type = Ui_select_injury_type()
window_enter_injury = Ui_enter_injury()
window_request_nurse = Ui_request_nurse()
window_step_1 = Ui_step_1()
window_step_2 = Ui_step_2()
window_step_3 = Ui_step_3()
window_confirmation = Ui_confirmation()
window_confirmation_again = Ui_confirmation_again()
window_qr_patient = Ui_scan_qr_patient()
window_patient_gender = Ui_gender_patient_window()
window_session_record = Ui_session_record()

window.addWidget(main_window) # INDEX 0
window.addWidget(window_select_body_part) # INDEX 1
window.addWidget(window_select_injury_type) # INDEX 2
window.addWidget(window_enter_injury)  # INDEX 3
window.addWidget(window_request_nurse)  # INDEX 4
window.addWidget(window_step_1) # INDEX 5
window.addWidget(window_step_2) # INDEX 6
window.addWidget(window_step_3) # INDEX 7
window.addWidget(window_confirmation) # INDEX 8
window.addWidget(window_confirmation_again) # INDEX 9
window.addWidget(window_qr_patient) # INDEX 10
window.addWidget(window_patient_gender) # INDEX 11
window.addWidget(window_session_record) # INDEX 12

####################### PARAMETERS FOR THE WINDOW (EXACT FOR THE TOUCH SCREEN) #######################

window.setMaximumHeight(600)
window.setMaximumWidth(1024)
window.setWindowTitle("Interactive First Aid Cabinet - BET COET 4A - Build 2022")

window.show()
sys.exit(app.exec_())