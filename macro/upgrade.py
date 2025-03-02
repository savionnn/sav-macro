import pyautogui
import time

def upgrade(coord):
    x, y = coord
    pyautogui.click(x, y)
    time.sleep(0.1)
    pyautogui.press('t')
