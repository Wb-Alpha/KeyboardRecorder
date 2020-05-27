import sys
#from . import MainUI
import threading

from pynput import keyboard, mouse
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import PyQt5
import tkinter as tk


def recordKeyboard(key):
    global times
    times += 1
    global count
    count.config(text = str(times))
    print(times)


def on_click(x, y, button, pressed):
    print("click")


def countKeyboard():
    while True:
        '''with mouse.Listener(
                on_click=on_c   lick) as listener:
            listener.join()'''

        with keyboard.Listener(
                on_release=recordKeyboard) as listener:
            listener.join()


def GUI():
    #---------------------------临时的GUI，过渡使用--------------------
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


    root.mainloop()




if __name__ == "__main__":

    # Store the input times data
    data = {}
    global times
    global count
    times = 0
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Key.space', 'Key.enter']

    # init
    for key in keys:
        data[key] = 0
    t1 = threading.Thread(target=GUI)
    t2 = threading.Thread(target=countKeyboard)
    t1.start()
    t2.start()
    


