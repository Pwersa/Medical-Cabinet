#! /usr/bin/env python
import sys, cv2, datetime, time, re, csv, socket, os, threading, subprocess, smtplib, json, shutil
import tqdm
import http.client
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QSpinBox, QMessageBox, QScrollArea, QScroller, \
                                QScrollerProperties, QRadioButton, QLineEdit, QPushButton, QWidget, QComboBox
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie
from pyzbar import pyzbar
from record_session import Ui_record_session
from cabinet_notif import Ui_cabinet_notif
from confirm_name import Ui_whitelist_confirm
from whitelist_error import Ui_whitelist_error
from tkinter import *
from email.mime.text import MIMEText

# DATE AND TIME, RESPONDER ID, NAME, COURSE, PATIENT ID, NAME, 
# COURSE, GENDER, INJURY TYPE (used are also for csv file)
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
scanned_data = []
check_connection_companion = [0]
responder_notif = [0]
camera_on_off = [0]
check_current_index = []
check_current_index_close = []

# OPEN CONFIGURATION FILES AS SOON PROGRAM RUNS (IP ADDRESS, PORT, EMAIL, etc.)
with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "r") as data:
    configuration_settings = json.load(data)

# DEBUG
checked_button = []
restart_button = []

############################ CLASSES ############################

class Ui_scan_qr_code(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_code, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/scan_qr_code.ui", self)
        self.scan_button.clicked.connect(self.camera_scan)
        self.hidden_button.clicked.connect(self.hidden_settings)
        self.restart_button.clicked.connect(self.restart_program)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        
        # ID_Identifier
        id_identify = configuration_settings["id_identifier"]
        # Whitelist
        whitelisted_name = configuration_settings["whitelisted"]
        
        for barcode in barcodes:
            x, y , w, h = barcode.rect

            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            
            if id_identify in barcode_info:
                print(barcode_info)
                print("TUPC ID IS SCANNED")
            
                dt = datetime.datetime.now()
                time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(barcode_info)
                fullname = str(parsed_text[1]+" "+ parsed_text[2])

                # 1st QR CODE RESPONDER of COET
                session.append(str(time_now))
                # ID
                session.append(parsed_text[0])
                # NAME
                session.append(fullname)
                # COURSE
                session.append(parsed_text[-2])
                camera_on_off.append(1)
                print(session)
                
                break
                
            result = any(item in barcode_info for item in whitelisted_name)  
            if result == True:
                print("OTHERS IS SCANNED")
                
                dt = datetime.datetime.now()
                time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(barcode_info)
                fullname = str(parsed_text[0]+" "+ parsed_text[1])
                
                session.append(str(time_now))
                session.append("Teacher")
                session.append(fullname)
                camera_on_off.append(1)
                break
                
        return frame

    def camera_scan(self):
        if configuration_settings["enable_camera"] == True:
            
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()

            while ret:
                ret, frame = camera.read()
                frame = self.read_barcodes(frame)
                cv2.imshow('Barcode/QR code reader', frame)
                
                if camera_on_off[-1] == 1:
                    camera_on_off.clear()
                    camera_on_off.append(0)
                    camera.release()
                    cv2.destroyAllWindows()
                    window.setCurrentIndex(2)
                    break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    camera_on_off.clear()
                    camera_on_off.append(0)
                    dt = datetime.datetime.now()
                    x = dt.strftime("%Y-%m-%d %H-%M-%S")
                    session.append(str(x))
                    # ID
                    session.append("TUPC-RESPONDER")
                    # NAME
                    session.append("JR ANGELO")
                    # COURSE
                    session.append("COET")

                    camera.release()
                    cv2.destroyAllWindows()
                    window.setCurrentIndex(2)
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
            window.setCurrentIndex(50)
            checked_button.clear()
            
        else:
            checked_button.append(1)
            
    def restart_program(self):
        if len(restart_button) >= 5:
            restart_button.clear()
            window.refresh()

        else:
            restart_button.append(1)

class Ui_select_body_part(QMainWindow):
    def __init__(self):
        super(Ui_select_body_part, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/select_body_part.ui", self)
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
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
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
        self.solenoid_threading()

        if configuration_settings["enable_solenoid"] == True:
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
            
        else:
            
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
        x.setDaemon(True)
        x.start()
            
    def open_close_solenoid(self):
        if configuration_settings["enable_solenoid"] == True:

            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22, GPIO.OUT)
            GPIO.output(22, 0)
            time.sleep(1)
            GPIO.output(22, 1)
        
        else:
            pass 
            
    def responder_csv_file(self):
        if configuration_settings["allow_saving_csv"] == True:
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
            
            print(session)
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            print("CSV FILE WAS NOT CREATED.")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
        
        if configuration_settings["email_connection"] == True:
            print("[EMAIL] Sending started.")
            x = threading.Thread(target=self.send_email_notif)
            x.setDaemon(True)
            x.start() 
            
        else:
            pass
        
        self.responder_threading()

    def send_email_notif(self):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
            server.sendmail("coetmedicalcabinet.2022@gmail.com", configuration_settings["email"], "EMERGENCY RECEIVED FROM THE MEDICAL CABINET!")   

        except:
            pass   
        
    def responder_threading(self):   
        x = threading.Thread(target=self.old_send)
        x.setDaemon(True)
        x.start()
        
    def old_send(self):
        try:
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"], timeout=3)                     
            conn.close()
        
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096

            host = configuration_settings["companion_app_IP"]
            port = 4899

            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)
            
            s = socket.socket()
            #s.settimeout(5)
            
            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
            
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
        
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
            
            s.close()
            #os.remove("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv")
            
        except:
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

