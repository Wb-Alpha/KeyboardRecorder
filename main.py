import datetime
import sqlite3
import sys
# from . import MainUI
import threading

from pynput import keyboard, mouse
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import PyQt5
import tkinter as tk


def exitAndSave(root):
    root.destroy()
    global isExit
    isExit = True
    database1 = sqlite3.connect('InputData')
    c = database1.cursor()
    parameter = (datetime.datetime.now().date(), times)
    update = '''insert into keyStatistics (time, count) values (?, ?)'''
    # c.execute(update, parameter)
    print(isExit)


def recordKeyboard(key):
    global times
    times += 1
    global count
    count.config(text=str(times))
    print(times)
    if not isExit:
        return False


def on_click(x, y, button, pressed):
    print("click")


def countKeyboard():
    #该线程由于一直无法结束监听而似乎没有被关闭
    while isExit == False:
        '''with mouse.Listener(
                on_click=on_c   lick) as listener:
            listener.join()'''
        with keyboard.Listener(
                on_release=recordKeyboard) as listener:
            listener.join()


def GUI():
    # ---------------------------临时的GUI，过渡使用--------------------
    root = tk.Tk()
    root.resizable(0, 0)

    mainCanves = tk.Frame(root, height=150, width=250)
    mainCanves.pack()

    label1 = tk.Label(mainCanves, text="已经敲击了")
    label1.grid(row=0, column=0)

    global count
    count = tk.Label(mainCanves, text=str(times))
    count.grid(row=1, column=0)

    label2 = tk.Label(mainCanves, text="次键盘")
    label2.grid(row=2, column=0)

    root.protocol('WM_DELETE_WINDOW', lambda: exitAndSave(root))

    root.mainloop()


if __name__ == "__main__":

    # Store the input times data
    data = {}
    global times
    global isExit
    global count
    isExit = False
    times = 0
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Key.space', 'Key.enter']

    # database
    database = sqlite3.connect('InputData')
    con = database.cursor()


    con.execute('''create table if not exists keyStatistics
                (time varchar(30) primary key,
                count int not null);
                ''')

    sql_datainit = "select count from keyStatistics where ?"
    nowdate = datetime.datetime.now().date()
    times = con.execute(sql_datainit, nowdate)


    # init
    for key in keys:
        data[key] = 0
    t1 = threading.Thread(target=GUI)
    t2 = threading.Thread(target=countKeyboard)

    t1.daemon = True
    t2.daemon = True

    t1.start()
    t2.start()

    t1.join()
