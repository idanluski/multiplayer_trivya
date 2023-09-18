from tkinter import *
import time

def show_lable(j):
    log = Label(entry, text="Login" + "." * (j % 4))
    log.grid(row=3, column=1)

def hold_login():
    j = 1
    log = Label(entry, text="Login" + "." * (j % 4))
    log.grid(row=2, column=1)
    for i in range(7):
        time.sleep(0.5)
        j += 1
        log.config(text ="Login" + "." * (j % 4))

    #Label(entry, text="succes")
    #entry.destroy()
def get_username_detail(ls):
    ls.append(username_entry.get())
    ls.append(password_entry.get())
    #hold_login()
    entry_cliked = False
    print(ls)


global entry_cliked
entry_cliked = True


entry = Tk()
ls_username = []

username = Label(entry,text = "username:")
username.grid(row = 0, column = 0)


username_entry = Entry(entry,borderwidth=5)
username_entry.grid(row=0, column=1)


password = Label(entry,text = "password:")
password.grid(row = 1, column = 0)


password_entry = Entry(entry,borderwidth=5)
password_entry.grid(row = 1, column = 1)



buttun_enter = Button(entry, text= "enter", command=lambda : get_username_detail(ls_username))
Button.grid(buttun_enter,row=2,column=0)





def main_gui():
    while entry_cliked:
        entry.mainloop()
    entry.destroy()


