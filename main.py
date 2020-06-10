import datetime
import os
import sqlite3
import sys
import MainUI
import store
import threading
from pynput import keyboard, mouse
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow
import PyQt5
import tkinter as tk


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# 窗口关闭函数
def exitAndSave(root):
    root.destroy()
    global startdate  # 应用启动时的时间
    global kb_times  # 键盘敲击次数
    init_data = store.isExist(startdate)

    if init_data != None:
        store.update(kb_times, startdate)

    else:
        store.insert(kb_times, startdate)


def recordKeyboard(key):
    global kb_times
    global label_kb_count
    kb_times += 1
    label_kb_count.config(text=str(kb_times))
    #print(kb_times)

def recordMouse(x, y):
    global ms_times
    global label_ms_count
    kb_times += 1
    label_ms_count.config(text=str(ms_times))
    print(ms_times)


def on_click(x, y, button, pressed):
    print("click")


def countKeyboard():
    # 该线程由于一直无法结束监听而似乎没有被关闭
    while True:
        with keyboard.Listener(
                on_release=recordKeyboard) as listener:
            listener.join()

def countMouse():
    while True:
        with mouse.Listener(
                on_release=recordMouse) as listener:
            listener.join()


def GUI():
    # ---------------------------临时的GUI，过渡使用--------------------
    root = tk.Tk()
    root.resizable(0, 0)

    mainCanves = tk.Frame(root, height=150, width=250)
    mainCanves.pack()

    label_kb_text = tk.Label(mainCanves, text="今天敲击键盘次数：")
    label_kb_text.grid(row=0, column=0)

    # Label组件
    global label_kb_count
    label_kb_count = tk.Label(mainCanves, text=str(kb_times))
    label_kb_count.grid(row=0, column=1)

    label_ms_text = tk.Label(mainCanves, text="今天敲击鼠标次数:")
    label_ms_text.grid(row=1, column=0)

    global label_ms_count
    label_ms_count = tk.Label(mainCanves, text=str(ms_times))
    label_ms_count.grid(row=1, column=1)



    root.protocol('WM_DELETE_WINDOW', lambda: exitAndSave(root))

    root.mainloop()


if __name__ == "__main__":

    # Store the input times data
    global kb_times
    global ms_times
    global label_kb_count
    isExit = False
    kb_times = 0  # 启动时将键盘敲击次数默认为0
    ms_times = 0  # 启动时将鼠标敲击次数默认为0

    # 如果是初次启动没有数据库表则新建数据库表
    store.initTable()

    # 取得启动时的时间，方便再程序退出的时候保存对应天数的数据
    global startdate
    startdate = datetime.datetime.now().date()

    # 查询当天是否有数据
    init_data = store.isExist(startdate)
    if init_data != None:
        kb_times = init_data['count']

    t1 = threading.Thread(target=GUI)
    t2 = threading.Thread(target=countKeyboard)
    t3 = threading.Thread(target=countMouse)

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True

    t1.start()
    t2.start()
    t3.start()

    t1.join()
