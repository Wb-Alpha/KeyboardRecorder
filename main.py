import sys
#from . import MainUI
from pynput import keyboard, mouse
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import PyQt5
import tkinter as tk


def recordKeyboard(key):
    global times
    times += 1
    print(times)


def on_click(x, y, button, pressed):
    print("click")


if __name__ == "__main__":

    # Store the input times data
    data = {}
    global times
    times = 0
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Key.space', 'Key.enter']

    # init
    for key in keys:
        data[key] = 0
    #---------------------------临时的GUI，过渡使用--------------------
    '''root = tk.Tk()
    root.resizable(0, 0)

    mainCanves = tk.Canvas(root, height=150, width=250)
    mainCanves.pack()

    label1 = tk.Label(mainCanves, text="已经敲击了")
    label1.grid(row=0, column=0)

    label2 = tk.Label(mainCanves, text="次键盘")
    label2.grid(row=1, column=0)'''

    while True:
        '''with mouse.Listener(
                on_click=on_c   lick) as listener:
            listener.join()'''

        with keyboard.Listener(
                on_release=recordKeyboard) as listener:
            listener.join()
    root.mainloop()
