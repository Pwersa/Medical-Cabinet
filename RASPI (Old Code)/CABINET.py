#! /usr/bin/env python
import sys, cv2, datetime, time, re, csv, socket, os, threading, ast, smtplib, tqdm, json, glob
import http.client
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QSpinBox, QMessageBox, QScrollArea, QScroller, \
                                QScrollerProperties, QRadioButton, QLineEdit, QPushButton, QWidget, QComboBox
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie
from record_session import Ui_record_session
from cabinet_notif import Ui_cabinet_notif
from confirm_name import Ui_whitelist_confirm
from whitelist_error import Ui_whitelist_error
from tkinter import *
from email.mime.text import MIMEText

# DATE AND TIME, RESPONDER ID, NAME, COURSE, PATIENT ID, NAME, COURSE, GENDER, INJURY TYPE (used are also for csv file)
session_time = []
responder_time = []
session = []
body_parts_selected = []
injury_types_selected = ["Placeholder"]

# All available options in their respective type
injury_type_selection = ["Cut", "Poison", "Puncture", "Burn", "Electric", "Bruises", "Laceration", "Others"]
body_parts_list = ["Neck", "Stomach", "Thigh", "Crotch", "Legs", "Head", "Arm", "Hand", "Knee", "Foot"]
arm = ["Shoulder", "Forearm", "Wrist", "Elbow"]
face = ["Lips", "Nose", "Ears", "Cheeks", "Eyes", "Jaw", "Forehead", "Chin"]
hand = ["Palm", "Wrist", "Knuckles", "Fingers"]
gender_types = ["Male", "Female", "N/A"]

# alphabets
alphabet = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', "Backspace"], 
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '.'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', " "]]

input_text = []
input_name = []

# Used for adding whitelist data (DEBUG)
scanned_data = []

# Used for checking if the 1st send (responder) is succesfull, if not, 
# it will send again in the end with the last sending which is session
check_connection_companion = [0]

# CHeck if responder notification was activated (0 by default which means its not)
responder_notif = [0]

# OPEN CONFIGURATION FILES AS SOON PROGRAM RUNS (IP ADDRESS, PORT, EMAIL, etc.)
with open("config/config.json", "r") as data:
    configuration_settings = json.load(data)

# UPDATE DYNAMIC LIST IN ORDER TO FOLLOW THE NOT SENT FILES
for i in configuration_settings["files_not_sent_responder"]:
    responder_time.append(i)

for i in configuration_settings["files_not_sent_session"]:
    session_time.append(i)
    
print("NOT SENT DATA")
print(responder_time)
print(session_time)

# DEBUG
checked_button = []
restart_button = []

class Ui_scan_qr_code(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_code, self).__init__()
        loadUi("scan_qr_code.ui", self)
        self.scan_button.clicked.connect(self.qr_camera)
        self.hidden_button.clicked.connect(self.hidden_settings)
        self.restart_button.clicked.connect(self.restart_program)
    
    def qr_camera(self):
        
        # Check config file for CAMERA
        if configuration_settings["enable_camera"] == True:
            print("CAMERA IS CONNECTED")
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

                # ID_Identifier
                id_identify = configuration_settings["id_identifier"]
                
                # Whitelist
                whitelisted_name = configuration_settings["whitelisted"]
                
                if data:      
                    if id_identify in data:
                        print("TUPC ID IS SCANNED")
            
                        dt = datetime.datetime.now()
                        time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                        regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                        parsed_text = regexp.findall(data)
                        fullname = str(parsed_text[1]+" "+ parsed_text[2])

                        # 1st QR CODE RESPONDER of COET
                        session.append(str(time_now))
                        # ID
                        session.append(parsed_text[0])
                        # NAME
                        session.append(fullname)
                        # COURSE
                        session.append(parsed_text[-2])
                
                        cap.release()
                        cv2.destroyAllWindows()
                        window.setCurrentIndex(2)
                        break
                    
                    result = any(item in data for item in whitelisted_name)
                    
                    if result == True:
                        print("OTHERS IS SCANNED")
                
                        dt = datetime.datetime.now()
                        time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                        regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                        parsed_text = regexp.findall(data)
                        fullname = str(parsed_text[0]+" "+ parsed_text[1])
                        
                        session.append(str(time_now))
                        session.append("Teacher")
                        session.append(fullname)

                        cap.release()
                        cv2.destroyAllWindows()
                        window.setCurrentIndex(2)
                        break
    
                if (cv2.waitKey(1) == ord("r")):
                    time.sleep(0.5)
                    dt = datetime.datetime.now()
                    x = dt.strftime("%Y-%m-%d %H-%M-%S")
                    session.append(str(x))
                    # ID
                    session.append("TUPC-RESPONDER")
                    # NAME
                    session.append("JR ANGELO")
                    # COURSE
                    session.append("COET")

                    cap.release()
                    cv2.destroyAllWindows()
                    window.setCurrentIndex(2)

                    break

                if (cv2.waitKey(2) == ord("y")):
                    if configuration_settings["enable_debug_window"] == True:
                        
                        cap.release()
                        cv2.destroyAllWindows()
                        window.setCurrentIndex(50)
                        break

                    else:
                    
                        break            

        else:
            print("CAMERA IS NOT CONNECTED")
            dt = datetime.datetime.now()
            x = dt.strftime("%Y-%m-%d %H-%M-%S")
            session.append(str(x))
            # ID
            session.append("TUPC-RESPONDER")
            # NAME
            session.append("JR ANGELO")
            # COURSE
            session.append("COET")
            window.setCurrentIndex(2)
            
    def hidden_settings(self):
        if len(checked_button) >= 5:
            print("ITS UP")
            window.setCurrentIndex(50)
            checked_button.clear()
            
        else:
            checked_button.append(1)
            print("HIDDEN >>>>")
            
    def restart_program(self):
        window.refresh()

class Ui_scan_qr_patient(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_patient, self).__init__()
        loadUi("scan_qr_code_again.ui", self)
        self.guest_patient_window.clicked.connect(self.guest_patient)
        self.scan_qr_patient.clicked.connect(self.qr_camera)
        
    def guest_patient(self):
        session.append("GUEST")
        window.setCurrentIndex(29)
        responder_notif.clear()
        responder_notif.append(0)

    def qr_camera(self):
        responder_notif.clear()
        responder_notif.append(0)
        body_parts_selected.clear()
        injury_types_selected.clear()
        injury_types_selected.insert(0, "Placeholder")
        
        # Check config file for CAMERA
        if configuration_settings["enable_camera"] == True:
            print("CAMERA IS CONNECTED")
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

                # ID_Identifier
                id_identify = configuration_settings["id_identifier"]
                
                # Whitelist
                whitelisted_name = configuration_settings["whitelisted"]
                
                if data:      
                    if id_identify in data:
                        print("TUPC ID IS SCANNED")
            
                        dt = datetime.datetime.now()
                        time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                        regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                        parsed_text = regexp.findall(data)
                        fullname = str(parsed_text[1]+" "+ parsed_text[2])

                        # 1st QR CODE RESPONDER of COET
                        session.append(str(time_now))
                        # ID
                        session.append(parsed_text[0])
                        # NAME
                        session.append(fullname)
                        # COURSE
                        session.append(parsed_text[-2])
                
                        cap.release()
                        cv2.destroyAllWindows()
                        window.setCurrentIndex(8)

                        break
                    
                    
                    result = any(item in data for item in whitelisted_name)
                    
                    if result == True:
                        print("OTHERS IS SCANNED")
                
                        dt = datetime.datetime.now()
                        time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                        regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                        parsed_text = regexp.findall(data)
                        fullname = str(parsed_text[0]+" "+ parsed_text[1])
                        
                        session.append(str(time_now))
                        session.append("Teacher")
                        session.append(fullname)

                        cap.release()
                        cv2.destroyAllWindows()
                        window.setCurrentIndex(8)

                        break
                        
                if (cv2.waitKey(1) == ord("p")):
                    session.insert(4, "TUPC-PATIENT")
                    # NAME
                    session.insert(5, "DURAN ROGIE")
                    # COURSE
                    session.insert(6, "COET")
                    time.sleep(0.5)

                    cap.release()
                    cv2.destroyAllWindows()
                    window.setCurrentIndex(8)
                    
                    break
            
        else:
            print("CAMERA IS NOT CONNECTED")
            dt = datetime.datetime.now()
            x = dt.strftime("%Y-%m-%d %H-%M-%S")
            session.append(str(x))
            # ID
            session.append("TUPC-RESPONDER")
            # NAME
            session.append("JR ANGELO")
            # COURSE
            session.append("COET")
            window.setCurrentIndex(0)
        
