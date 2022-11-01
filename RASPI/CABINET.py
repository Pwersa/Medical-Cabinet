import sys, cv2, datetime, time, re, csv, socket, tqdm, os
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QMessageBox
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie
from record_session import Ui_record_session
import threading

# DATE AND TIME, RESPONDER ID, NAME, COURSE, PATIENT ID, NAME, COURSE, GENDER, INJURY TYPE
session = []
body_parts_selected = []
injury_types_selected = []

injury_type_selection = ["Cut", "Poison", "Puncture", "Burn", "Others", "Go back to window"]
body_parts_list = ["Hand", "Head", "Face", "Knee"]
gender_types = ["Male", "Female", "N/A"]

# CSV FILE
data_qr = []

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
                # Same situation but for CSV File
                data_qr.append(str(x))
                data_qr.append(parsed_text[0])
                data_qr.append(fullname)
                data_qr.append(parsed_text[-2])

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
                #x = dt.strftime("%Y-%m-%d %H:%M:%S")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(data)
                fullname = str(parsed_text[1]+" "+ parsed_text[2])

                # 1st QR CODE Patient
                #session.append(str(x))
                # ID
                session.append(parsed_text[0])
                # NAME
                session.append(fullname)
                # COURSE
                session.append(parsed_text[-2])
                # CHECK IF ADDED DATA IN LIST IS CORRECT
                
                # Same situation but for CSV File
                data_qr.append(parsed_text[0])
                # NAME
                data_qr.append(fullname)
                # COURSE
                data_qr.append(parsed_text[-2])

                time.sleep(0.5)
                break
                       
            if (cv2.waitKey(1) == ord("p")):
                time.sleep(0.5)
                break

        cap.release()
        cv2.destroyAllWindows()
        window.setCurrentIndex(8)

class Ui_select_body_part(QMainWindow):
    def __init__(self):
        super(Ui_select_body_part, self).__init__()
        loadUi("select_body_part.ui", self)
        self.hand_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[0]))
        
    def body_part_buttons(self, body_parts_list):
        if body_parts_list == "Hand":
            body_parts_selected.append("Hand") 
            #data_qr.append("Hand") # DISABLED IF DEBUG MODE FOR CSV IS ONLINE
            print("Selected Body Part: " + str(self.hand_button.text()))
            window.setCurrentIndex(2)
    
