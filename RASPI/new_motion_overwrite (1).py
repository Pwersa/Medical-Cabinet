from genericpath import exists
import cv2
import time
import pandas as pd

from datetime import datetime
from sqlalchemy import create_engine
import requests

import base64
static_back = None

motion_list = [None, None]

time = []

video = cv2.VideoCapture(0)

while True:
 
    check, frame = video.read()
    motion = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back = gray
        continue

    diff_frame = cv2.absdiff(static_back, gray)

    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cnts, _ = cv2.findContours(thresh_frame.copy(),
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    motion_list.append(motion)

    motion_list = motion_list[-2:]

    if motion_list[-1] == 1 and motion_list[-2] == 0:
        url = 'http://localhost:3000/time'
           
        result, image = video.read()
        date = datetime.now()
        date2 = "motion_capture " + date.strftime("%m-%d-%Y, %H-%M-%S")
        date3 = date2+".png"

        cv2.imwrite(date3, image)

        with open(date3, "rb") as f:
            png_encoded = base64.b64encode(
                f.read())
            print(png_encoded)

        myobj = {'time_captured': str(
            datetime.now()), 'captured_image': png_encoded}
        requests.post(url, data=myobj)

    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('g'):
        break

video.release()
cv2.destroyAllWindows()