class Ui_select_injury_type(QMainWindow):
    def __init__(self):
        super(Ui_select_injury_type, self).__init__()
        loadUi("select_injury_type.ui", self)
        self.cut_button.clicked.connect(lambda: self.injuries(injury_type_selection[0]))
        self.poison_button.clicked.connect(lambda: self.injuries(injury_type_selection[1]))
        self.puncture_button.clicked.connect(lambda: self.injuries(injury_type_selection[2]))
        self.burn_button.clicked.connect(lambda: self.injuries(injury_type_selection[3]))
        self.electric_shock_button.clicked.connect(lambda: self.injuries(injury_type_selection[4]))
        self.bruises_button.clicked.connect(lambda: self.injuries(injury_type_selection[5]))
        self.laceration_button.clicked.connect(lambda: self.injuries(injury_type_selection[6]))
        self.others_button.clicked.connect(lambda: self.injuries(injury_type_selection[7]))

        # Used for hold and drag function
        self.scroll_area = self.findChild(QScrollArea, "scrollArea")
        self.scroll = QScroller.scroller(self.scroll_area.viewport())
        self.scroll.grabGesture(self.scrollArea.viewport(), QScroller.LeftMouseButtonGesture)
        self.props = self.scroll.scrollerProperties()
        #self.props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        self.scroll.setScrollerProperties(self.props)
        
    def injuries(self, injury_type_selection):
        if injury_type_selection == "Bruises":
            injury_types_selected.append("BRUISES") 
            window.setCurrentIndex(41)
            
        elif injury_type_selection == "Burn":
            injury_types_selected.append("BURN") 
            window.setCurrentIndex(42)
        
        elif injury_type_selection == "Cut":
            injury_types_selected.append("CUT") 
            window.setCurrentIndex(43)
        
        elif injury_type_selection == "Electric":
            injury_types_selected.append("ELECTRIC") 
            window.setCurrentIndex(44)
            
        elif injury_type_selection == "Laceration":
            injury_types_selected.append("LACERATION") 
            window.setCurrentIndex(45)
            
        elif injury_type_selection == "Poison":
            injury_types_selected.append("POISON") 
            window.setCurrentIndex(46)
            
        elif injury_type_selection == "Puncture":
            injury_types_selected.append("PUNCTURE") 
            window.setCurrentIndex(47)
            
        elif injury_type_selection == "Others":
            window.setCurrentIndex(3)
            