class Ui_select_injury_type(QMainWindow):
    def __init__(self):
        super(Ui_select_injury_type, self).__init__()
        loadUi("select_injury_type.ui", self)
        self.cut_button.clicked.connect(lambda: self.injuries(injury_type_selection[0]))
        self.poison_button.clicked.connect(lambda: self.injuries(injury_type_selection[1]))
        self.puncture_button.clicked.connect(lambda: self.injuries(injury_type_selection[2]))
        self.burn_button.clicked.connect(lambda: self.injuries(injury_type_selection[3]))
        self.others_button.clicked.connect(lambda: self.injuries(injury_type_selection[4]))
        self.go_back_button.clicked.connect(self.go_back)
    
    def injuries(self, injury_type_selection):
        if injury_type_selection == "Cut":
            injury_types_selected.append("CUT") 
            print(injury_types_selected[-1])
            window.setCurrentIndex(9)
            self.debug_csv_send_responder()
            
        elif injury_type_selection == "Poison":
            injury_types_selected.append("POISON") 
            print(injury_types_selected[-1])
            window.setCurrentIndex(22)
            self.debug_csv_send_responder()
        
        elif injury_type_selection == "Puncture":
            injury_types_selected.append("PUNCTURE") 
            print(injury_types_selected[-1])
            window.setCurrentIndex(13)
            self.debug_csv_send_responder()
        
        elif injury_type_selection == "Burn":
            injury_types_selected.append("BURN") 
            print(injury_types_selected[-1])
            window.setCurrentIndex(17)
            self.debug_csv_send_responder()
        
        elif injury_type_selection == "Others":
            window.setCurrentIndex(3)
            
        elif injury_type_selection == "Go back to window":
            window.setCurrentIndex(window.currentIndex()-1)
            
    def go_back(self):
        print(session)
        window.setCurrentIndex(window.currentIndex()-1)
        
    def debug_csv_send_responder(self):
        dt = datetime.datetime.now()
        x = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        data_qr.append(str(x))
        data_qr.append("TUPC-RESPONDER")
        data_qr.append("INDAYA JR")
        data_qr.append("COET")
        data_qr.append("HAND")
        data_qr.append("CUT")
        
        with open('cabinet-history/session/recorded_accessed_responder.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_qr)

        data_qr.clear()

class Ui_enter_injury(QMainWindow):
    def __init__(self):
        super(Ui_enter_injury, self).__init__()
        loadUi("enter_injury.ui", self)
        self.enter_button.clicked.connect(self.enter_injury)
        self.enter_injury_go_back_button.clicked.connect(self.go_back)
        
        self.typed_injury = self.findChild(QTextEdit, "text_edit_injury")

    def enter_injury(self):
        session.append(self.typed_injury)
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

class Ui_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_confirmation, self).__init__()
        loadUi("confirmation.ui", self)
        self.no_button.clicked.connect(self.no_confirmation)
        self.yes_button.clicked.connect(self.yes_confirmation)

    def no_confirmation(self):
        if injury_types_selected[-1] == "CUT":
            print("CUT IS LAST")
            window.setCurrentIndex(9)
            
        elif injury_types_selected[-1] == "POISON":
            print("POISON IS LAST")
            window.setCurrentIndex(22)
            
        elif injury_types_selected[-1] == "PUNCTURE":
            print("PUNCTURE IS LAST")
            window.setCurrentIndex(13)
            
        elif injury_types_selected[-1] == "BURN":
            print("BURN IS LAST")
            window.setCurrentIndex(17)
        
    def yes_confirmation(self):
        window.setCurrentIndex(6)


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
        window.setCurrentIndex(7)
        
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
            #data_qr.append("MALE") # DISABLED IF DEBUG MODE FOR CSV IS ONLINE
            self.record_session_window()
        
        elif gender_types == "Female":
            session.append("FEMALE")
            #data_qr.append("FEMALE") # DISABLED IF DEBUG MODE FOR CSV IS ONLINE
            self.record_session_window()
            
        elif gender_types == "N/A":
            session.append("Not Said")
            #data_qr.append("Not Said") # DISABLED IF DEBUG MODE FOR CSV IS ONLINE
            self.record_session_window()

    def record_session_window(self):
        self.window_record_session = QtWidgets.QMainWindow()
        self.ui = Ui_record_session()
        self.ui.setupUi(self.window_record_session)
        self.window_record_session.show()

        #self.ui.qr_responder_name.setText(session[2] + " - " + session[3])
        #self.ui.qr_patient_name.setText(session[5] + " - " + session[6])
        #self.ui.date_session.setText(session[0])

        #self.ui.body_injured.setText(', ' .join(body_parts_selected))
        #self.ui.type_of_injury.setText(', ' .join(injury_types_selected))
        
        # DEBUG DISPLAY ITEMS
        self.ui.qr_responder_name.setText("INDAYA JR - COET")
        self.ui.qr_patient_name.setText("DURAN ROGIE - BET-COET")
        self.ui.date_session.setText("JANUARY 2022")

        self.ui.body_injured.setText("HAND")
        self.ui.type_of_injury.setText("CUT")

        session.clear()
        body_parts_selected.clear()
        injury_types_selected.clear()
        
        window.setCurrentIndex(0)
        self.save_session_tolocal()

    def save_session_tolocal(self):
        
        # DEBUG MODE (COMMENT IF WANT TO DISABLE)
        # Format datetime string
        dt = datetime.datetime.now()
        x = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        data_qr.append(str(x))
        data_qr.append("TUPC-RESPONDER")
        data_qr.append("INDAYA JR")
        data_qr.append("COET")
        data_qr.append("HAND")
        data_qr.append("CUT")
        data_qr.append("TUPC-PATIENT")
        data_qr.append("DURAN ROGIE")
        data_qr.append("BET COET")        
        data_qr.append("MALE")
        
        with open('cabinet-history/session/recorded_session.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data_qr)

        data_qr.clear()

        # SEND TO COMPANION APP AFTER SAVING LOCALLY
        self.start_threading()
        
    def start_threading(self):
        x = threading.Thread(target=self.send_to_companion)
        x.start()
        print(threading.activeCount())
        
    def send_to_companion(self):
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time stepr

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
        
        
####################### STEPS UI FOR EVERY INJURIES  #######################

######################  CUT PROCEDURES STEPS (4 windows TOTAL)  ###################### 
class Ui_step_1_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_1_cut, self).__init__()
        loadUi("injuries/cut_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("GIFs/cuts-1.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(10)
    
    def go_back(self):
        window.setCurrentIndex(2)
        
class Ui_step_2_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_2_cut, self).__init__()
        loadUi("injuries/cut_step_2.ui", self)
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)

        self.gif_player_label_2 = self.findChild(QLabel, "gif_player_label_2")
   
        self.cut_step2 = QMovie("GIFs/cuts-2.gif")
        self.gif_player_label_2.setMovie(self.cut_step2)
        self.cut_step2.start()
        
    def next_step(self):
        window.setCurrentIndex(11)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 1
        window.setCurrentIndex(window.currentIndex()-1)

