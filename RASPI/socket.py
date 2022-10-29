import sys, cv2, datetime, time, re, csv, socket, tqdm, os
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi     
        
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 # send 4096 bytes each time step

# the ip address or hostname of the server, the receiver
host = "26.98.239.158"
# the port, let's use 5001
port = 4899
# the name of file we want to send, make sure it exists
filename = "pangit_ni_rogie copy.csv"
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