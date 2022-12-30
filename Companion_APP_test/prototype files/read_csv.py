import csv
import mysql.connector
import os
from datetime import datetime
import xlsxwriter

try:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin123",
    database="companion_app"
    )

    mycursor = mydb.cursor()                

except mysql.connector.Error as err:
            print("oopsie poopsie")
      
with open("./sample_data.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      print(row)

date_time = row[0]
r_id = row[1]
rname = row[2]
rcourse = row[3]
p_id = row[4]
pname = row[5]
pcourse = row[6]
pgender = row[7]
injury = row[8]

try:
      sql = "INSERT INTO access_records (date_time, responder_id, responder_name, responder_course, patient_id, patient_name, patient_course, patient_gender, injury) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      value = (date_time, r_id, rname, rcourse, p_id, pname, pcourse, pgender, injury)
      mycursor.execute(sql, value)
      mydb.commit()

except mysql.connector.Error as err:
    print("oopsy daisy")
    

username = os.getlogin()
path = str("C:/Users/" + username)
directory = str(path + '/Documents/Access Records.xlsx')

outWorkBook = xlsxwriter.Workbook(directory)
outsheet = outWorkBook.add_worksheet()

outsheet.write("A1", "Date & Time")
outsheet.write("B1", "Responder ID")
outsheet.write("C1", "Responder Name")
outsheet.write("D1", "Responder Course")
outsheet.write("E1", "Patient ID")
outsheet.write("F1", "Patient Name")
outsheet.write("G1", "Patient Course")
outsheet.write("H1", "Patient Gender")
outsheet.write("J1", "Injury")

mycursor.execute("SELECT * FROM access_records")
result = mycursor.fetchall()

column1 = [item[0] for item in result]
column2 = [item[1] for item in result]
column3 = [item[2] for item in result]
column4 = [item[3] for item in result]
column5 = [item[4] for item in result]
column6 = [item[5] for item in result]
column7 = [item[6] for item in result]
column8 = [item[7] for item in result]
column9 = [item[8] for item in result]

for item in range(len(column1)):
    outsheet.write(item + 1, 0, column1[item])
    outsheet.write(item + 1, 1, column2[item])
    outsheet.write(item + 1, 2, column3[item])
    outsheet.write(item + 1, 3, column4[item])
    outsheet.write(item + 1, 4, column5[item])
    outsheet.write(item + 1, 5, column6[item])
    outsheet.write(item + 1, 6, column7[item])
    outsheet.write(item + 1, 7, column8[item])
    outsheet.write(item + 1, 8, column9[item])

#outsheet.write("J1", "Total Profit")
#outsheet.write("J2", str(total_earnings))

outWorkBook.close()