class Ui_step_3_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_3_cut, self).__init__()
        loadUi("injuries/cut_step_3.ui", self)
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")
   
        self.cut_step3 = QMovie("GIFs/cuts-2.gif")
        self.gif_player_label_3.setMovie(self.cut_step3)
        self.cut_step3.start()
        
    def next_step(self):
        window.setCurrentIndex(12)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 2
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_4_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_4_cut, self).__init__()
        loadUi("injuries/cut_step_4.ui", self)
        self.next_step_button_4.clicked.connect(self.finish_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        
        self.gif_player_label_4 = self.findChild(QLabel, "gif_player_label_4")
   
        self.cut_step4 = QMovie("GIFs/cuts-2.gif")
        self.gif_player_label_4.setMovie(self.cut_step4)
        self.cut_step4.start()
        
    def finish_step(self):
        window.setCurrentIndex(5)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 2
        window.setCurrentIndex(window.currentIndex()-1)
        


######################  PUNCTURE PROCEDURES STEPS (4 windows TOTAL)  ###################### 

class Ui_step_1_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_1_puncture, self).__init__()
        loadUi("injuries/puncture_before_steps.ui", self)
        
        self.next_step_button_4.clicked.connect(self.next_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)

        #self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
    def next_step(self):
        window.setCurrentIndex(14)
    
    def go_back(self):
        window.setCurrentIndex(2)
        
class Ui_step_2_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_2_puncture, self).__init__()
        loadUi("injuries/puncture_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("GIFs/cuts-1.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(15)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_3_puncture, self).__init__()
        loadUi("injuries/puncture_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)

        self.gif_player_label_2 = self.findChild(QLabel, "gif_player_label_2")
   
        self.cut_step2 = QMovie("GIFs/cuts-2.gif")
        self.gif_player_label_2.setMovie(self.cut_step2)
        self.cut_step2.start()
        
    def next_step(self):
        window.setCurrentIndex(16)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 1
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_4_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_4_puncture, self).__init__()
        loadUi("injuries/puncture_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        #self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")
   
        #self.cut_step3 = QMovie("GIFs/cuts-2.gif")
        #self.gif_player_label_3.setMovie(self.cut_step3)
        #self.cut_step3.start()
        
    def next_step(self):
        window.setCurrentIndex(5)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 2
        window.setCurrentIndex(window.currentIndex()-1)
        
        
        
######################  PUNCTURE PROCEDURES STEPS (5 windows TOTAL)  ###################### 