class Ui_select_injury_type(QMainWindow):
    def __init__(self):
        super(Ui_select_injury_type, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/select_injury_type.ui", self)
        self.cut_button.clicked.connect(lambda: self.injuries(injury_type_selection[0]))
        self.poison_button.clicked.connect(lambda: self.injuries(injury_type_selection[1]))
        self.puncture_button.clicked.connect(lambda: self.injuries(injury_type_selection[2]))
        self.burn_button.clicked.connect(lambda: self.injuries(injury_type_selection[3]))
        self.electric_shock_button.clicked.connect(lambda: self.injuries(injury_type_selection[4]))
        self.bruises_button.clicked.connect(lambda: self.injuries(injury_type_selection[5]))
        self.laceration_button.clicked.connect(lambda: self.injuries(injury_type_selection[6]))
        self.others_button.clicked.connect(lambda: self.injuries(injury_type_selection[7]))
        self.close_button.clicked.connect(self.program_close)

        # Used for hold and drag function
        self.scroll_area = self.findChild(QScrollArea, "scrollArea")
        self.scroll = QScroller.scroller(self.scroll_area.viewport())
        self.scroll.grabGesture(self.scrollArea.viewport(), QScroller.LeftMouseButtonGesture)
        self.props = self.scroll.scrollerProperties()
        self.props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        self.scroll.setScrollerProperties(self.props)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
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

class Ui_enter_injury(QMainWindow):
    def __init__(self):
        super(Ui_enter_injury, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/enter_injury.ui", self)
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
        
        #
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)

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
            
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
            
            input_text.clear()
            window.setCurrentIndex(4)
            
            # VERY IMPORTANT TO ADD THE SESSION TIME... TRUST ME.
            responder_time.append(session[0])
            
            session.clear()

        else:
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            self.enter_injury_threading()
        else:
            pass
        
        window.setCurrentIndex(4)
        
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def enter_injury_threading(self):
        x = threading.Thread(target=self.old_2nd_send)
        x.setDaemon(True)
        x.start()
        
    def old_2nd_send(self):
        try:
            print("TRYING TO CHECK INTERNET CONNECTION") 
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            
            SEPARATOR = "<SEPARATOR>"
            
            BUFFER_SIZE = 4096
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
    
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + responder_time[-1] + ".csv"
            filesize = os.path.getsize(filename)
        
            s = socket.socket()
            #s.settimeout(5)
            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())

            # start sending the file
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
    
                    s.sendall(bytes_read)
                
                    progress.update(len(bytes_read))

            s.close()

        except:
            check_connection_companion.clear()
            check_connection_companion.append(1)

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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/request_nurse.ui", self)
        self.end_procedure_button.clicked.connect(self.reset_program)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)

    def reset_program(self):
        window.setCurrentIndex(0)

