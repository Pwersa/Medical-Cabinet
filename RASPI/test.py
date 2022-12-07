from tkinter import *

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