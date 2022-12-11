import sys, cv2, datetime, time, re, csv, socket, tqdm, os, threading, ast, smtplib
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QSpinBox, QMessageBox, QScrollArea, QScroller, \
                                QScrollerProperties, QRadioButton, QLineEdit, QPushButton, QWidget
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QMovie
from record_session import Ui_record_session
from cabinet_notif import Ui_cabinet_notif
from tkinter import *

# OPEN CONFIGURATION FILES AS SOON PROGRAM RUNS (IP ADDRESS, PORT, EMAIL, etc.)
with open("config/config.txt", "r") as data:
    configuration_settings = ast.literal_eval(data.read())

# DATE AND TIME, RESPONDER ID, NAME, COURSE, PATIENT ID, NAME, COURSE, GENDER, INJURY TYPE (used are also for csv file)
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
alphabet = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', "-", "Backspace"], 
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', " "]]

input_text = []
input_name = []
input_section = []

# CSV FILE (DEBUG)
data_qr = []

# Check input Boxes
name_section_focus = ["name"]

# Used for checking if the 1st send (responder) is succesfull, if not, 
# it will send again in the end with the last sending which is session
check_connection_companion = [0]

class Ui_scan_qr_code(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_code, self).__init__()
        loadUi("scan_qr_code.ui", self)
        self.scan_button.clicked.connect(self.qr_camera)
    
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

                if data:
                    dt = datetime.datetime.now()
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
                    
                    # Same situation but for CSV File (DEBUG)
                    #data_qr.append(str(x))
                    #data_qr.append(parsed_text[0])
                    #data_qr.append(fullname)
                    #data_qr.append(parsed_text[-2])

                    time.sleep(0.5)
                    break
                        
                if (cv2.waitKey(1) == ord("r")):
                    time.sleep(0.5)
                    session.append("87897-12-31 23:23:59")
                    # ID
                    session.append("TUPC-RESPONDER")
                    # NAME
                    session.append("JR ANGELO")
                    # COURSE
                    session.append("COET")
                    break

            cap.release()
            cv2.destroyAllWindows()
            window.setCurrentIndex(2)

        else:
            print("CAMERA IS NOT CONNECTED")
            dt = datetime.datetime.now()
            x = dt.strftime("%Y-%m-%d %H:%M:%S")
            session.append(x)
            # ID
            session.append("TUPC-RESPONDER")
            # NAME
            session.append("JR ANGELO")
            # COURSE
            session.append("COET")
            window.setCurrentIndex(2)

class Ui_scan_qr_patient(QMainWindow):
    def __init__(self):
        super(Ui_scan_qr_patient, self).__init__()
        loadUi("scan_qr_code_again.ui", self)
        self.guest_patient_window.clicked.connect(self.guest_patient)
        self.scan_qr_patient.clicked.connect(self.qr_camera)
        
    def guest_patient(self):
        session.append("GUEST")
        window.setCurrentIndex(29)

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
                    session.insert(4, parsed_text[0])
                    # NAME
                    session.insert(5, fullname)
                    # COURSE
                    session.insert(6, parsed_text[-2])
                    # CHECK IF ADDED DATA IN LIST IS CORRECT
                    
                    # Same situation but for CSV File
                    #data_qr.append(4, parsed_text[0])
                    # NAME
                    #data_qr.append(5, fullname)
                    # COURSE
                    #data_qr.append(6, parsed_text[-2])

                    time.sleep(0.5)
                    break
                        
                if (cv2.waitKey(1) == ord("p")):
                    session.insert(4, "TUPC-PATIENT")
                    # NAME
                    session.insert(5, "DURAN ROGIE")
                    # COURSE
                    session.insert(6, "COET")
                    time.sleep(0.5)
                    
                    break

            cap.release()
            cv2.destroyAllWindows()
            window.setCurrentIndex(8)
            
        else:
            print("CAMERA IS NOT CONNECTED")
            dt = datetime.datetime.now()
            x = dt.strftime("%Y-%m-%d %H:%M:%S")
            session.append(x)
            # ID
            session.append("TUPC-RESPONDER")
            # NAME
            session.append("JR ANGELO")
            # COURSE
            session.append("COET")
            window.setCurrentIndex(2)
        
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
        self.props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        self.scroll.setScrollerProperties(self.props)
        
    def injuries(self, injury_type_selection):
        if injury_type_selection == "Cut":
            injury_types_selected.append("CUT") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(1)
            
        elif injury_type_selection == "Poison":
            injury_types_selected.append("POISON") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
        
        elif injury_type_selection == "Puncture":
            injury_types_selected.append("PUNCTURE") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(1)
        
        elif injury_type_selection == "Burn":
            injury_types_selected.append("BURN") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(1)
            
        elif injury_type_selection == "Electric":
            injury_types_selected.append("ELECTRIC") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(1)
            
        elif injury_type_selection == "Bruises":
            injury_types_selected.append("BRUISES") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(1)
            
        elif injury_type_selection == "Laceration":
            injury_types_selected.append("LACERATION") 
            print("Selected injury: " + injury_types_selected[-1])
            window.setCurrentIndex(1)
            
        elif injury_type_selection == "Others":
            print("Selected injury: OTHERS was selected.")
            window.setCurrentIndex(3)
            