class Ui_select_body_part(QMainWindow):
    def __init__(self):
        super(Ui_select_body_part, self).__init__()
        loadUi("select_body_part.ui", self)
        self.neck_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[0]))
        self.stomach_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[1]))
        self.thigh_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[2]))
        self.crotch_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[3]))
        self.legs_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[4]))
        self.head_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[5]))
        self.arm_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[6]))
        self.hand_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[7]))
        self.knee_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[8]))
        self.foot_button.clicked.connect(lambda: self.body_part_buttons(body_parts_list[9]))
        
    def body_part_buttons(self, body_parts_list):
        if body_parts_list == "Neck":
            body_parts_selected.append("NECK") 
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Stomach":
            body_parts_selected.append("STOMACH")
            window.setCurrentIndex(1)
            self.injuries()
                         
        elif body_parts_list == "Thigh":
            body_parts_selected.append("THIGH")
            window.setCurrentIndex(1)
            self.injuries()
                        
        elif body_parts_list == "Crotch":
            body_parts_selected.append("CROTCH")
            window.setCurrentIndex(1)
            self.injuries()
                
        elif body_parts_list == "Legs":
            body_parts_selected.append("LEG")
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Knee":
            body_parts_selected.append("KNEE")
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Foot":
            body_parts_selected.append("FOOT")
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Head":
            body_parts_selected.append("HEAD")
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Arm":
            body_parts_selected.append("ARM")
            self.injuries()
            
        elif body_parts_list == "Hand":
            body_parts_selected.append("HAND")
            self.injuries()
    
    def injuries(self):
        # RASPBERRY PI SOLENOID SETTINGS
        # UNLOCK THE CABINET IF IN CONFIG IS TRUE, else no
        self.solenoid_threading()
        
        # DISPLAY THE WINDOW TELLING THAT THE SOLENOID IS UNLOCKED
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON (1)")
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
            
        else:
            print("SOLENOID FEATURE IS OFF (1)")
            pass

        if injury_types_selected[-1] == "CUT":
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_types_selected[-1] == "POISON":
            window.setCurrentIndex(27)
            self.responder_csv_file()
        
        elif injury_types_selected[-1] == "PUNCTURE":
            window.setCurrentIndex(28)
            self.responder_csv_file()
        
        elif injury_types_selected[-1] == "BURN":
            window.setCurrentIndex(28)
            self.responder_csv_file()
        
        elif injury_types_selected[-1] == "ELECTRIC":
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_types_selected[-1] == "BRUISES":
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_types_selected[-1] == "LACERATION":
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_type_selection == "Others":
            window.setCurrentIndex(3)
            
        elif injury_type_selection == "Go back to window":
            window.setCurrentIndex(window.currentIndex()-1) 
            
    def solenoid_threading(self):
        x = threading.Thread(target=self.open_close_solenoid)
        x.start()
            
    def open_close_solenoid(self):
        print("CALLED SOLENOID >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON (2)")
            
            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            print("GPIO SOLENOID OPEN")
            GPIO.output(18, 0)
            time.sleep(10)
            print("GPIO SOLENOID CLOSE")
            GPIO.output(18, 1)
            #GPIO.output(18, 1)
            
        else:
            print("SOLENOID FEATURE IS OFF (2)")
            pass 
            
            
    def responder_csv_file(self):
        # Check config file for saving csv (record data)
        if configuration_settings["allow_saving_csv"] == True:
            print("SAVING ALL IN A CSV FILE...")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
            
            print(session)
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            print("CSV FILE WAS NOT CREATED.")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
        
        # Check config file for sending email
        # EMAIL ALSO SENT TO THE NURSE
        if configuration_settings["email_connection"] == True:
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
            
                server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
                server.sendmail("coetmedicalcabinet.2022@gmail.com", configuration_settings["email"], "EMERGENCY RECEIVED FROM THE MEDICAL CABINET!")
            except:
                pass    
            
        else:
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            if responder_notif[0] == 0:
                print("Will try to connect to to Companion APP")
                self.responder_threading()
                responder_notif.clear()
                responder_notif.append(1)
            else:
                pass
                
        else:
            pass
        
    def responder_threading(self):   
        x = threading.Thread(target=self.send_to_companion_responder)
        x.start()
        
    def send_to_companion_responder(self):                           
        try:
            print("TRYING TO CHECK INTERNET CONNECTION") 
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            time.sleep(3)
            
            print("TRYING TO SEND DATA")
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096
            
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
            
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)

            s = socket.socket()

            s.settimeout(5)
            s.connect((host, port))
            print("[+] Connected.")

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

            #os.remove("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv")
            s.close()

        except:
            
            # VERY IMPORTANT TO ADD THE SESSION TIME IN THIS LIST WHEN IT ERRORS... TRUST ME.
            responder_time.append(session[0])
            
            # UPDATING THE CONFIG FILE ASAP
            with open("config/config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["files_not_sent_responder"].append(responder_time[-1])

            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                print("WRITE TO CONFIG SUCCESS")
                
            print("SEND DATA FAILED")
            print("NO INTERNET CONNECTION")
            check_connection_companion.clear()
            check_connection_companion.append(1)
            #window.setCurrentIndex(41)

            #TKINTER for window if connection to the companion app was failed
            root = Tk()
            root.geometry('800x600')

            def delete_items():
                root.destroy()

            frame1 = Frame(root)
            frame1.configure(bg='gray')
            frame1.pack()

            title = Label(frame1, text = "FAILED!!! TO SEND\nEMERGENCY\nNOTIFICATION", font=("Unispace", 48))
            title.grid(row=0, column=0, pady=(20, 0))

            title_2 = Label(frame1, text = "Please check the Clinic manually\nif the Nurse is PRESENT", font=("Unispace", 28))
            title_2.grid(row=1, column=0, pady=(20, 10))

            button_remove = Button(frame1, text = "CONFIRM", command = delete_items, font=("Unispace", 45, "bold", "underline"))
            button_remove.config(height=1, width=10)
            button_remove.grid(row=2, column=0)

            root.title("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
            root.configure(bg='gray')
            root.mainloop()
            
            return False
        
class Ui_enter_injury(QMainWindow):
    def __init__(self):
        super(Ui_enter_injury, self).__init__()
        loadUi("enter_injury.ui", self)
        self.typed_injury = self.findChild(QLineEdit, "typed_injury")
        self.enter_button.clicked.connect(self.enter_injury)
        self.enter_injury_go_back_button.clicked.connect(self.go_back)
        self.text_clear.clicked.connect(self.clear_text)

        # keyboard
        self.number1_button = self.findChild(QPushButton, "number_1")
        self.number1_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][0]))

        self.number2_button = self.findChild(QPushButton, "number_2")
        self.number2_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][1]))

        self.number3_button = self.findChild(QPushButton, "number_3")
        self.number3_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][2]))

        self.number4_button = self.findChild(QPushButton, "number_4")
        self.number4_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][3]))

        self.number5_button = self.findChild(QPushButton, "number_5")
        self.number5_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][4]))

        self.number6_button = self.findChild(QPushButton, "number_6")
        self.number6_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][5]))

        self.number7_button = self.findChild(QPushButton, "number_7")
        self.number7_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][6]))

        self.number8_button = self.findChild(QPushButton, "number_8")
        self.number8_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][7]))

        self.number9_button = self.findChild(QPushButton, "number_9")
        self.number9_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][8]))

        self.number0_button = self.findChild(QPushButton, "number_0")
        self.number0_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][9]))

        self.a_button = self.findChild(QPushButton, "a_button")
        self.a_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][0]))

        self.b_button = self.findChild(QPushButton, "b_button")
        self.b_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][4]))

        self.c_button = self.findChild(QPushButton, "c_button")
        self.c_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][2]))

        self.d_button = self.findChild(QPushButton, "d_button")
        self.d_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][2]))

        self.e_button = self.findChild(QPushButton, "e_button")
        self.e_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][2]))

        self.f_button = self.findChild(QPushButton, "f_button")
        self.f_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][3]))

        self.g_button = self.findChild(QPushButton, "g_button")
        self.g_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][4]))

        self.h_button = self.findChild(QPushButton, "h_button")
        self.h_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][5]))

        self.i_button = self.findChild(QPushButton, "i_button")
        self.i_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][7]))

        self.j_button = self.findChild(QPushButton, "j_button")
        self.j_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][6]))

        self.k_button = self.findChild(QPushButton, "k_button")
        self.k_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][7]))

        self.l_button = self.findChild(QPushButton, "l_button")
        self.l_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][8]))

        self.m_button = self.findChild(QPushButton, "m_button")
        self.m_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][6]))

        self.n_button = self.findChild(QPushButton, "n_button")
        self.n_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][5]))

        self.o_button = self.findChild(QPushButton, "o_button")
        self.o_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][8]))

        self.p_button = self.findChild(QPushButton, "p_button")
        self.p_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][9]))

        self.q_button = self.findChild(QPushButton, "q_button")
        self.q_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][0]))

        self.r_button = self.findChild(QPushButton, "r_button")
        self.r_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][3]))

        self.s_button = self.findChild(QPushButton, "s_button")
        self.s_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][1]))

        self.t_button = self.findChild(QPushButton, "t_button")
        self.t_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][4]))

        self.u_button = self.findChild(QPushButton, "u_button")
        self.u_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][6]))

        self.v_button = self.findChild(QPushButton, "v_button")
        self.v_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][3]))

        self.w_button = self.findChild(QPushButton, "w_button")
        self.w_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][1]))

        self.x_button = self.findChild(QPushButton, "x_button")
        self.x_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][1]))
        
        self.y_button = self.findChild(QPushButton, "y_button")
        self.y_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][5]))

        self.z_button = self.findChild(QPushButton, "z_button")
        self.z_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][0]))

        self.backspace_button = self.findChild(QPushButton, "backspace_button")
        self.backspace_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][11]))

        self.hypen_button = self.findChild(QPushButton, "hypen_button")
        self.hypen_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][10]))

        self.spacebar_button = self.findChild(QPushButton, "spacebar_button")
        self.spacebar_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][7]))

    def clear_text(self):
        input_text.clear()
        self.typed_injury.setText("")
        self.typed_injury.setCursorPosition(0)

    def input_keyboard(self, alphabet):
        if alphabet == "Backspace":
            check = self.typed_injury.cursorPosition()
            subtract = check - 1
        
            if len(input_text) >= 1:
                input_text.pop(subtract)
                new_string = "".join(input_text)
                self.typed_injury.setText(new_string)
                self.typed_injury.setCursorPosition(subtract)
                self.typed_injury.hasFocus()

            else:
                pass

        elif alphabet == " ":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "1":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "2":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "3":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "4":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "5":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "6":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "7":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "8":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "9":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "0":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)
        
        elif alphabet == "-":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "Q":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "W":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "E":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "R":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "T":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "Y":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "U":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "I":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "O":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "P":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "A":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "S":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "D":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "F":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "G":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "H":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "J":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "K":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "L":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "Z":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "X":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "C":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "V":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "B":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "N":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "M":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

    def enter_injury(self):
        if configuration_settings["allow_saving_csv"] == True:
            print("SAVING ALL IN A CSV FILE...")
            session.append(self.typed_injury.text())
            session.append("OTHER is selected")
            
            print(session)
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
            
            input_text.clear()
            window.setCurrentIndex(4)
            
            # VERY IMPORTANT TO ADD THE SESSION TIME... TRUST ME.
            responder_time.append(session[0])
            
            # UPDATING THE CONFIG FILE ASAP
            with open("config/config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["files_not_sent_responder"].append(responder_time[-1])

            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                print("WRITE TO CONFIG SUCCESS")
                
            # CLEAR LIST FOR NEW DATA TO SAVE
            session.clear()
            
        else:
            print("Disabled saving typed data to csv file")
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            self.enter_injury_threading()
        else:
            print("DISABLED CONNECTING TO COMPANION APP")
            pass
        
        window.setCurrentIndex(4)
        
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def enter_injury_threading(self):
        x = threading.Thread(target=self.send_injury)
        x.start()
    
    def send_injury(self):
        try:
            print("TRYING TO CHECK INTERNET CONNECTION") 
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            time.sleep(1)
            
            print("TRYING TO SEND DATA")
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096
            
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
            
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + responder_time[-1] + ".csv"
            filesize = os.path.getsize(filename)

            s = socket.socket()

            s.settimeout(3)
            s.connect((host, port))
            print("[+] Connected.")

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
                    
            responder_time.pop()
            
            with open("config/config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["files_not_sent_responder"] = responder_time

            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                print("WRITE TO CONFIG SUCCESS")

            #os.remove("cabinet-history/responder/recorded_accessed_responder" + " " + responder_time[-1] + ".csv")
            s.close()

        except:

            #TKINTER for window if connection to the companion app was failed
            root = Tk()
            root.geometry('800x600')

            def delete_items():
                root.destroy()

            frame1 = Frame(root)
            frame1.configure(bg='gray')
            frame1.pack()

            title = Label(frame1, text = "FAILED!!! TO SEND\nEMERGENCY\nNOTIFICATION", font=("Unispace", 48))
            title.grid(row=0, column=0, pady=(20, 0))

            title_2 = Label(frame1, text = "Please check the Clinic manually\nif the Nurse is PRESENT", font=("Unispace", 28))
            title_2.grid(row=1, column=0, pady=(20, 10))

            button_remove = Button(frame1, text = "CONFIRM", command = delete_items, font=("Unispace", 45, "bold", "underline"))
            button_remove.config(height=1, width=10)
            button_remove.grid(row=2, column=0)

            root.title("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
            root.configure(bg='gray')
            root.mainloop()
            
            return False

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
            window.setCurrentIndex(28)

        elif injury_types_selected[-1] == "POISON_INHALATION":
            window.setCurrentIndex(26)
            
        elif injury_types_selected[-1] == "POISON_INGESTION":
            window.setCurrentIndex(23)
            
        elif injury_types_selected[-1] == "POISON_CONTACT":
            window.setCurrentIndex(27)
            
        elif injury_types_selected[-1] == "PUNCTURE":
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "ELECTRIC":
            window.setCurrentIndex(30)
            
        elif injury_types_selected[-1] == "BRUISES":
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "LACERATION":
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "BURN":
            window.setCurrentIndex(28)
        
    def yes_confirmation(self):
        window.setCurrentIndex(6)

class Ui_confirmation_again(QMainWindow):
    def __init__(self):
        super(Ui_confirmation_again, self).__init__()
        loadUi("confirmation_again.ui", self)
        self.new_injury_button.clicked.connect(self.new_injury)
        self.finish_procedure.clicked.connect(self.done_procedure)

    def new_injury(self):
        window.setCurrentIndex(2)
    
    # GOING TO SCAN QR CODE AGAIN BUT FOR THE PATIENT
    def done_procedure(self):
        window.setCurrentIndex(7)
        
class Ui_guest_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_guest_patient_window, self).__init__()
        loadUi("guest_patient_info.ui", self)
        self.confirm_guest.clicked.connect(self.guest_info)
        
        self.name_info = self.findChild(QLineEdit, "name_info")

        # keyboard
        self.number1_button = self.findChild(QPushButton, "number_1")
        self.number1_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][0]))

        self.number2_button = self.findChild(QPushButton, "number_2")
        self.number2_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][1]))

        self.number3_button = self.findChild(QPushButton, "number_3")
        self.number3_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][2]))

        self.number4_button = self.findChild(QPushButton, "number_4")
        self.number4_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][3]))

        self.number5_button = self.findChild(QPushButton, "number_5")
        self.number5_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][4]))

        self.number6_button = self.findChild(QPushButton, "number_6")
        self.number6_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][5]))

        self.number7_button = self.findChild(QPushButton, "number_7")
        self.number7_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][6]))

        self.number8_button = self.findChild(QPushButton, "number_8")
        self.number8_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][7]))

        self.number9_button = self.findChild(QPushButton, "number_9")
        self.number9_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][8]))

        self.number0_button = self.findChild(QPushButton, "number_0")
        self.number0_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][9]))

        self.a_button = self.findChild(QPushButton, "a_button")
        self.a_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][0]))

        self.b_button = self.findChild(QPushButton, "b_button")
        self.b_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][4]))

        self.c_button = self.findChild(QPushButton, "c_button")
        self.c_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][2]))

        self.d_button = self.findChild(QPushButton, "d_button")
        self.d_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][2]))

        self.e_button = self.findChild(QPushButton, "e_button")
        self.e_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][2]))

        self.f_button = self.findChild(QPushButton, "f_button")
        self.f_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][3]))

        self.g_button = self.findChild(QPushButton, "g_button")
        self.g_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][4]))

        self.h_button = self.findChild(QPushButton, "h_button")
        self.h_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][5]))

        self.i_button = self.findChild(QPushButton, "i_button")
        self.i_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][7]))

        self.j_button = self.findChild(QPushButton, "j_button")
        self.j_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][6]))

        self.k_button = self.findChild(QPushButton, "k_button")
        self.k_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][7]))

        self.l_button = self.findChild(QPushButton, "l_button")
        self.l_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][8]))

        self.m_button = self.findChild(QPushButton, "m_button")
        self.m_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][6]))

        self.n_button = self.findChild(QPushButton, "n_button")
        self.n_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][5]))

        self.o_button = self.findChild(QPushButton, "o_button")
        self.o_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][8]))

        self.p_button = self.findChild(QPushButton, "p_button")
        self.p_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][9]))

        self.q_button = self.findChild(QPushButton, "q_button")
        self.q_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][0]))

        self.r_button = self.findChild(QPushButton, "r_button")
        self.r_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][3]))

        self.s_button = self.findChild(QPushButton, "s_button")
        self.s_button.clicked.connect(lambda: self.input_keyboard(alphabet[2][1]))

        self.t_button = self.findChild(QPushButton, "t_button")
        self.t_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][4]))

        self.u_button = self.findChild(QPushButton, "u_button")
        self.u_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][6]))

        self.v_button = self.findChild(QPushButton, "v_button")
        self.v_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][3]))

        self.w_button = self.findChild(QPushButton, "w_button")
        self.w_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][1]))

        self.x_button = self.findChild(QPushButton, "x_button")
        self.x_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][1]))
        
        self.y_button = self.findChild(QPushButton, "y_button")
        self.y_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][5]))

        self.z_button = self.findChild(QPushButton, "z_button")
        self.z_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][0]))

        self.backspace_button = self.findChild(QPushButton, "backspace_button")
        self.backspace_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][11]))

        self.hypen_button = self.findChild(QPushButton, "hypen_button")
        self.hypen_button.clicked.connect(lambda: self.input_keyboard(alphabet[0][10]))
        
        self.period_button = self.findChild(QPushButton, "period_button")
        self.period_button.clicked.connect(lambda: self.input_keyboard(alphabet[1][10]))
        
        self.spacebar_button = self.findChild(QPushButton, "spacebar_button")
        self.spacebar_button.clicked.connect(lambda: self.input_keyboard(alphabet[3][7]))

    def input_keyboard(self, alphabet):
        
        if alphabet == "Backspace":
            check = self.name_info.cursorPosition()
            subtract = check - 1
        
            if len(input_name) >= 1:
                input_name.pop(subtract)
                new_string = "".join(input_name)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(subtract)
                self.name_info.hasFocus()

            else:
                pass
            

        elif alphabet == " ":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "1":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "2":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "3":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "4":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "5":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "6":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "7":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "8":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "9":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "0":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)
        
        elif alphabet == "-":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "Q":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "W":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "E":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "R":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "T":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "Y":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "U":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "I":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "O":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "P":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)
            
        elif alphabet == ".":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "A":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "S":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "D":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "F":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "G":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "H":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "J":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "K":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "L":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "Z":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "X":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "C":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "V":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "B":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "N":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)

        elif alphabet == "M":
            check = self.name_info.cursorPosition()
            input_name.insert(check, alphabet)
            new_string = "".join(input_name)

            self.name_info.setText(new_string)
            self.name_info.setCursorPosition(check + 1)
        
    def guest_info(self):
        session.insert(5, self.name_info.text())
        self.name_info.setText("")
        input_name.clear()
        window.setCurrentIndex(8)
        