class Ui_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_confirmation, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation.ui", self)
        self.no_button.clicked.connect(self.no_confirmation)
        self.yes_button.clicked.connect(self.yes_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)

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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_again.ui", self)
        self.new_injury_button.clicked.connect(self.new_injury)
        self.finish_procedure.clicked.connect(self.done_procedure)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)

    def new_injury(self):
        window.setCurrentIndex(window.currentIndex()-1)
    
    # GOING TO SCAN QR CODE AGAIN BUT FOR THE PATIENT
    def done_procedure(self):
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON (2)")
            
            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            print("GPIO SOLENOID OPEN")
            GPIO.output(18, 0)
            time.sleep(1)
            print("GPIO SOLENOID CLOSE")
            GPIO.output(18, 1)
            #GPIO.output(18, 1)
            
        else:
            print("SOLENOID FEATURE IS OFF (2)")
            pass
        
        window.setCurrentIndex(7)

class Ui_scan_qr_patient(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_patient, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/scan_qr_code_again.ui", self)
        self.guest_patient_window.clicked.connect(self.guest_patient)
        self.scan_qr_patient.clicked.connect(self.camera_scan)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def guest_patient(self):
        
        window.setCurrentIndex(29)
        responder_notif.clear()
        responder_notif.append(0)

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        
        # ID_Identifier
        id_identify = configuration_settings["id_identifier"]
                
        # Whitelist
        whitelisted_name = configuration_settings["whitelisted"]
        
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            #1
            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            #2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            #3
            
            if id_identify in barcode_info:
                print(barcode_info)
                print("TUPC ID IS SCANNED")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(barcode_info)
                fullname = str(parsed_text[1]+" "+ parsed_text[2])
                
                # ID
                session.insert(4, parsed_text[0])
                # NAME
                session.insert(5, fullname)
                # COURSE
                session.insert(6, parsed_text[-2])
                
                camera_on_off.append(1)
                
                break
                
            result = any(item in barcode_info for item in whitelisted_name)  
            if result == True:
                print("OTHERS IS SCANNED")
                
                dt = datetime.datetime.now()
                time_now = dt.strftime("%Y-%m-%d %H-%M-%S")
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(barcode_info)
                fullname = str(parsed_text[0]+" "+ parsed_text[1])
                
                session.append(str(time_now))
                session.append("Teacher")
                session.append(fullname)
                camera_on_off.append(1)
                break
                
        return frame

    def camera_scan(self):
        if configuration_settings["enable_camera"] == True:
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            
            while ret:
                ret, frame = camera.read()
                frame = self.read_barcodes(frame)
                cv2.imshow('Barcode/QR code reader', frame)
                
                if camera_on_off[-1] == 1:
                    camera_on_off.clear()
                    camera_on_off.append(0)
                    camera.release()
                    cv2.destroyAllWindows()
                    window.setCurrentIndex(8)
                    break
                
                if cv2.waitKey(1) & 0xFF == 27:
                    camera_on_off.clear()
                    camera_on_off.append(0)
                    
                    # ID
                    session.append("TUPC-RESPONDER")
                    # NAME
                    session.append("JR ANGELO")
                    # COURSE
                    session.append("COET")

                    camera.release()
                    cv2.destroyAllWindows()
                    window.setCurrentIndex(8)
                    break
            
        else:
            # ID
            session.append("TUPC-RESPONDER")
            # NAME
            session.append("JR ANGELO")
            # COURSE
            session.append("COET")
            window.setCurrentIndex(8)


class Ui_gender_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_gender_patient_window, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/patient_gender.ui", self)
        self.confirm_guest.clicked.connect(self.gender_and_age_submit)
        
        self.age =  self.findChild(QSpinBox, "age_box")
        self.male_radio = self.findChild(QRadioButton, "male_checkbox")
        self.female_radio = self.findChild(QRadioButton, "female_checkbox")
        
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
            
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
        
        window.setCurrentIndex(0)
        self.save_session_tolocal()

    def save_session_tolocal(self):
        
        if configuration_settings["allow_saving_csv"] == True:
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/session/recorded_session" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/session/recorded_session" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
        
        else:
            pass
            
        if configuration_settings["connection_mode"] == True:
            self.session_threading()
        else:
            pass
        
    def session_threading(self):
        x = threading.Thread(target=self.old_send)
        x.setDaemon(True)
        x.start()
    
    def old_send(self):
        try:
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_2nd"], timeout=3)                     
            conn.close()
        
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096 
            host = configuration_settings["companion_app_IP"]
            port = 4799
            
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/session/recorded_session" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)
            
            s = socket.socket()
            #s.settimeout(5)
            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())

            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
             
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
            
            s.close()
            #os.remove("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/session/recorded_session" + " " + session[0] + ".csv")
            session.clear()
    
        except:
            session.clear()
            print("error")
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