class Ui_select_body_part(QMainWindow):
    def __init__(self):
        super(Ui_select_body_part, self).__init__()
        loadUi("select_body_part(beta).ui", self)
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
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Stomach":
            body_parts_selected.append("STOMACH")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
                         
        elif body_parts_list == "Thigh":
            body_parts_selected.append("THIGH")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
                        
        elif body_parts_list == "Crotch":
            body_parts_selected.append("CROTCH")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
                
        elif body_parts_list == "Legs":
            body_parts_selected.append("LEG")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Knee":
            body_parts_selected.append("KNEE")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Foot":
            body_parts_selected.append("FOOT")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Head":
            body_parts_selected.append("HEAD")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Arm":
            print("ARM")
            body_parts_selected.append("ARM")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
            
        elif body_parts_list == "Hand":
            body_parts_selected.append("HAND")
            print("Selected body part was: " + body_parts_selected[-1])
            window.setCurrentIndex(1)
            self.injuries()
    
    def injuries(self):
        # RASPBERRY PI SOLENOID SETTINGS
        # UNLOCK THE CABINET IF IN CONFIG IS TRUE, else no
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON")
                   
            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            GPIO.output(18, 1)
            
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
        
        else:
            print("SOLENOID FEATURE IS OFF")
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()

        if injury_types_selected[-1] == "CUT":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_types_selected[-1] == "POISON_CONTACT":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(27)
            self.responder_csv_file()
        
        elif injury_types_selected[-1] == "PUNCTURE":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
            self.responder_csv_file()
        
        elif injury_types_selected[-1] == "BURN":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
            self.responder_csv_file()
        
        elif injury_types_selected[-1] == "ELECTRIC":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_types_selected[-1] == "BRUISES":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_types_selected[-1] == "LACERATION":
            print("Previous injury was: " + injury_types_selected[-1])
            window.setCurrentIndex(28)
            self.responder_csv_file()
            
        elif injury_type_selection == "Others":
            print("Previous injury was: Others was selected.")
            window.setCurrentIndex(3)
            
        elif injury_type_selection == "Go back to window":
            print("GO BACK A WINDOW")
            window.setCurrentIndex(window.currentIndex()-1) 
            
    def responder_csv_file(self):
        # Check config file for saving csv (record data)
        if configuration_settings["allow_saving_csv"] == True:
            print("SAVING ALL IN A CSV FILE...")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
            
            filename = "cabinet-history/accessed-responder/recorded_accessed_responder.csv"
            f = open(filename, "w+")
            f.close()
            
            with open('cabinet-history/accessed-responder/recorded_accessed_responder.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
                
        else:
            print("CSV FILE WAS NOT CREATED.")
            session.append(injury_types_selected[-1])
            session.append(body_parts_selected[-1])
        
        # Check config file for sending email
        # EMAIL ALSO SENT TO THE NURSE
        if configuration_settings["email_connection"] == True:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
            server.sendmail("coetmedicalcabinet.2022@gmail.com", configuration_settings["email"], "HELLO BADI")
        else:
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            print("Will try to connecto to Companion APP")
            self.responder_threading()
        else:
            pass
        
    def responder_threading(self):   
        x = threading.Thread(target=self.send_to_companion_responder)
        x.start()
        
    def send_to_companion_responder(self):
        try:
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096 # send 4096 bytes each time stepr

            # the ip address or hostname of the server, the receiver
            print("ENTER HOST HERE")
            host = configuration_settings["companion_app_IP"]
            # the port, let's use 5001
            print("ENTER PORT HERE")
            port = configuration_settings["port_1st"]
            # the name of file we want to send, make sure it exists
            filename = "cabinet-history/accessed-responder/recorded_accessed_responder.csv"
            # get the file size
            filesize = os.path.getsize(filename)

            # create the client socket
            s = socket.socket()

            print(f"[+] Connecting to {host}:{port}")
            s.settimeout(5)
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
            
        except:   
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
            print("BACKSPACE")
            check = self.typed_injury.cursorPosition()
            subtract = check - 1
        
            if len(input_text) >= 1:
                input_text.pop(subtract)
                new_string = "".join(input_text)
                print(new_string)
                print(self.typed_injury.cursorPosition())
                self.typed_injury.setText(new_string)
                self.typed_injury.setCursorPosition(subtract)
                self.typed_injury.hasFocus()

            else:
                print("NO MORE ITEMS")
                pass

        elif alphabet == " ":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "1":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "2":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "3":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "4":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "5":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "6":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "7":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "8":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "9":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "0":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)
        
        elif alphabet == "-":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "Q":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "W":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "E":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "R":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "T":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "Y":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "U":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "I":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "O":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "P":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "A":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "S":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "D":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "F":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "G":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "H":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "J":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "K":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "L":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "Z":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "X":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "C":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "V":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "B":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "N":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

        elif alphabet == "M":
            check = self.typed_injury.cursorPosition()
            input_text.insert(check, alphabet)
            new_string = "".join(input_text)
            print("ASDASD" + new_string)

            self.typed_injury.setText(new_string)
            self.typed_injury.setCursorPosition(check + 1)

    def enter_injury(self):
        if configuration_settings["allow_saving_csv"] == True:
            print("Saving typed data to csv file")
            session.append(self.typed_injury.text())
            session.append("Emergency Seek")
            
            filename = "cabinet-history/accessed-responder/recorded_accessed_responder.csv"
            f = open(filename, "w+")
            f.close()
            
            with open('cabinet-history/accessed-responder/recorded_accessed_responder.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
            
            window.setCurrentIndex(4)
            
        else:
            print("Disabled saving typed data to csv file")
            pass
        
        # Check config file if program will connect to the companion app
        if configuration_settings["connection_mode"] == True:
            self.enter_injury_threading()
        else:
            pass
        
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
    def enter_injury_threading(self):
        x = threading.Thread(target=self.send_injury)
        x.start()
    
    def send_injury(self):
        try:
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096 # send 4096 bytes each time stepr

            # the ip address or hostname of the server, the receiver
            print("ENTER HOST HERE")
            host = configuration_settings["companion_app_IP"]
            # the port, let's use 5001
            print("ENTER PORT HERE")
            port = configuration_settings["port_1st"]
            # the name of file we want to send, make sure it exists
            filename = "cabinet-history/accessed-responder/recorded_accessed_responder.csv"
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
            dead = True
            
        except:
            self.send_injury()

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
            window.setCurrentIndex(28)

        elif injury_types_selected[-1] == "POISON_INHALATION":
            print("POISON IS LAST")
            window.setCurrentIndex(26)
            
        elif injury_types_selected[-1] == "POISON_INGESTION":
            print("POISON IS LAST")
            window.setCurrentIndex(23)
            
        elif injury_types_selected[-1] == "POISON_CONTACT":
            print("POISON IS LAST")
            window.setCurrentIndex(27)
            
        elif injury_types_selected[-1] == "PUNCTURE":
            print("PUNCTURE IS LAST")
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "ELECTRIC":
            print("ELECTRIC IS LAST")
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "BRUISES":
            print("BRUISES IS LAST")
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "LACERATION":
            print("BRUISES IS LAST")
            window.setCurrentIndex(28)
            
        elif injury_types_selected[-1] == "BURN":
            print("BURN IS LAST")
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
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON")
                   
            import RPi.GPIO as GPIO

            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            GPIO.output(18, 1)
        
        else:
            print("SOLENOID FEATURE IS OFF")
            pass
        
        window.setCurrentIndex(7)
        
class Ui_guest_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_guest_patient_window, self).__init__()
        loadUi("guest_patient_info.ui", self)
        self.confirm_guest.clicked.connect(self.guest_info)
        
        self.name_info = self.findChild(QLineEdit, "name_info")
        self.section_info = self.findChild(QLineEdit, "section_info")
        
        app.focusChanged.connect(self.on_focusChaned)
        self.name_info.setFocus()

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
        
    def on_focusChaned(self, widget):
        self.lineEditFocused = widget
        
        if widget == self.name_info:
            print("NAME IS FOCUSED")
            name_section_focus.pop()
            name_section_focus.append("name")
            
        elif widget == self.section_info:
            name_section_focus.pop()
            name_section_focus.append("section")

    def input_keyboard(self, alphabet):
        #if self.name_info.focus
        if alphabet == "Backspace":
            print("BACKSPACE")
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
            subtract_1 = check - 1
            subtract_2 = check_cursor_section - 1
            
            if name_section_focus[0] == "name":
                if len(input_name) >= 1:
                    input_name.pop(subtract_1)
                    new_string = "".join(input_name)
                    self.name_info.setText(new_string)
                    self.name_info.setCursorPosition(subtract_1)
                    self.name_info.hasFocus()
                else:
                    pass
                    
            elif name_section_focus[0] == "section":
                if len(input_section) >= 1:
                    input_section.pop(subtract_2)
                    new_string = "".join(input_section)
                    self.section_info.setText(new_string)
                    self.section_info.setCursorPosition(subtract_2)
                    self.section_info.hasFocus()
                else:
                    pass

        elif alphabet == " ":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "1":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "2":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "3":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "4":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "5":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "6":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "7":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "8":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "9":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "0":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)
        
        elif alphabet == "-":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "Q":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "W":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "E":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "R":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "T":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "Y":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "U":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "I":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "O":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "P":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "A":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "S":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "D":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "F":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "G":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "H":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "J":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "K":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "L":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "Z":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "X":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "C":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "V":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "B":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "N":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)

        elif alphabet == "M":
            check = self.name_info.cursorPosition()
            check_cursor_section = self.section_info.cursorPosition()
                
            if name_section_focus[0] == "name":
                input_name.insert(check, alphabet)
                new_string = "".join(input_name)
                print("ASDASD" + new_string)
                self.name_info.setText(new_string)
                self.name_info.setCursorPosition(check + 1)
                
            elif name_section_focus[0] == "section":
                input_section.insert(check_cursor_section, alphabet)
                new_string = "".join(input_section)
                print("ASDASD" + new_string)
                self.section_info.setText(new_string)
                self.section_info.setCursorPosition(check_cursor_section + 1)
        
    def guest_info(self):
        session.insert(5, self.name_info.text())
        session.insert(6, self.section_info.text())
        window.setCurrentIndex(8)
        