class Ui_gender_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_gender_patient_window, self).__init__()
        loadUi("patient_gender.ui", self)
        self.confirm_guest.clicked.connect(self.gender_and_age_submit)
        
        self.age =  self.findChild(QSpinBox, "age_box")
        self.male_radio = self.findChild(QRadioButton, "male_checkbox")
        self.female_radio = self.findChild(QRadioButton, "female_checkbox")
            
    def gender_and_age_submit(self):
        if self.male_checkbox.isChecked():
            session.append("MALE")
            session.append(self.age.value())
            self.record_session_window()
            
            input_text.clear()
            input_name.clear()
            body_parts_selected.clear()
            injury_types_selected.clear()
            injury_types_selected.insert(0, "Placeholder")
            
        elif self.female_checkbox.isChecked():
            session.append("FEMALE")
            session.append(self.age.value())
            self.record_session_window()
            
            input_text.clear()
            input_name.clear()
            body_parts_selected.clear()
            injury_types_selected.clear()
            injury_types_selected.insert(0, "Placeholder")
        
    def record_session_window(self):
        self.window_record_session = QtWidgets.QMainWindow()
        self.ui = Ui_record_session()
        self.ui.setupUi(self.window_record_session)
        self.window_record_session.show()
        
        session.insert(6, "GUEST PATIENT")

        self.ui.qr_responder_name.setText(session[2] + " - " + session[3])
        self.ui.qr_patient_name.setText(session[5] + " - " + session[6])
        self.ui.date_session.setText(session[0])
        
        self.respond = session[2] + " - " + session[3]
        self.patient = session[5] + " - " + session[6]
        self.date = session[0]

        self.ui.qr_responder_name.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">{self.respond}</span></p></body><html>")
        self.ui.qr_patient_name.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">{self.patient}</span></p></body><html>")
        self.ui.date_session.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{self.date}</span></p></body></html>")
        self.ui.body_injured.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{}</span></p></body></html>".format(", ".join(body_parts_selected)))
        self.ui.type_of_injury.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{}</span></p></body></html>".format(", ".join(injury_types_selected[1:])))

        #data_qr.clear()
        
        window.setCurrentIndex(0)
        self.save_session_tolocal()

    def save_session_tolocal(self):
        
        if configuration_settings["allow_saving_csv"] == True:
            filename = "cabinet-history/session/recorded_session" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("cabinet-history/session/recorded_session" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
        
        else:
            pass
        
        # VERY IMPORTANT TO SAVE THE TIME BEFORE CLEARING OUT
        session_time.append(session[0])
        
        print("UPDATING THE CONFIG FILE")
        with open("config/config.json", "r") as jsonFile:
            data = json.load(jsonFile)
            
        data["files_not_sent_session"] = session_time
        
        with open("config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)
                    
        session.clear()
            
        if configuration_settings["connection_mode"] == True:
            self.session_threading()
        else:
            pass
        
    def session_threading(self):
        x = threading.Thread(target=self.send_to_companion)
        x.start()
        
    def send_to_companion(self):
        try:
            # CHECK IF THERE ARE STILL FILES NOT SENT
            print("CHECK FOR SESSION FILES ")
            if len(session_time) == 0:
                pass
            
            else:
                print("TRYING TO CHECK INTERNET CONNECTION") 
                conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
                conn.close()
                time.sleep(3)

                HOST = configuration_settings["companion_app_IP"]
                PORT = configuration_settings["port_2nd"]
                SIZE = 1024
                FORMAT = "utf"
                CLIENT_FOLDER = "cabinet-history"

                # Starting a tcp socket
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))

                # Folder path 
                path = os.path.join(CLIENT_FOLDER, "session")
                folder_name = path.split("/")[-1]

                # Sending the folder name """
                msg = f"{folder_name}"
                print(f"[CLIENT] Sending folder name: {folder_name}")
                client.send(msg.encode(FORMAT))

                # Receiving the reply from the server """
                msg = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER] {msg}\n")

                # Sending files """
                files = sorted(os.listdir(path))

                for file_name in files:
                    
                    # Send the file name """
                    msg = f"FILENAME:{file_name}"
                    print(f"[CLIENT] Sending file name: {file_name}")
                    client.send(msg.encode(FORMAT))
                    
                    # CHECK IF LIST WAS UPDATED
                    print("SESSION BEFORE POP")
                    session_time.pop()
                    print("SESSIOBN AFTER POP")
                    print(session_time)
                    
                    # UPDATE THE CONFIG FILE
                    print("UPDATING THE CONFIG FILE")
                    with open("config/config.json", "r") as jsonFile:
                        data = json.load(jsonFile)
                        
                    data["files_not_sent_session"] = session_time
                    
                    with open("config/config.json", "w") as jsonFile:
                        json.dump(data, jsonFile)

                    # Recv the reply from the server 
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")

                    # Send the data 
                    file = open(os.path.join(path, file_name), "r")
                    file_data = file.read()

                    msg = f"DATA:{file_data}"
                    client.send(msg.encode(FORMAT))
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")
                    
                    
                    # Sending the close command 
                    msg = f"FINISH:Complete data send"
                    client.send(msg.encode(FORMAT))
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")

                # Closing the connection from the server 
                msg = f"CLOSE:File transfer is completed"
                client.send(msg.encode(FORMAT))
                client.close()
                
            # ADD TIMER SO THE COMPANION APP WILL NOT BE CONFUSED
            time_send_next_data = configuration_settings["debug_time_send"]
            print(time_send_next_data)
            time.sleep(time_send_next_data)    
                
            # CHECK IF THERE ARE STILL FILES NOT SENT
            print("CHECK FOR RESPONDER FILES ")
            if len(responder_time) == 0:
                print("(RESPONDER) NO FILES WHERE NEEDED TO SEND")
                pass
            else:
                print("(RESPONDER) THERE ARE FILES NEEDED TO SEND")
                print("TRYING TO CHECK INTERNET CONNECTION") 
                conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
                conn.close()
                time.sleep(3)

                HOST = configuration_settings["companion_app_IP"]
                PORT = configuration_settings["port_3rd"]
                SIZE = 1024
                FORMAT = "utf"
                CLIENT_FOLDER = "cabinet-history"

                # Starting a tcp socket
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((HOST, PORT))

                # Folder path 
                path = os.path.join(CLIENT_FOLDER, "responder")
                folder_name = path.split("/")[-1]

                # Sending the folder name 
                msg = f"{folder_name}"
                print(f"[CLIENT] Sending folder name: {folder_name}")
                client.send(msg.encode(FORMAT))

                # Receiving the reply from the server 
                msg = client.recv(SIZE).decode(FORMAT)
                print(f"[SERVER] {msg}\n")

                # Sending files 
                files = sorted(os.listdir(path))

                for file_name in files:
                    
                    # Send the file name 
                    msg = f"FILENAME:{file_name}"
                    print(f"[CLIENT] Sending file name: {file_name}")
                    client.send(msg.encode(FORMAT))
                    
                    # CHECK IF LIST WAS UPDATED
                    print("RESPONDER BEFORE POP")
                    responder_time.pop()
                    print("RESPONDER AFTER POP")
                    print(responder_time)
                    
                    # UPDATE THE CONFIG FILE
                    print("UPDATING THE CONFIG FILE")
                    with open("config/config.json", "r") as jsonFile:
                        data = json.load(jsonFile)
                        
                    data["files_not_sent_responder"] = responder_time
                    
                    with open("config/config.json", "w") as jsonFile:
                        json.dump(data, jsonFile)

                    # Recv the reply from the server 
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")

                    # Send the data 
                    file = open(os.path.join(path, file_name), "r")
                    file_data = file.read()

                    msg = f"DATA:{file_data}"
                    client.send(msg.encode(FORMAT))
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")

                    # Sending the close command 
                    msg = f"FINISH:Complete data send"
                    client.send(msg.encode(FORMAT))
                    msg = client.recv(SIZE).decode(FORMAT)
                    print(f"[SERVER] {msg}")

                # Closing the connection from the server 
                msg = f"CLOSE:File transfer is completed"
                client.send(msg.encode(FORMAT))
                client.close()
         
        except:
            print("SEND DATA FAILED")
            print("NO INTERNET CONNECTION OR COMPANION APP IS NOT AVAILABLE")
            check_connection_companion.clear()
            check_connection_companion.append(1)
            

            #window.setCurrentIndex(41)
        
        
