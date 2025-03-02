import pyautogui
import time

def placement(coord, slot):
    x, y = coord
    pyautogui.press(str(slot))
    time.sleep(0.1)
    pyautogui.moveTo(x,y)
    pyautogui.click(x, y)