class Ui_gender_patient_window(QMainWindow):
    def __init__(self):
        super(Ui_gender_patient_window, self).__init__()
        loadUi("patient_gender.ui", self)
        self.confirm_guest.clicked.connect(self.gender_and_age_submit)
        
        self.age =  self.findChild(QSpinBox, "age_box")
        self.male_radio = self.findChild(QRadioButton, "male_checkbox")
        self.female_radio = self.findChild(QRadioButton, "female_checkbox")
            
    def gender_and_age_submit(self, ):
        if self.male_checkbox.isChecked():
            session.append("MALE")
            session.append(self.age.value())
            self.record_session_window()
        
        elif self.female_checkbox.isChecked():
            session.append("FEMALE")
            session.append(self.age.value())
            self.record_session_window()
        
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

        #self.ui.body_injured.setText(', ' .join(body_parts_selected))
        #self.ui.type_of_injury.setText(', ' .join(injury_types_selected))
        
        # DEBUG DISPLAY ITEMS
        #self.respond = "JR ANGELO IGNACIO INDAYA  -  COET-4A"
        #self.patient = "ROGIE PRINZ DURAN  -  BET-COET-4A"
        #self.date = "1234-44-44"
        #self.body = ["HAND", "HAND"]
        #self.injury = ["CUT", "PUNCTURE"]
        
        self.ui.qr_responder_name.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">{self.respond}</span></p></body><html>")
        self.ui.qr_patient_name.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:600;\">{self.patient}</span></p></body><html>")
        self.ui.date_session.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{self.date}</span></p></body></html>")
        self.ui.body_injured.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{}</span></p></body></html>".format(", ".join(body_parts_selected)))
        self.ui.type_of_injury.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">{}</span></p></body></html>".format(", ".join(injury_types_selected[1:])))
        
        print("SESSION:")
        print(session)
        data_qr.clear()
        
        body_parts_selected.clear()
        injury_types_selected.clear()
        
        window.setCurrentIndex(0)
        self.save_session_tolocal()

    def save_session_tolocal(self):
        
        if configuration_settings["allow_saving_csv"] == True:
            filename = "cabinet-history/session/recorded_session.csv"
            f = open(filename, "w+")
            f.close()
            
            with open('cabinet-history/session/recorded_session.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(session)
        
        else:
            pass
            
        session.clear()
        
        # SEND TO COMPANION APP AFTER SAVING LOCALLY
        # CHECK IF RESPONDER NOTIF FAILED TO SENT, IF YES, IT WILL NOW CONTINUOSLY SEND UNTIL A CONNECTION IS RECEIVED
        if check_connection_companion[-1] == 1:
            print("RESPONDER WAS NOT NOTIFIED")
            self.responder_threading()     
        else:
            print("RESPONDER WAS ALREADY NOTIFIED")
            check_connection_companion.clear()
            #pass
            
        if configuration_settings["connection_mode"] == True:
            self.session_threading()
        else:
            pass
        
    def session_threading(self):
        x = threading.Thread(target=self.send_to_companion)
        x.start()
        
    def send_to_companion(self):
        try:
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096 # send 4096 bytes each time stepr

            # the ip address or hostname of the server, the receiver
            print("ENTER HOST HERE")
            host = configuration_settings["companion_app_IP"]
            # the port, let's use 5001
            print("ENTER PORT HERE")
            port = configuration_settings["port_2nd"]
            # the name of file we want to send, make sure it exists
            filename = "cabinet-history/session/recorded_session.csv"
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
            check_connection_companion.clear()
            dead = True
            
        except:
            self.send_to_companion()
        
    def responder_threading(self):   
        x = threading.Thread(target=self.send_to_companion_responder)
        x.start()
        
    def send_to_companion_responder(self):
        try:
            SEPARATOR = "<SEPARATOR>"
            BUFFER_SIZE = 4096 # send 4096 bytes each time stepr

            # the ip address or hostname of the server, the receiver
            print("ENTER HOST HERE")
            host = configuration_settings["companion_app_IP"]
            # the port, let's use 5001
            print("ENTER PORT HERE")
            port = configuration_settings["port_1st"]
            # the name of file we want to send, make sure it exists
            filename = "cabinet-history/accessed-responder/recorded_accessed_responder.csv"
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
            
            
        except:
            self.send_to_companion_responder()      
        
        
####################### STEPS UI FOR EVERY INJURIES  #######################

class Ui_before_procedures(QMainWindow):
    def __init__(self):
        super(Ui_before_procedures, self).__init__()
        loadUi("injuries/before_procedures_cautions.ui", self)
        self.goto_steps_button.clicked.connect(self.injuries)
        self.go_back_button.clicked.connect(self.go_back)
        
    def injuries(self):
        if injury_types_selected[-1] == "CUT":
            print(injury_types_selected[-1])
            window.setCurrentIndex(9)
        
        elif injury_types_selected[-1] == "PUNCTURE":
            print(injury_types_selected[-1])
            window.setCurrentIndex(13)

        elif injury_types_selected[-1] == "BURN":
            print(injury_types_selected[-1])
            window.setCurrentIndex(18)
            
        elif "POISON" in injury_types_selected: 
            print("POISON IN LIST")
            print(injury_types_selected[-1])
            window.setCurrentIndex(22)
            
        elif injury_types_selected[-1] == "POISON_INHALATION":
            print("POISON IS LAST")
            window.setCurrentIndex(26)
            
        elif injury_types_selected[-1] == "POISON_INGESTION":
            print("POISON IS LAST")
            window.setCurrentIndex(23)
            
        elif injury_types_selected[-1] == "POISON_CONTACT":
            print("POISON IS LAST")
            window.setCurrentIndex(27)
                
        elif injury_types_selected[-1] == "ELECTRIC":
            print(injury_types_selected[-1])
            window.setCurrentIndex(30)
            
        elif injury_types_selected[-1] == "BRUISES":
            print(injury_types_selected[-1])
            window.setCurrentIndex(34)
            
        elif injury_types_selected[-1] == "LACERATION":
            print(injury_types_selected[-1])
            window.setCurrentIndex(35)
            
    def go_back(self):
        # GO BACK A WINDOW WHICH IS STEP 2
        window.setCurrentIndex(2)
        
        

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
        window.setCurrentIndex(5)
    
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
        window.setCurrentIndex(5)
    
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
        window.setCurrentIndex(5)
    
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
        window.setCurrentIndex(5)
    
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
        window.setCurrentIndex(5)
    
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
        
    def inhalation_steps(self):
        body_parts_selected.append("NOSE")
        injury_types_selected.append("POISON_INHALATION")
        print("NOSE")
        window.setCurrentIndex(26)
    
    def ingestion_steps(self):
        body_parts_selected.append("MOUTH")
        injury_types_selected.append("POISON_INGESTION")
        window.setCurrentIndex(23)
    
    def contact_steps(self):
        injury_types_selected.append("POISON_CONTACT")
        window.setCurrentIndex(1)
    
    def go_back(self):
        window.setCurrentIndex(2)
        
    def solenoid_poison(self):
        if configuration_settings["enable_solenoid"] == True:
            print("SOLENOID FEATURE IS ON")
                   
            import RPi.GPIO as GPIO
            
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(18, GPIO.OUT)
            GPIO.output(18, 1)
            
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
        
        else:
            print("SOLENOID FEATURE IS OFF")
            self.cabinet_notif = QtWidgets.QMainWindow()
            self.ui = Ui_cabinet_notif()
            self.ui.setupUi(self.cabinet_notif)
            self.cabinet_notif.show()
        
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
        window.setCurrentIndex(5)
    
    def go_back(self):
        window.setCurrentIndex(window.currentIndex()-1)
        
class Ui_step_poison_inhalation(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_inhalation, self).__init__()
        loadUi("injuries/poison_inhalation.ui", self)
        
        self.next_step_button_4.clicked.connect(self.next_step)
        self.go_back_injury_type_4.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(5)
    
    def go_back(self):
        window.setCurrentIndex(22)
        
class Ui_step_poison_contact(QMainWindow):
    def __init__(self):
        super(Ui_step_poison_contact, self).__init__()
        loadUi("injuries/poison_eye.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_injury_type.clicked.connect(self.go_back)
        
        self.gif_player_label = self.findChild(QLabel, "gif_player_label")
        
        self.poison_spill_eyes = QMovie("GIFs/poison-spill-1.gif")
        self.gif_player_label.setMovie(self.poison_spill_eyes)
        self.poison_spill_eyes.start()
        
    def next_step(self):
        window.setCurrentIndex(5)
    
    def go_back(self):
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
        window.setCurrentIndex(28)
        
class Ui_step_electric_seek_emergency(QMainWindow):
    def __init__(self):
        super(Ui_step_electric_seek_emergency, self).__init__()
        loadUi("injuries/electric_shock_seek_emergency.ui", self)
        self.next_step_button.clicked.connect(self.next_step)
        self.go_back_button.clicked.connect(self.go_back)
        
    def next_step(self):
        window.setCurrentIndex(5)
    
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
        window.setCurrentIndex(5)
    
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
        window.setCurrentIndex(5)
    
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


#######################  PARAMETERS FOR THE WINDOW (EXACT FOR THE TOUCH SCREEN DISPLAY)  #######################

if __name__ == "__main__":
    window.setWindowTitle("Interactive First Aid Cabinet - BET COET 4A - Build 2022")
    window.setMaximumHeight(600)
    window.setMaximumWidth(1024)
    window.show()
    sys.exit(app.exec_())