####################### STEPS UI FOR EVERY INJURIES  #######################

class Ui_before_procedures(QMainWindow):
    def __init__(self):
        super(Ui_before_procedures, self).__init__()
        loadUi("injuries/before_procedures_cautions.ui", self)
        self.goto_steps_button.clicked.connect(self.injuries)
    
    def injuries(self):
        if injury_types_selected[-1] == "CUT":
            window.setCurrentIndex(9)
        
        elif injury_types_selected[-1] == "PUNCTURE":
            window.setCurrentIndex(13)

        elif injury_types_selected[-1] == "BURN":
            window.setCurrentIndex(18)
            
        elif "POISON" in injury_types_selected: 
            window.setCurrentIndex(22)
            
        elif injury_types_selected[-1] == "POISON_INHALATION":
            window.setCurrentIndex(26)
            
        elif injury_types_selected[-1] == "POISON_INGESTION":
            window.setCurrentIndex(23)
            
        elif injury_types_selected[-1] == "POISON_CONTACT":
            window.setCurrentIndex(27)
                
        elif injury_types_selected[-1] == "ELECTRIC":
            window.setCurrentIndex(30)
            
        elif injury_types_selected[-1] == "BRUISES":
            window.setCurrentIndex(34)
            
        elif injury_types_selected[-1] == "LACERATION":
            window.setCurrentIndex(35)

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
        window.setCurrentIndex(28)
        
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
        window.setCurrentIndex(window.currentIndex()-1)