######################  CUT PROCEDURES STEPS (4 windows TOTAL)  ###################### 
class Ui_step_1_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_1_cut, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/cut_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/cuts-1.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(10)
    
    def go_back(self):
        window.setCurrentIndex(28)
    
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_2_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_2_cut, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/cut_step_2.ui", self)
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)

        self.gif_player_label_2 = self.findChild(QLabel, "gif_player_label_2")
   
        self.cut_step2 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/cuts-2.gif")
        self.gif_player_label_2.setMovie(self.cut_step2)
        self.cut_step2.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(11)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

class Ui_step_3_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_3_cut, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/cut_step_3.ui", self)
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")
   
        self.cut_step3 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/cuts-3.gif")
        self.gif_player_label_3.setMovie(self.cut_step3)
        self.cut_step3.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(12)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_4_cut(QMainWindow):
    def __init__(self):
        super(Ui_step_4_cut, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/cut_step_4.ui", self)
        self.next_step_button_4.clicked.connect(self.finish_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.gif_player_label_4 = self.findChild(QLabel, "gif_player_label_4")
   
        self.cut_step4 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/cuts-4.gif")
        self.gif_player_label_4.setMovie(self.cut_step4)
        self.cut_step4.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def finish_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

######################  PUNCTURE PROCEDURES STEPS (4 windows TOTAL)  ###################### 
class Ui_step_1_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_1_puncture, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/puncture_before_steps.ui", self)
        
        self.next_step_button_4.clicked.connect(self.next_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_2_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_2_puncture, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/puncture_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/cuts-1.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(15)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_3_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_3_puncture, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/puncture_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)

        self.gif_player_label_2 = self.findChild(QLabel, "gif_player_label_2")
   
        self.cut_step2 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/cuts-2.gif")
        self.gif_player_label_2.setMovie(self.cut_step2)
        self.cut_step2.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(16)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 1
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_4_puncture(QMainWindow):
    def __init__(self):
        super(Ui_step_4_puncture, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/puncture_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 2
        window.setCurrentIndex(window.currentIndex()-1)
        

######################  Ui_degrees_burns PROCEDURES STEPS (5 windows TOTAL)  ###################### 

class Ui_degrees_burns(QMainWindow):
    def __init__(self):
        super(Ui_degrees_burns, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/burns_degrees.ui", self)
        self.first_degree_burn.clicked.connect(self.first_degree)
        self.second_degree_burn.clicked.connect(self.second_degree)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def first_degree(self):
        window.setCurrentIndex(19)
        
    def second_degree(self):
        window.setCurrentIndex(38)
    
    def go_back(self):
        window.setCurrentIndex(18)
        
class Ui_before_steps_burns(QMainWindow):
    def __init__(self):
        super(Ui_before_steps_burns, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/burns_before_steps.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.cut_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/1st-burn-cool.gif")
        self.gif_player_label.setMovie(self.cut_step1)
        self.cut_step1.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(17)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_1_1st_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_1_1st_burn, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/1st_burns_step_1.ui", self)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
   
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")

        self.burn_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/1st-burns-1.gif")
        self.gif_player_label.setMovie(self.burn_step1)
        self.burn_step1.start()
        
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(21)
    
    def go_back(self):
        window.setCurrentIndex(17)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_2_1st_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_2_1st_burn, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/1st_burns_step_2.ui", self)

        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(21)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_3_1st_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_3_1st_burn, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/1st_burns_step_3.ui", self)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")

        self.burn_step3 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/1st-burns-2.gif")
        self.gif_player_label_3.setMovie(self.burn_step3)
        self.burn_step3.start()
        
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(19)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

####################################### 2nd DEGREE BURN ##################################################

class Ui_step_1_2nd_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_1_2nd_burn, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/2nd_burns_step_1.ui", self)
        
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
   
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")

        self.burn_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/2nd-burns-1.gif")
        self.gif_player_label.setMovie(self.burn_step1)
        self.burn_step1.start()
        
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(40)
    
    def go_back(self):
        window.setCurrentIndex(17)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_2_2nd_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_2_2nd_burn, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/2nd_burns_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(40)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_3_2nd_burn(QMainWindow):
    def __init__(self):
        super(Ui_step_3_2nd_burn, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/2nd_burns_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.gif_player_label_3 = self.findChild(QLabel, "gif_player_label_3")

        self.burn_step3 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/2nd-burns-2.gif")
        self.gif_player_label_3.setMovie(self.burn_step3)
        self.burn_step3.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(38)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

######################  POISON PROCEDURES STEPS (6 windows TOTAL)  ###################### 
        
class Ui_poison_types(QMainWindow):
    def __init__(self):
        super(Ui_poison_types, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/poison_types.ui", self)
        
        self.inhalation_button.clicked.connect(self.inhalation_steps)
        self.ingestion_button.clicked.connect(self.ingestion_steps)
        self.contact_button.clicked.connect(self.contact_steps)
        self.go_back_injury_type.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
    def ingestion_steps(self):
        body_parts_selected.append("MOUTH-SWALLOWED")
        window.setCurrentIndex(23)
        self.save_to_csv()
        self.solenoid_threading()
        
        if configuration_settings["enable_solenoid"] == True:
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
            
        else:
            pass 
        
    def inhalation_steps(self):
        body_parts_selected.append("NOSE-INHALED")
        window.setCurrentIndex(26)
        self.save_to_csv()
        self.solenoid_threading()
        
        if configuration_settings["enable_solenoid"] == True:
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
            
        else:
            pass 
        
    def contact_steps(self):
        window.setCurrentIndex(1)
    
    def go_back(self):
        window.setCurrentIndex(28)
    
    def solenoid_threading(self):
        x = threading.Thread(target=self.open_close_solenoid)
        x.setDaemon(True)
        x.start()
            
    def open_close_solenoid(self):
        if configuration_settings["enable_solenoid"] == True:
            
            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(22, GPIO.OUT)
            GPIO.output(22, 0)
            time.sleep(1)
            GPIO.output(22, 1)
            #GPIO.output(18, 1)
            
        else:
            pass 
        
    def save_to_csv(self):
        if configuration_settings["allow_saving_csv"] == True:
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
    
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
        
        if configuration_settings["email_connection"] == True:
            print("[EMAIL] Sending started.")
            x = threading.Thread(target=self.send_email_notif)
            x.setDaemon(True)
            x.start()   
            
        else:
            pass
    
        self.responder_threading()
        
    def send_email_notif(self):
        try:
            print("[EMAIL] Trying to send email...")
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
        
            server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
            server.sendmail("coetmedicalcabinet.2022@gmail.com", configuration_settings["email"], "EMERGENCY RECEIVED FROM THE MEDICAL CABINET!")
            print("EMAIL SENT SUCCESFULLY")

        except:
            print("[EMAIL] Send email unsuccesfully.")
            pass
        
    def responder_threading(self):   
        x = threading.Thread(target=self.old_send_2)
        x.setDaemon(True)
        x.start()
    
    def old_send_2(self):
        try:
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            
            SEPARATOR = "<SEPARATOR>"
            
            BUFFER_SIZE = 4096
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
    
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)
            
            s = socket.socket()
            #s.settimeout(5)
            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())
            
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                     
                        break
                
                    s.sendall(bytes_read)
                
                    progress.update(len(bytes_read))
           
            s.close()
            #os.remove("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv")
            
            
            
        except:
        
            check_connection_companion.clear()
            check_connection_companion.append(1)

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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/poison_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(24)
    
    def go_back(self):
        body_parts_selected.pop()
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_2_poison(QMainWindow):
    def __init__(self):
        super(Ui_step_2_poison, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/poison_step_2.ui", self)
        
        self.next_step_button_2.clicked.connect(self.next_step)
        self.go_back_injury_type_2.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(25)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_3_poison(QMainWindow):
    def __init__(self):
        super(Ui_step_3_poison, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/poison_step_3.ui", self)
        
        self.next_step_button_3.clicked.connect(self.next_step)
        self.go_back_injury_type_3.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_poison_inhalation(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_inhalation, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/poison_inhalation.ui", self)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.next_step_button_4.clicked.connect(self.next_step)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        body_parts_selected.pop()
        window.setCurrentIndex(22)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_poison_contact(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_contact, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/poison_eye.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.poison_spill_eyes = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/poison-spill-1.gif")
        self.gif_player_label.setMovie(self.poison_spill_eyes)
        self.poison_spill_eyes.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        body_parts_selected.pop()
        window.setCurrentIndex(22)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

####################### STEPS UI FOR EVERY INJURIES  #######################

class Ui_before_procedures(QMainWindow):
    def __init__(self):
        super(Ui_before_procedures, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/before_procedures_cautions.ui", self)
        self.goto_steps_button.clicked.connect(self.injuries)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
    
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

################### INFORMATION OF GUEST ###################
class Ui_guest_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_guest_patient_window, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/guest_patient_info.ui", self)
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
        
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)

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
        
        if self.name_info.text() == "":
            pass
        else:
            session.insert(4, "GUEST PATIENT")
            session.insert(5, self.name_info.text())
            session.insert(6, "GUEST")
            
            self.name_info.setText("")
            input_name.clear()
            window.setCurrentIndex(8)

######################  ELECTRIC SHOCK PROCEDURES STEPS (4 windows TOTAL)  ###################### 

class Ui_step_electric_shock_caution(QMainWindow):
    def __init__(self):
        super(Ui_step_electric_shock_caution, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/electric_shock_caution.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(31)
    
    def go_back(self):
        #injury_types_selected.pop()
        print(injury_types_selected)
        window.setCurrentIndex(28)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_electric_seek_emergency(QMainWindow):
    def __init__(self):
        super(Ui_step_electric_seek_emergency, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/electric_shock_seek_emergency.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

class Ui_step_1_electric(QMainWindow):
    def __init__(self):
        super(Ui_step_1_electric, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/electric_shock_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(33)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
       
class Ui_step_2_electric(QMainWindow):
    def __init__(self):
        super(Ui_step_2_electric, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/electric_shock_step_2.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

######################  BRUISES PROCEDURES STEPS (1 window TOTAL)  ###################### 

class Ui_step_1_bruises(QMainWindow):
    def __init__(self):
        super(Ui_step_1_bruises, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/bruises_step_1.ui", self)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)

        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
        # FIND THE LABEL THAT WE NEED TO SET THE GIF
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        # PROPERTIES FOR SETMOVIE
        self.bruises_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/bruise-1.gif")
        self.gif_player_label.setMovie(self.bruises_step1)
        self.bruises_step1.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(28)
    
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

######################  BRUISES PROCEDURES STEPS (1 window TOTAL)  ###################### 

class Ui_step_1_laceration(QMainWindow):
    def __init__(self):
        super(Ui_step_1_laceration, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/laceration_step_1.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
    
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.laceration_step1 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/laceration-1.gif")
        self.gif_player_label.setMovie(self.laceration_step1)
        self.laceration_step1.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(36)
    
    def go_back(self):
        window.setCurrentIndex(28)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_2_laceration(QMainWindow):
    def __init__(self):
        super(Ui_step_2_laceration, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/laceration_step_2.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.laceration_step2 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/laceration-2.gif")
        self.gif_player_label.setMovie(self.laceration_step2)
        self.laceration_step2.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(37)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)
        
class Ui_step_3_laceration(QMainWindow):
    def __init__(self):
        super(Ui_step_3_laceration, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/injuries/laceration_step_3.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        self.end_procedure_now_button.clicked.connect(self.end_session_confirmation)
        
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.laceration_step3 = QMovie("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/GIFs/laceration-3.gif")
        self.gif_player_label.setMovie(self.laceration_step3)
        self.laceration_step3.start()
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def next_step(self):
        window.setCurrentIndex(48)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def end_session_confirmation(self):
        check_current_index.append(window.currentIndex())
        window.setCurrentIndex(53)

####################### INJURY SELECTION CONFIRMATION ###############################################
class Ui_bruises_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_bruises_confirmation, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_bruises_confirmation.ui", self)
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_burn_confirmation.ui", self)
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_cut_confirmation.ui", self)
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_electric_confirmation.ui", self)
        self.sure_button.clicked.connect(self.next_step)
        self.go_back.clicked.connect(self.go_back_button)
        
    def next_step(self):
        window.setCurrentIndex(28)
        self.save_to_csv()
        
    def save_to_csv(self):
        if configuration_settings["allow_saving_csv"] == True:
            print("SAVING ALL IN A CSV FILE...")
            session.append(injury_types_selected[-1])
            session.append("FULL-BODY")
            body_parts_selected.append("FULL-BODY")
            
            print(session)
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            f = open(filename, "w+")
            f.close()
            
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            print("CSV FILE WAS NOT CREATED.")
            session.append(injury_types_selected[-1])
            session.append("FULL-BODY")
            body_parts_selected.append("FULL-BODY")

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
            
        self.responder_threading()
    
    def responder_threading(self):   
        x = threading.Thread(target=self.old_send_2)
        x.setDaemon(True)
        x.start()
        
    def old_send_2(self):
        try:
            conn = http.client.HTTPConnection(configuration_settings["companion_app_IP"], configuration_settings["port_1st"])                     
            conn.close()
            
            SEPARATOR = "<SEPARATOR>"
            
            BUFFER_SIZE = 4096
            host = configuration_settings["companion_app_IP"]
            port = configuration_settings["port_1st"]
        
            filename = "/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv"
            filesize = os.path.getsize(filename)
        
            s = socket.socket()
            #s.settimeout(5)
            print(f"[+] Connecting to {host}:{port}")
            s.connect((host, port))
            print("[+] Connected.")
            s.send(f"{filename}{SEPARATOR}{filesize}".encode())

            # start sending the file
            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "rb") as f:
                while True:
                    
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        
                        break
                
                    s.sendall(bytes_read)
                
    
                    progress.update(len(bytes_read))
 
            s.close()
            #os.remove("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/cabinet-history/responder/recorded_accessed_responder" + " " + session[0] + ".csv")
            
        except:
            check_connection_companion.clear()
            check_connection_companion.append(1)

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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_laceration_confirmation.ui", self)
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_poison_confirmation.ui", self)
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/confirmation_ui/injury_puncture_confirmation.ui", self)
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/final_procedure.ui", self)
        self.end_procedure_button.clicked.connect(self.reset_program)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)

    def reset_program(self):
        window.setCurrentIndex(5)

# WINDOW DEBUG
class debug_window_1(QMainWindow):
    def __init__(self):
        super(debug_window_1, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_window_1.ui", self)
        self.exit_button.clicked.connect(self.exit_window)
        self.confirm_button.clicked.connect(self.login_window)

        self.username = self.findChild(QLineEdit, "user_name")
        self.password = self.findChild(QLineEdit, "pass_word")
        self.password.setEchoMode(QLineEdit.Password)
    
    def login_window(self):
        with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_config.json", "r") as data:
            debug_configurations = json.load(data)

        if self.username.text() == debug_configurations["username"] and self.password.text() == debug_configurations["password"]:
            dt = datetime.datetime.now()
            time_now = dt.strftime("%Y-%m-%d %H-%M-%S")

            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_config.json", "r") as data:
                debug_configurations = json.load(data)

            debug_configurations["date"].append(time_now)

            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_config.json", "w") as jsonFile:
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
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_window_2.ui", self)
        self.continue_button.clicked.connect(self.continue_window)
        self.exit_button.clicked.connect(self.exit_window)

    def continue_window(self):

        window.setCurrentIndex(49)

    def exit_window(self):
        window.setCurrentIndex(0)

class debug_window_3(QMainWindow):
    def __init__(self):
        super(debug_window_3, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_window_3.ui", self)
        self.confirm_settings.clicked.connect(self.change_configs)
        self.exit_settings.clicked.connect(self.exit_window)
        self.add_whitelist.clicked.connect(self.add_user)
        
        self.scroll_area = self.findChild(QScrollArea, "scrollArea")
        self.scroll = QScroller.scroller(self.scroll_area.viewport())
        self.scroll.grabGesture(self.scrollArea.viewport(), QScroller.LeftMouseButtonGesture)
        self.props = self.scroll.scrollerProperties()
        self.props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
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
        
        with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "r") as jsonFile:
            data = json.load(jsonFile)

        #########################################################
        if self.connection_mode_companion.currentIndex() == 0:
            data["connection_mode"] = True
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.connection_mode_companion.currentIndex() == 1:
            data["connection_mode"] = False
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.device_ip.text() == "":
            self.device_ip.setFocus()
        
        else:
            data["companion_app_IP"] = str(self.device_ip.text())
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        data["port_1st"] = self.first_port.value()
        
        with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        data["port_2nd"] = self.second_port.value()
        
        with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        data["port_3rd"] = self.third_port.value()
        
        with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        data["debug_time_send"] = self.time_send.value()
        
        with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
            json.dump(data, jsonFile)

        #########################################################
        if self.connection_email.currentIndex() == 0:
            data["email_connection"] = True
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.connection_email.currentIndex() == 1:
            data["email_connection"] = False
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.email_receiver.text() == "":
            self.email_receiver.setFocus()
        
        else:
            data["email"] = str(self.email_receiver.text())
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.camera_enable.currentIndex() == 0:
            data["enable_camera"] = True
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.camera_enable.currentIndex() == 1:
            data["enable_camera"] = False
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.solenoid_enable.currentIndex() == 0:
            data["enable_solenoid"] = True
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.solenoid_enable.currentIndex() == 1:
            data["enable_solenoid"] = False
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.csv_saving.currentIndex() == 0:
            data["allow_saving_csv"] = True
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.csv_saving.currentIndex() == 1:
            data["allow_saving_csv"] = False
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        #########################################################
        if self.csv_deleting.currentIndex() == 0:
            data["allow_deleting_csv"] = True
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        elif self.csv_deleting.currentIndex() == 1:
            data["allow_deleting_csv"] = False
        
            with open("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/config.json", "w") as jsonFile:
                json.dump(data, jsonFile)

        window.setCurrentIndex(49)
    
    def add_user(self):
        window.setCurrentIndex(52)

    def exit_window(self):
        window.setCurrentIndex(0)

class debug_window_4(QMainWindow):
    def __init__(self):
        super(debug_window_4, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/config/debug_tools/debug_window_4.ui", self)
        self.scan_button.clicked.connect(self.camera_scan)
        self.exit_scan.clicked.connect(self.exit_scan_now)

    def read_barcodes(self, frame):
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            x, y , w, h = barcode.rect

            barcode_info = barcode.data.decode('utf-8')
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            
            try:
                camera_on_off.append(1)
                print(barcode_info)
                print("TUPC ID IS SCANNED")
            
                regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
                parsed_text = regexp.findall(barcode_info)
                fullname = str(parsed_text[0]+" "+ parsed_text[1])
                print("WILL BE ADDED TO WHITELIST")
                print(fullname)
                scanned_data.clear()
                scanned_data.append(parsed_text[0] + " ")
                scanned_data.append(parsed_text[1])

                self.show_scanned_user()
                break
            
            except:
                self.error_qr_code()
                break
                    
                
        return frame

    def camera_scan(self):
        if configuration_settings["enable_camera"] == True:
            
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            
            while ret:
                ret, frame = camera.read()
                frame = self.read_barcodes(frame)
                cv2.imshow('Barcode/QR code reader', frame)
                
                if camera_on_off[-1] == 1:
                    camera_on_off.clear()
                    camera_on_off.append(0)
                    
                    self.show_scanned_user()
                    camera.release()
                    cv2.destroyAllWindows()
                    break
                
                if cv2.waitKey(1) & 0xFF == 27:
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
        
class Ui_end_session_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_end_session_confirmation, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/end_confirmation.ui", self)
        
        self.no_button.clicked.connect(self.no_confirmation_button)
        self.yes_button.clicked.connect(self.yes_confirmation_button)
        self.close_button.clicked.connect(self.program_close)
        
    def program_close(self):
        check_current_index_close.append(window.currentIndex())
        window.setCurrentIndex(54)
        
    def no_confirmation_button(self):
        print("THE CURRENT INDEX", check_current_index)
        window.setCurrentIndex(check_current_index[0])
        check_current_index.clear()
        
    def yes_confirmation_button(self):
        check_current_index.clear()
        window.setCurrentIndex(6)
        
class Ui_close_program_confirmation(QMainWindow):
    def __init__(self):
        super(Ui_close_program_confirmation, self).__init__()
        loadUi("/home/pi/Desktop/Main_Program/RASPI_TEST_BOOT/close_confirmation.ui", self)
        
        self.no_button.clicked.connect(self.no_confirmation_button)
        self.yes_button.clicked.connect(self.yes_confirmation_button)
        
    def no_confirmation_button(self):
        print("THE CURRENT INDEX", check_current_index_close)
        window.setCurrentIndex(check_current_index_close[0])
        check_current_index_close.clear()
        
    def yes_confirmation_button(self):
        check_current_index.clear()
        window.close()

############################ WINDOW PROPERTIES ############################
app = QApplication(sys.argv)
window = QtWidgets.QStackedWidget()
window.setWindowFlag(Qt.FramelessWindowHint)
window.setWindowTitle("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
window.setMaximumHeight(600)
window.setMaximumWidth(1024)

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

window.addWidget(Ui_end_session_confirmation())# INDEX 53
window.addWidget(Ui_close_program_confirmation())# INDEX 54

#######################  PARAMETERS FOR THE WINDOW (EXACT FOR THE TOUCH SCREEN DISPLAY)  #######################

if __name__ == "__main__":
    window.show()
    sys.exit(app.exec_())