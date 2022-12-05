import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

server.login("coetmedicalcabinet.2022@gmail.com", "bovcsjaynaszeels")
server.sendmail("coetmedicalcabinet.2022@gmail.com", "indaya42@gmail.com", "HELLO BADI")