
"""Contains code for interacting with the game"""

import numpy as np
import win32gui, win32ui, win32con, win32api, win32process
import time
import ctypes
from send_keys import PressKey, ReleaseKey, Z, L, J
import pyautogui
import cv2

SetFocus = ctypes.windll.user32.SetFocus

forwards_output = [1, 0, 0]
left_output = [0, 1, 0]
right_output = [0, 0, 1]
do_nothing = [0, 0, 0]

button_sleep_time = 0.1


def go_forwards():
    PressKey(Z)
    time.sleep(button_sleep_time)
    ReleaseKey(Z)
    time.sleep(button_sleep_time)


def turn_right():
    PressKey(Z)
    PressKey(L)
    time.sleep(button_sleep_time)
    ReleaseKey(Z)
    ReleaseKey(L)
    time.sleep(button_sleep_time)


def turn_left():
    PressKey(Z)
    PressKey(J)
    time.sleep(button_sleep_time)
    ReleaseKey(Z)
    ReleaseKey(J)
    time.sleep(button_sleep_time)


class Game:

    def __init__(self, window_name, width, height):

        self.WIDTH = width
        self.HEIGHT = height

        try:
            self.hwin = win32gui.FindWindow(None, window_name)

        except Exception as e:
            print(e)

        SetFocus(self.hwin)

        self.keyList = ["\b"]
        for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'£$/\\":
            self.keyList.append(char)

    def get_screen(self):
        """Returns screenshot of the target window.

        Returns:
          img: A screenshot of the area occupied by the target window. Values between 0 and 255.
        """

        rect = win32gui.GetWindowRect(self.hwin)

        left = rect[0]
        right = rect[1]
        width = rect[2] - left
        height = rect[3] - right

        img = np.array(pyautogui.screenshot(region=(left, right, width, height)))

        cv2.rectangle(img, (20, 45), (240, 190), (0, 0, 0), -1)  # This covers 'Lap times'
        cv2.rectangle(img, (680, 45), (760, 120), (0, 0, 0), -1)  # This covers 'Lap count'
        img = cv2.resize(img, (self.WIDTH, self.HEIGHT))

        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # use COLOR_BGR2RGB for colour output

    @staticmethod
    def send_input(input_move):
        """ Takes an input move and executes it by outputting the appropriate key(s).
        Args:
          input_move: The key to be pressed in one hot format.
        """
        choice = np.argmax(input_move)

        if choice == 0:
            print('forwards')
            go_forwards()
        elif choice == 1:
            print('right')
            turn_right()
        elif choice == 2:
            print('left')
            turn_left()
        else:
            print('something happened')

    def key_check(self):
        """Checks for keys that were pressed at the calling of the function.

        Returns:
          keys: keys pressed in string form. e.g 'abcdef'.
        """
        keys = []

        for key in self.keyList:
            if win32api.GetAsyncKeyState(ord(key)):
                keys.append(key)

        return keys

    @staticmethod
    def get_output(keys):
        """Given a string of keys pressed, return the corresponding output.

        Returns:
          output: output in one hot format.
        """
        if 'Z' in keys and 'L' in keys:
            output = right_output
        elif 'Z' in keys and 'J' in keys:
            output = left_output
        elif 'Z' in keys:
            output = forwards_output
        else:
            output = do_nothing

        return output
