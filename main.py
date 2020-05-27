import sys

from pynput import keyboard, mouse
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
import PyQt5

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

    app = QApplication(sys.argv)

    mainWindow = QWidget()
    mainWindow.resize(250, 150)
    mainWindow.setWindowTitle("KeyboardRecorder")


    mainWindow.show()

    while True:
        '''with mouse.Listener(
                on_click=on_c   lick) as listener:
            listener.join()'''

        with keyboard.Listener(
                on_release=recordKeyboard) as listener:
            listener.join()
    sys.exit(app.exec_())