class Ui_step_3_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_3_cut, self).__init__()
        loadUi("injuries/cut_step_3.ui", self)
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")
   
        self.cut_step3 = QMovie("GIFs/cuts-3.gif")
        self.gif_player_label_3.setMovie(self.cut_step3)
        self.cut_step3.start()
        
    def next_step(self):
        window.setCurrentIndex(12)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_4_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_4_cut, self).__init__()
        loadUi("injuries/cut_step_4.ui", self)
        self.next_step_button_4.clicked.connect(self.finish_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        
        self.gif_player_label_4 = self.findChild(QLabel, "gif_player_label_4")
   
        self.cut_step4 = QMovie("GIFs/cuts-4.gif")
        self.gif_player_label_4.setMovie(self.cut_step4)
        self.cut_step4.start()
        
    def finish_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
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
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
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
        window.setCurrentIndex(48)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 2
        window.setCurrentIndex(window.currentIndex()-1)
        
        
        
######################  PUNCTURE PROCEDURES STEPS (5 windows TOTAL)  ###################### 

class Ui_degrees_burns(QMainWindow):
    def __init__(self):
        super(Ui_degrees_burns, self).__init__()
        loadUi("injuries/burns_degrees.ui", self)
        self.first_degree_burn.clicked.connect(self.first_degree)
        self.second_degree_burn.clicked.connect(self.second_degree)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        
    def first_degree(self):
        window.setCurrentIndex(19)
        
    def second_degree(self):
        window.setCurrentIndex(38)
    
    def go_back(self):
        window.setCurrentIndex(18)
        
class Ui_before_steps_burns(QMainWindow):
    def __init__(self):
        super(Ui_before_steps_burns, self).__init__()
        loadUi("injuries/burns_before_steps.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("GIFs/1st-burn-cool.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(17)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
        
class Ui_step_1_1st_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_1_1st_burn, self).__init__()
        loadUi("injuries/1st_burns_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
   
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")

        self.burn_step1 = QMovie("GIFs/1st-burns-1.gif")
        self.gif_player_label.setMovie(self.burn_step1)
        self.burn_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(21)
    
    def go_back(self):
        window.setCurrentIndex(17)
        
class Ui_step_2_1st_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_2_1st_burn, self).__init__()
        loadUi("injuries/1st_burns_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(21)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_1st_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_3_1st_burn, self).__init__()
        loadUi("injuries/1st_burns_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")

        self.burn_step3 = QMovie("GIFs/1st-burns-2.gif")
        self.gif_player_label_3.setMovie(self.burn_step3)
        self.burn_step3.start()
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(19)

####################################### 2nd DEGREE BURN ##################################################

class Ui_step_1_2nd_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_1_2nd_burn, self).__init__()
        loadUi("injuries/2nd_burns_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
   
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")

        self.burn_step1 = QMovie("GIFs/2nd-burns-1.gif")
        self.gif_player_label.setMovie(self.burn_step1)
        self.burn_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(40)
    
    def go_back(self):
        window.setCurrentIndex(17)
        
class Ui_step_2_2nd_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_2_2nd_burn, self).__init__()
        loadUi("injuries/2nd_burns_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(40)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_2nd_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_3_2nd_burn, self).__init__()
        loadUi("injuries/2nd_burns_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")

        self.burn_step3 = QMovie("GIFs/2nd-burns-2.gif")
        self.gif_player_label_3.setMovie(self.burn_step3)
        self.burn_step3.start()
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(38)
        
        
        
######################  POISON PROCEDURES STEPS (6 windows TOTAL)  ###################### 
        
class Ui_poison_types(QMainWindow):
    def __init__(self):
        super(Ui_poison_types, self).__init__()
        loadUi("injuries/poison_types.ui", self)
        
        self.inhalation_button.clicked.connect(self.inhalation_steps)
        self.ingestion_button.clicked.connect(self.ingestion_steps)
        self.contact_button.clicked.connect(self.contact_steps)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
    def ingestion_steps(self):
        body_parts_selected.append("MOUTH-SWALLOWED")
        window.setCurrentIndex(23)
        self.save_to_csv()
        self.solenoid_threading()
        
    def inhalation_steps(self):
        body_parts_selected.append("NOSE-INHALED")
        window.setCurrentIndex(26)
        self.save_to_csv()
        self.solenoid_threading()
        
    def contact_steps(self):
        window.setCurrentIndex(1)
    
    def go_back(self):
        window.setCurrentIndex(28)
    
    def solenoid_threading(self):
        x = threading.Thread(target=self.open_close_solenoid)
        x.start()
            
    def open_close_solenoid(self):
        print("CALLED SOLENOID >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON (2)")
            
            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            print("GPIO SOLENOID OPEN")
            GPIO.output(18, 0)
            time.sleep(10)
            print("GPIO SOLENOID CLOSE")
            GPIO.output(18, 1)
            #GPIO.output(18, 1)
            
        else:
            print("SOLENOID FEATURE IS OFF (2)")
            pass 
        
    def save_to_csv(self):
        # Check config file for saving csv (record data)
        if configuration_settings["allow_saving_csv"] == True:
            print("SAVING ALL IN A CSV FILE...")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
            
            print(session)
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            print("CSV FILE WAS NOT CREATED.")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
        
        # Check config file for sending email
        # EMAIL ALSO SENT TO THE NURSE
        if configuration_settings["email_connection"] == True:
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
            
                server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
                server.sendmail("coetmedicalcabinet.2022@gmail.com", configuration_settings["email"], "EMERGENCY RECEIVED FROM THE MEDICAL CABINET!")
            except:
                pass    
        else:
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            if responder_notif[0] == 0:
                print("Will try to connect to to Companion APP")
                self.responder_threading()
                responder_notif.clear()
                responder_notif.append(1)
            else:
                pass
                
        else:
            pass
        
    def responder_threading(self):   
        x = threading.Thread(target=self.send_to_companion_responder)
        x.start()
        
    def send_to_companion_responder(self):                           
        try:
            print("TRYING TO CHECK INTERNET CONNECTION") 
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            time.sleep(3)
            
            print("TRYING TO SEND DATA")
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096
            
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
            
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)

            s = socket.socket()

            s.settimeout(5)
            s.connect((host, port))
            print("[+] Connected.")

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

            #os.remove("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv")
            
            # close the socket
            s.close()

        except:
            
            # VERY IMPORTANT TO ADD THE SESSION TIME IN THIS LIST WHEN IT ERRORS... TRUST ME.
            responder_time.append(session[0])
            
            # UPDATING THE CONFIG FILE ASAP
            with open("config/config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["files_not_sent_responder"].append(responder_time[-1])

            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                print("WRITE TO CONFIG SUCCESS")
                
            print("SEND DATA FAILED")
            print("NO INTERNET CONNECTION")
            check_connection_companion.clear()
            check_connection_companion.append(1)
            #window.setCurrentIndex(41)

            #TKINTER for window if connection to the companion app was failed

            root = Tk()
            root.geometry('800x600')

            def delete_items():
                root.destroy()

            frame1 = Frame(root)
            frame1.configure(bg='gray')
            frame1.pack()

            title = Label(frame1, text = "FAILED!!! TO SEND\nEMERGENCY\nNOTIFICATION", font=("Unispace", 48))
            title.grid(row=0, column=0, pady=(20, 0))

            title_2 = Label(frame1, text = "Please check the Clinic manually\nif the Nurse is PRESENT", font=("Unispace", 28))
            title_2.grid(row=1, column=0, pady=(20, 10))

            button_remove = Button(frame1, text = "CONFIRM", command = delete_items, font=("Unispace", 45, "bold", "underline"))
            button_remove.config(height=1, width=10)
            button_remove.grid(row=2, column=0)

            root.title("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
            root.configure(bg='gray')
            root.mainloop()
            
            return False
        
class Ui_step_1_poison(QMainWindow):
    def __init__(self):
        super(Ui_step_1_poison, self).__init__()
        loadUi("injuries/poison_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        #self.go_back_injury_type.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(24)
    
    def go_back(self):
        body_parts_selected.pop()
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
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_poison_inhalation(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_inhalation, self).__init__()
        loadUi("injuries/poison_inhalation.ui", self)
        
        self.next_step_button_4.clicked.connect(self.next_step)
        #self.go_back_injury_type_4.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        body_parts_selected.pop()
        window.setCurrentIndex(22)
        
class Ui_step_poison_contact(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_contact, self).__init__()
        loadUi("injuries/poison_eye.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        #self.go_back_injury_type.clicked.connect(self.go_back)
        
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.poison_spill_eyes = QMovie("GIFs/poison-spill-1.gif")
        self.gif_player_label.setMovie(self.poison_spill_eyes)
        self.poison_spill_eyes.start()
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        body_parts_selected.pop()
        window.setCurrentIndex(22)


######################  ELECTRIC SHOCK PROCEDURES STEPS (4 windows TOTAL)  ###################### 

class Ui_step_electric_shock_caution(QMainWindow):
    def __init__(self):
        super(Ui_step_electric_shock_caution, self).__init__()
        loadUi("injuries/electric_shock_caution.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(31)
    
    def go_back(self):
        #injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(28)
        
class Ui_step_electric_seek_emergency(QMainWindow):
    def __init__(self):
        super(Ui_step_electric_seek_emergency, self).__init__()
        loadUi("injuries/electric_shock_seek_emergency.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)

class Ui_step_1_electric(QMainWindow):
    def __init__(self):
        super(Ui_step_1_electric, self).__init__()
        loadUi("injuries/electric_shock_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(33)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_2_electric(QMainWindow):
    def __init__(self):
        super(Ui_step_2_electric, self).__init__()
        loadUi("injuries/electric_shock_step_2.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)



######################  BRUISES PROCEDURES STEPS (1 window TOTAL)  ###################### 

class Ui_step_1_bruises(QMainWindow):
    def __init__(self):
        super(Ui_step_1_bruises, self).__init__()
        loadUi("injuries/bruises_step_1.ui", self)

        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.bruises_step1 = QMovie("GIFs/bruise-1.gif")
        self.gif_player_label.setMovie(self.bruises_step1)
        self.bruises_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
        
        
######################  BRUISES PROCEDURES STEPS (1 window TOTAL)  ###################### 

class Ui_step_1_laceration(QMainWindow):
    def __init__(self):
        super(Ui_step_1_laceration, self).__init__()
        loadUi("injuries/laceration_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
    
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.laceration_step1 = QMovie("GIFs/laceration-1.gif")
        self.gif_player_label.setMovie(self.laceration_step1)
        self.laceration_step1.start()
        
    def next_step(self):
        window.setCurrentIndex(36)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
class Ui_step_2_laceration(QMainWindow):
    def __init__(self):
        super(Ui_step_2_laceration, self).__init__()
        loadUi("injuries/laceration_step_2.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.laceration_step2 = QMovie("GIFs/laceration-2.gif")
        self.gif_player_label.setMovie(self.laceration_step2)
        self.laceration_step2.start()
        
    def next_step(self):
        window.setCurrentIndex(37)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_laceration(QMainWindow):
    def __init__(self):
        super(Ui_step_3_laceration, self).__init__()
        loadUi("injuries/laceration_step_3.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.laceration_step3 = QMovie("GIFs/laceration-3.gif")
        self.gif_player_label.setMovie(self.laceration_step3)
        self.laceration_step3.start()
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
        
        
######################################## INJURY SELECTION CONFIRMATION ###############################################
class Ui_bruises_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_bruises_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_bruises_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(1)
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)
        
class Ui_burn_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_burn_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_burn_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(1)
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)
        
class Ui_cut_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_cut_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_cut_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(1)
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)
    
class Ui_electric_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_electric_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_electric_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(28)
        self.save_to_csv()
        
    def save_to_csv(self):
        # Check config file for saving csv (record data)
        if configuration_settings["allow_saving_csv"] == True:
            print("SAVING ALL IN A CSV FILE...")
            session.append(injury_types_selected[-1])
            session.append("FULL BODY")
            
            print(session)
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            print("CSV FILE WAS NOT CREATED.")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
        
        # Check config file for sending email
        # EMAIL ALSO SENT TO THE NURSE
        if configuration_settings["email_connection"] == True:
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
            
                server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
                server.sendmail("coetmedicalcabinet.2022@gmail.com", configuration_settings["email"], "EMERGENCY RECEIVED FROM THE MEDICAL CABINET!")
            except:
                pass    
        else:
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            if responder_notif[0] == 0:
                print("Will try to connect to to Companion APP")
                self.responder_threading()
                responder_notif.clear()
                responder_notif.append(1)
            else:
                pass
                
        else:
            pass
        
    def responder_threading(self):   
        x = threading.Thread(target=self.send_to_companion_responder)
        x.start()
        
    def send_to_companion_responder(self):                           
        try:
            print("TRYING TO CHECK INTERNET CONNECTION") 
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            time.sleep(3)
            
            print("TRYING TO SEND DATA")
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096
            
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
            
            filename = "cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)

            s = socket.socket()

            s.settimeout(5)
            s.connect((host, port))
            print("[+] Connected.")

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

            #os.remove("cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv")
            
            # close the socket
            s.close()

        except:
            
            # VERY IMPORTANT TO ADD THE SESSION TIME IN THIS LIST WHEN IT ERRORS... TRUST ME.
            responder_time.append(session[0])
            
            # UPDATING THE CONFIG FILE ASAP
            with open("config/config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["files_not_sent_responder"].append(responder_time[-1])

            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)
                print("WRITE TO CONFIG SUCCESS")
                
            print("SEND DATA FAILED")
            print("NO INTERNET CONNECTION")
            check_connection_companion.clear()
            check_connection_companion.append(1)
            #window.setCurrentIndex(41)

            #TKINTER for window if connection to the companion app was failed

            root = Tk()
            root.geometry('800x600')

            def delete_items():
                root.destroy()

            frame1 = Frame(root)
            frame1.configure(bg='gray')
            frame1.pack()

            title = Label(frame1, text = "FAILED!!! TO SEND\nEMERGENCY\nNOTIFICATION", font=("Unispace", 48))
            title.grid(row=0, column=0, pady=(20, 0))

            title_2 = Label(frame1, text = "Please check the Clinic manually\nif the Nurse is PRESENT", font=("Unispace", 28))
            title_2.grid(row=1, column=0, pady=(20, 10))

            button_remove = Button(frame1, text = "CONFIRM", command = delete_items, font=("Unispace", 45, "bold", "underline"))
            button_remove.config(height=1, width=10)
            button_remove.grid(row=2, column=0)

            root.title("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
            root.configure(bg='gray')
            root.mainloop()
            
            return False
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)
        
class Ui_laceration_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_laceration_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_laceration_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(1)
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)
        
class Ui_poison_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_poison_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_poison_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(28)
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)
        
class Ui_puncture_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_puncture_confirmation, self).__init__()
        loadUi("confirmation_ui/injury_puncture_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(1)
            
    def go_back_button(self):
        injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(2)


class Ui_final_procedure(QMainWindow):
    def __init__(self):
        super(Ui_final_procedure, self).__init__()
        loadUi("final_procedure.ui", self)
        self.end_procedure_button.clicked.connect(self.reset_program)

    def reset_program(self):
        window.setCurrentIndex(5)


# WINDOW DEBUG
class debug_window_1(QMainWindow):
    def __init__(self):
        super(debug_window_1, self).__init__()
        loadUi("config/debug_tools/debug_window_1.ui", self)
        self.exit_button.clicked.connect(self.exit_window)
        self.confirm_button.clicked.connect(self.login_window)

        self.username = self.findChild(QLineEdit, "user_name")
        self.password = self.findChild(QLineEdit, "pass_word")
        self.password.setEchoMode(QLineEdit.Password)
    
    def login_window(self):
        with open("config/debug_tools/debug_config.json", "r") as data:
            debug_configurations = json.load(data)

        if self.username.text() == debug_configurations["username"] and self.password.text() == debug_configurations["password"]:
            dt = datetime.datetime.now()
            time_now = dt.strftime("%Y-%m-%d %H-%M-%S")

            with open("config/debug_tools/debug_config.json", "r") as data:
                debug_configurations = json.load(data)

            debug_configurations["date"].append(time_now)

            with open("config/debug_tools/debug_config.json", "w") as jsonFile:
                json.dump(debug_configurations, jsonFile)
            print("WRITE TO CONFIG SUCCESS")

            window.setCurrentIndex(51)
        else:
            pass

    def exit_window(self):
        window.setCurrentIndex(0)

class debug_window_2(QMainWindow):
    def __init__(self):
        super(debug_window_2, self).__init__()
        loadUi("config/debug_tools/debug_window_2.ui", self)
        self.continue_button.clicked.connect(self.continue_window)
        self.exit_button.clicked.connect(self.exit_window)

    def continue_window(self):

        window.setCurrentIndex(49)

    def exit_window(self):
        window.setCurrentIndex(0)

class debug_window_3(QMainWindow):
    def __init__(self):
        super(debug_window_3, self).__init__()
        loadUi("config/debug_tools/debug_window_3.ui", self)
        self.confirm_settings.clicked.connect(self.change_configs)
        self.exit_settings.clicked.connect(self.exit_window)
        self.add_whitelist.clicked.connect(self.add_user)
        
        self.scroll_area = self.findChild(QScrollArea, "scrollArea")
        self.scroll = QScroller.scroller(self.scroll_area.viewport())
        self.scroll.grabGesture(self.scrollArea.viewport(), QScroller.LeftMouseButtonGesture)
        self.props = self.scroll.scrollerProperties()
        #self.props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        self.scroll.setScrollerProperties(self.props)

        #
        self.connection_mode_companion = self.findChild(QComboBox, "settings_connection_mode")
        if configuration_settings["connection_mode"] == True:
            self.connection_mode_companion.setCurrentIndex(0)
        elif configuration_settings["connection_mode"] == False:
            self.connection_mode_companion.setCurrentIndex(1)

        #
        self.device_ip = self.findChild(QLineEdit, "settings_device_ip")
        self.device_ip.setText(configuration_settings["companion_app_IP"])

        #
        self.first_port = self.findChild(QSpinBox, "settings_1st_port")
        self.first_port.setValue(configuration_settings["port_1st"])

        #
        self.second_port = self.findChild(QSpinBox, "settings_2nd_port")
        self.second_port.setValue(configuration_settings["port_2nd"])

        #
        self.third_port = self.findChild(QSpinBox, "settings_3rd_port")
        self.third_port.setValue(configuration_settings["port_3rd"])

        #
        self.time_send = self.findChild(QSpinBox, "settings_send_wait_time")
        self.time_send.setValue(configuration_settings["debug_time_send"])

        #
        self.connection_email = self.findChild(QComboBox, "settings_email_connection")
        if configuration_settings["email_connection"] == True:
            self.connection_email.setCurrentIndex(0)
        elif configuration_settings["email_connection"] == False:
            self.connection_email.setCurrentIndex(1)
        
        #
        self.email_receiver = self.findChild(QLineEdit, "settings_email_send")
        self.email_receiver.setText(configuration_settings["email"])

        #
        self.camera_enable = self.findChild(QComboBox, "settings_enable_camera")
        if configuration_settings["enable_camera"] == True:
            self.camera_enable.setCurrentIndex(0)
        elif configuration_settings["enable_camera"] == False:
            self.camera_enable.setCurrentIndex(1)

        #
        self.solenoid_enable = self.findChild(QComboBox, "settings_enable_solenoid")
        if configuration_settings["enable_solenoid"] == True:
            self.solenoid_enable.setCurrentIndex(0)
        elif configuration_settings["enable_solenoid"] == False:
            self.solenoid_enable.setCurrentIndex(1)

        #
        self.csv_saving = self.findChild(QComboBox, "settings_csv_saving")
        if configuration_settings["allow_saving_csv"] == True:
            self.csv_saving.setCurrentIndex(0)
        elif configuration_settings["allow_saving_csv"] == False:
            self.csv_saving.setCurrentIndex(1)

        #
        self.csv_deleting = self.findChild(QComboBox, "settings_csv_deleting")
        if configuration_settings["allow_deleting_csv"] == True:
            self.csv_deleting.setCurrentIndex(0)
        elif configuration_settings["allow_deleting_csv"] == False:
            self.csv_deleting.setCurrentIndex(1)
    
    def change_configs(self):
        print("BUTTON CONNECTED")
        
        with open("config/config.json", "r") as jsonFile:
            data = json.load(jsonFile)

        #########################################################
        if self.connection_mode_companion.currentIndex() == 0:
            data["connection_mode"] = True
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.connection_mode_companion.currentIndex() == 1:
            data["connection_mode"] = False
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.device_ip.text() == "":
            self.device_ip.setFocus()
        
        else:
            data["companion_app_IP"] = str(self.device_ip.text())
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        data["port_1st"] = self.first_port.value()
        
        with open("config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        data["port_2nd"] = self.second_port.value()
        
        with open("config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        data["port_3rd"] = self.third_port.value()
        
        with open("config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        data["debug_time_send"] = self.time_send.value()
        
        with open("config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        if self.connection_email.currentIndex() == 0:
            data["email_connection"] = True
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.connection_email.currentIndex() == 1:
            data["email_connection"] = False
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.email_receiver.text() == "":
            self.email_receiver.setFocus()
        
        else:
            data["email"] = str(self.email_receiver.text())
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.camera_enable.currentIndex() == 0:
            data["enable_camera"] = True
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.camera_enable.currentIndex() == 1:
            data["enable_camera"] = False
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.solenoid_enable.currentIndex() == 0:
            data["enable_solenoid"] = True
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.solenoid_enable.currentIndex() == 1:
            data["enable_solenoid"] = False
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.csv_saving.currentIndex() == 0:
            data["allow_saving_csv"] = True
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.csv_saving.currentIndex() == 1:
            data["allow_saving_csv"] = False
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.csv_deleting.currentIndex() == 0:
            data["allow_deleting_csv"] = True
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.csv_deleting.currentIndex() == 1:
            data["allow_deleting_csv"] = False
        
            with open("config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        window.setCurrentIndex(49)
    
    def add_user(self):
        window.setCurrentIndex(52)

    def exit_window(self):
        window.setCurrentIndex(0)

class debug_window_4(QMainWindow):
    def __init__(self):
        super(debug_window_4, self).__init__()
        loadUi("config/debug_tools/debug_window_4.ui", self)
        self.scan_button.clicked.connect(self.scan_now)
        self.exit_scan.clicked.connect(self.exit_scan_now)

    def scan_now(self):

        if configuration_settings["enable_camera"] == True:
            print("CAMERA IS CONNECTED")
            cap = cv2.VideoCapture(0)
            detector = cv2.QRCodeDetector()

            while True:
                _, img = cap.read()
                data, bbox, _ = detector.detectAndDecode(img)
        
                if(bbox is not None):
                    for i in range(len(bbox)):
                        cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
                        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 250, 120), 2)
                        

                cv2.imshow("Scan QR CODE to CONTINUE", img)

                if data:
                    try:
                        regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                        parsed_text = regexp.findall(data)
                        fullname = str(parsed_text[0]+" "+ parsed_text[1])
                        print("WILL BE ADDED TO WHITELIST")
                        print(fullname)
                        scanned_data.clear()
                        scanned_data.append(parsed_text[0])
                        scanned_data.append(parsed_text[1])
                        cap.release()
                        cv2.destroyAllWindows()
                        self.show_scanned_user()
                        break
                        
                    except:
                        self.error_qr_code()
                        
                        break
                    
                if (cv2.waitKey(1) == ord(".")):
                    scanned_data.append("JR" + " ")
                    scanned_data.append("ANGELO")
                    cap.release()
                    cv2.destroyAllWindows()
                    self.show_scanned_user()
                    break
            
        else:
            pass
        
    def show_scanned_user(self):
        self.whitelist_data = QtWidgets.QMainWindow()
        self.ui = Ui_whitelist_confirm()
        self.ui.setupUi(self.whitelist_data)
        self.whitelist_data.show()
        
        first_name = scanned_data[0]
        last_name = scanned_data[1]
        
        self.ui.name_whitelist.setText(f"<html><head/><body><p align=\"center\">{first_name}{last_name}</p></body></html>")
        
    def error_qr_code(self):
        self.error_whitelist = QtWidgets.QMainWindow()
        self.ui = Ui_whitelist_error()
        self.ui.setupUi(self.error_whitelist)
        self.error_whitelist.show()
    
    def exit_scan_now(self):
        window.setCurrentIndex(49)
        
##################################################################################################################
    
app = QApplication(sys.argv)
window = QtWidgets.QStackedWidget()
window.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
window.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)

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
window.addWidget(Ui_step_1_1st_burn()) # INDEX 19
window.addWidget(Ui_step_2_1st_burn()) # INDEX 20
window.addWidget(Ui_step_3_1st_burn()) # INDEX 21

window.addWidget(Ui_poison_types()) # INDEX 22
window.addWidget(Ui_step_1_poison()) # INDEX 23
window.addWidget(Ui_step_2_poison()) # INDEX 24
window.addWidget(Ui_step_3_poison()) # INDEX 25
window.addWidget(Ui_step_poison_inhalation()) # INDEX 26
window.addWidget(Ui_step_poison_contact()) # INDEX 27

window.addWidget(Ui_before_procedures()) # INDEX 28
window.addWidget(Ui_guest_patient_window()) # INDEX 29

window.addWidget(Ui_step_electric_shock_caution()) # INDEX 30
window.addWidget(Ui_step_electric_seek_emergency()) # INDEX 31
window.addWidget(Ui_step_1_electric()) # INDEX 32
window.addWidget(Ui_step_2_electric()) # INDEX 33

window.addWidget(Ui_step_1_bruises()) # INDEX 34

window.addWidget(Ui_step_1_laceration()) # INDEX 35
window.addWidget(Ui_step_2_laceration()) # INDEX 36
window.addWidget(Ui_step_3_laceration()) # INDEX 37

window.addWidget(Ui_step_1_2nd_burn()) # INDEX 38
window.addWidget(Ui_step_2_2nd_burn()) # INDEX 39
window.addWidget(Ui_step_3_2nd_burn()) # INDEX 40

window.addWidget(Ui_bruises_confirmation()) # INDEX 41
window.addWidget(Ui_burn_confirmation()) # INDEX 42
window.addWidget(Ui_cut_confirmation()) # INDEX 43
window.addWidget(Ui_electric_confirmation()) # INDEX 44
window.addWidget(Ui_laceration_confirmation()) # INDEX 45
window.addWidget(Ui_poison_confirmation()) # INDEX 46
window.addWidget(Ui_puncture_confirmation()) # INDEX 47

window.addWidget(Ui_final_procedure()) # INDEX 48

# DEBUG WINDOWS
window.addWidget(debug_window_1())# INDEX 49
window.addWidget(debug_window_2())# INDEX 50
window.addWidget(debug_window_3())# INDEX 51
window.addWidget(debug_window_4())# INDEX 52
#window.addWidget(debug_window_5())# INDEX 53

#######################  PARAMETERS FOR THE WINDOW (EXACT FOR THE TOUCH SCREEN DISPLAY)  #######################

if __name__ == "__main__":
    window.setWindowTitle("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
    window.setMaximumHeight(600)
    window.setMaximumWidth(1024)
    window.show()
    sys.exit(app.exec_())  