from datetime import datetime
import time, re

print("hello world")

#sample_data = "TUPC-18-0516 EDELLON JY BET-COET-C 5514"

sample_data = input("enter student ID:")
key="TUPC-"
key_index = sample_data.find(key)
lkey=int(4)


if key_index < 0:
    print("not valid tupc student ID")
else:
    identifier= sample_data[key_index:key_index+lkey]
    print("key index is:" + str(key_index))
    print("identifier is: " + identifier)
    print("valid TUPC student ID")
    
    regexp=re.compile(r'[a-zA-z0-9_|^&+\-%*/=!>]+')
    sample_text = regexp.findall(sample_data)
    print(sample_text)
    print("CREDENTIALS")
    print(datetime.now())
    print("ID: " + sample_text[0])
    print("NAME: " + sample_text[1] + "," + sample_text[2])
    print("Section: " + sample_text[3] + sample_text[4])