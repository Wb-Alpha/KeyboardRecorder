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

class MyMainForm(QMainWindow, MainUI.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def exitAndSave(root):
    root.destroy()
    '''
    database1 = sqlite3.connect('InputData')
    database1.row_factory = dict_factory
    c = database1.cursor()
    sql_datainit = "select count from keyStatistics where time=?"
    
    lasttime = c.execute(sql_datainit, (nowdate, ))
    init_data = lasttime.fetchone()'''
    global nowdate
    init_data = store.isExist(nowdate)

    if init_data != None:
        store.update(count, nowdate)
        '''
        update = "update keyStatistics set count=? where time=?"
        parameter = (times, datetime.datetime.now().date())
        c.execute(update, parameter)
        '''
    else:
        store.insert(count, nowdate)
        '''
        parameter = (datetime.datetime.now().date(), times)
        update = "insert into keyStatistics (time, count) values (?, ?)"
        c.execute(update, parameter)
        '''



def recordKeyboard(key):
    global times
    times += 1
    global count
    count.config(text=str(times))
    print(times)



def on_click(x, y, button, pressed):
    print("click")


def countKeyboard():
    #该线程由于一直无法结束监听而似乎没有被关闭
    while True:
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
    global count
    isExit = False
    times = 0
    keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'Key.space', 'Key.enter']

    # database
    database = sqlite3.connect('InputData')
    database.row_factory = dict_factory
    con = database.cursor()

    #如果是初次启动没有数据库表则新建数据库表
    store.initTable()

    #取得启动时的时间，方便再程序退出的时候保存对应天数的数据
    global nowdate
    nowdate = datetime.datetime.now().date()

    # 查询当天是否有数据
    init_data = store.isExist(nowdate)
    if init_data != None:
        times = init_data['count']

    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()

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

