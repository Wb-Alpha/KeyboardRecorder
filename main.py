import datetime
import os
import sqlite3
import sys
import store
import threading
from pynput import keyboard, mouse
import tkinter as tk


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# 窗口关闭函数
def exitAndSave(root):
    root.destroy()
    global start_date  # 应用启动时的时间
    global kb_count  # 键盘敲击次数
    init_data = store.isExist(start_date)

    if init_data != None:
        store.update(start_date, kb_count, ms_count)

    else:
        store.insert(start_date, kb_count, ms_count)


def recordKeyboard(key):
    global kb_count
    global label_kb_count
    kb_count += 1
    label_kb_count.config(text=str(kb_count))
    # print(kb_times)


def recordMouse(x, y, button, pressed):
    global ms_count
    global label_ms_count
    global state
    if state:
        ms_count += 1
        label_ms_count.config(text=str(ms_count))
        print(ms_count)
    state = not state  # 改变状态


def countKeyboard():
    # 该线程由于一直无法结束监听而似乎没有被关闭
    while True:
        with keyboard.Listener(
                on_release=recordKeyboard) as listener:
            listener.join()


def countMouse():
    # 由于这个组件按一次鼠标会默认记录为点击两次，这会导致鼠标计数变成
    # 原来的两倍，故我们设定一个布尔型的状态变量，每记录到一次点击就改变
    # 一次状态，仅当True的时候会计数，这样子就可以恢复正常
    # 初始化鼠标计数状态
    global state
    state = True
    while True:
        with mouse.Listener(
                on_click=recordMouse) as listener:
            listener.join()


def GUI():
    # ---------------------------临时的GUI，过渡使用--------------------
    root = tk.Tk()
    root.resizable(0, 0)
    root.geometry('170x100')

    mainCanves = tk.Frame(root, height=150, width=250)
    mainCanves.pack()

    label_kb_text = tk.Label(mainCanves, text="今天敲击键盘次数：")
    label_kb_text.place(relx=0, rely=0.1, anchor="nw")

    # Label组件
    global label_kb_count
    label_kb_count = tk.Label(mainCanves, text=str(kb_count))
    label_kb_count.place(relx=0.7, rely=0.1, anchor="nw")

    label_ms_text = tk.Label(mainCanves, text="今天敲击鼠标次数:")
    label_ms_text.place(x=0, rely=0.3, anchor="nw")

    global label_ms_count
    label_ms_count = tk.Label(mainCanves, text=str(ms_count))
    label_ms_count.place(relx=0.7, rely=0.3, anchor="nw")

    img_png = tk.PhotoImage(file='img/setting1.png')
    button_setting = tk.Button(mainCanves, image=img_png)
    button_setting.place(relx=0.7, rely=0.8, anchor="nw")

    root.protocol('WM_DELETE_WINDOW', lambda: exitAndSave(root))

    root.mainloop()


if __name__ == "__main__":

    # Store the input times data
    global kb_count
    global ms_count
    global label_kb_count
    isExit = False
    kb_count = 0  # 启动时将键盘敲击次数默认为0
    ms_count = 0  # 启动时将鼠标敲击次数默认为0

    # 如果是初次启动没有数据库表则新建数据库表
    store.initTable()

    # 取得启动时的时间，方便再程序退出的时候保存对应天数的数据
    global start_date
    start_date = datetime.datetime.now().date()

    # 查询当天是否有数据
    init_data = store.isExist(start_date)
    if init_data is not None:
        kb_count = init_data['kb_count']
        ms_count = init_data['ms_count']

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