class Ui_degrees_burns(QMainWindow):
    def __init__(self):
        super(Ui_degrees_burns, self).__init__()
        loadUi("injuries/burns_degrees.ui", self)
        self.next_step_button_4.clicked.connect(self.next_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        self.call_nurse_button.clicked.connect(self.call_nurse)
        
    def next_step(self):
        window.setCurrentIndex(18)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 1
        window.setCurrentIndex(2)
        
    def call_nurse(self):
        pass
        
class Ui_before_steps_burns(QMainWindow):
    def __init__(self):
        super(Ui_before_steps_burns, self).__init__()
        loadUi("injuries/burns_before_steps.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("GIFs/burns-remove-jewelries.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(19)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
        
class Ui_step_1_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_1_burn, self).__init__()
        loadUi("injuries/burns_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("GIFs/burns-1.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(20)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_2_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_2_burn, self).__init__()
        loadUi("injuries/burns_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(21)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_3_burn, self).__init__()
        loadUi("injuries/burns_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1_3 = QMovie("GIFs/burns-3.gif")
        self.gif_player_label_3.setMovie(self.cut_step1_3)
        self.cut_step1_3.start()
        
    def next_step(self):
        window.setCurrentIndex(5)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
        
        
######################  POISON PROCEDURES STEPS (6 windows TOTAL)  ###################### 
        
class Ui_posion_types(QMainWindow):
    def __init__(self):
        super(Ui_posion_types, self).__init__()
        loadUi("injuries/poison_types.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(23)
    
    def go_back(self):
        
        window.setCurrentIndex(2)
        
class Ui_step_1_poison(QMainWindow):
    def __init__(self):
        super(Ui_step_1_poison, self).__init__()
        loadUi("injuries/poison_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(24)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_2_poison(QMainWindow):
    def __init__(self):
        super(Ui_step_2_poison, self).__init__()
        loadUi("injuries/poison_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(25)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_poison(QMainWindow):
    def __init__(self):
        super(Ui_step_3_poison, self).__init__()
        loadUi("injuries/poison_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(26)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_poison_inhalation(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_inhalation, self).__init__()
        loadUi("injuries/poison_inhalation.ui", self)
        
        self.next_step_button_4.clicked.connect(self.next_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(27)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_poison_skin_eyes(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_skin_eyes, self).__init__()
        loadUi("injuries/poison_skin_eye.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(5)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)




        
app = QApplication(sys.argv)
window = QtWidgets.QStackedWidget()




#############################  ADD CLASS HERE  /  ADDING THE WINDOWS IN THE WIDGETS FOR INDEXING  #############################

window.addWidget(Ui_scan_qr_code()) # INDEX 0
window.addWidget(Ui_select_body_part()) # INDEX 1
window.addWidget(Ui_select_injury_type()) # INDEX 2
window.addWidget(Ui_enter_injury())  # INDEX 3
window.addWidget(Ui_request_nurse())  # INDEX 4
window.addWidget(Ui_confirmation()) # INDEX 5
window.addWidget(Ui_confirmation_again()) # INDEX 6
window.addWidget(Ui_scan_qr_patient()) # INDEX 7
window.addWidget(Ui_gender_patient_window()) # INDEX 8

window.addWidget(Ui_step_1_cut()) # INDEX 9
window.addWidget(Ui_step_2_cut()) # INDEX 10
window.addWidget(Ui_step_3_cut()) # INDEX 11
window.addWidget(Ui_step_4_cut()) # INDEX 12

window.addWidget(Ui_step_1_puncture()) # INDEX 13
window.addWidget(Ui_step_2_puncture()) # INDEX 14
window.addWidget(Ui_step_3_puncture()) # INDEX 15
window.addWidget(Ui_step_4_puncture()) # INDEX 16

window.addWidget(Ui_degrees_burns()) # INDEX 17
window.addWidget(Ui_before_steps_burns()) # INDEX 18
window.addWidget(Ui_step_1_burn()) # INDEX 19
window.addWidget(Ui_step_2_burn()) # INDEX 20
window.addWidget(Ui_step_3_burn()) # INDEX 21

window.addWidget(Ui_posion_types()) # INDEX 22
window.addWidget(Ui_step_1_poison()) # INDEX 23
window.addWidget(Ui_step_2_poison()) # INDEX 24
window.addWidget(Ui_step_3_poison()) # INDEX 25
window.addWidget(Ui_step_poison_inhalation()) # INDEX 26
window.addWidget(Ui_step_poison_skin_eyes()) # INDEX 27


#######################  PARAMETERS FOR THE WINDOW (EXACT FOR THE TOUCH SCREEN)  #######################

window.setMaximumHeight(600)
window.setMaximumWidth(1024)
window.setWindowTitle("Interactive First Aid Cabinet - BET COET 4A - Build 2022")

window.show()
sys.exit(app.exec_())