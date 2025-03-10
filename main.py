from macro import upgrade, coordinate, placement
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pynput import keyboard
import pyautogui
import threading

unitsBool = [False,False,False,False,False,False]
units = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6)]
unitSlots = [1,1,1,1,1,1]
unitActions = ["Place & Upgrade","Place & Upgrade","Place & Upgrade","Place & Upgrade","Place & Upgrade","Place & Upgrade"]
unitUpgrades = [0,0,0,0,0,0]
unitPrices = [1000,1000,1000,1000,1000,1000]
labels = []
entries = []
combo_boxes_slot = []
combo_boxes_action = []
combo_boxes_upgrade = []

def selectUnit(unit):
    unitsBool[unit] = not unitsBool[unit]

def selectCoordinate(unit):
    units[unit] = coordinate.coordinate()
    labels[unit].config(text='X: {} Y: {}'.format(int(units[unit][0]),int(units[unit][1])), font=("Arial", 8))

def selectSlot(event, unit):
    slot = combo_boxes_slot[unit].get()
    unitSlots[unit] = slot

def selectSlotAction(event, unit):
    slot = combo_boxes_action[unit].get()
    unitActions[unit] = slot

def selectSlotUpgrade(event, unit):
    slot = combo_boxes_upgrade[unit].get()
    unitUpgrades[unit] = slot

root = tk.Tk()
root.title("AV Macro")
root.geometry("314x450+900+0")
root.minsize(314,500)

style = ttk.Style()

root.tk.call("source", "./ttk_theme/azure.tcl")  
root.tk.call("set_theme", "dark")

style.configure(
    "Custom.TButton",  
    foreground="white", 
    background="#444444", 
    font=("Arial",10),
    padding=0
)

canvas = tk.Canvas(root, width=314, height=360)
canvas.place(x=0,y=0)
canvas.create_line(102, 0, 102, 360, width=1)  
canvas.create_line(209, 0, 209, 360, width=1) 
canvas.create_line(-3, 179, 314, 179, width=1) 
canvas.create_line(-3, 360, 314, 360, width=1) 
canvas.tag_lower("lines")
for i in range(6):
    Checkbutton(root,text="Unit {}".format(i+1),font=("Arial", 10),command=lambda i=i: selectUnit(i)).place(x=i%3*106, y=i//3*181, width=100, height=25)
    Label(root,text="Slot:".format(i+1),font=("Arial", 10)).place(x=i%3*106, y=i//3*181+25, width=50, height=25)
    combo_box = ttk.Combobox(root,font=("Arial",10), values=[1,2,3,4,5,6], width=6, state="readonly", takefocus=0)
    combo_box.place(x=i%3*106+45, y=i//3*181+25, height=25)
    combo_box.set(1)
    combo_box.bind("<<ComboboxSelected>>", lambda event,i=i: selectSlot(event,i))
    combo_boxes_slot.append(combo_box)

    Label(root,text="Action: ".format(i+1),font=("Arial", 10)).place(x=i%3*106, y=i//3*181+55, width=50, height=25)
    combo_box_action = ttk.Combobox(root,font=("Arial",10), values=["Place & Upgrade","Upgrade"], width=6, state="readonly", takefocus=0)
    combo_box_action.place(x=i%3*106+45, y=i//3*181+55, height=25)
    combo_box_action.set("Place & Upgrade")
    combo_box_action.bind("<<ComboboxSelected>>", lambda event,i=i: selectSlotAction(event,i))
    combo_boxes_action.append(combo_box_action)

    Label(root,text="Upgrade: ".format(i+1),font=("Arial", 10)).place(x=i%3*106, y=i//3*181+85, width=50, height=25)
    combo_box_upgrade = ttk.Combobox(root,font=("Arial",10), values=[0,1,2,3,4,5,6,7,8,9,10,"MAX"], width=6, state="readonly", takefocus=0)
    combo_box_upgrade.place(x=i%3*106+45, y=i//3*181+85, height=25)
    combo_box_upgrade.set(0)
    combo_box_upgrade.bind("<<ComboboxSelected>>", lambda event,i=i: selectSlotUpgrade(event,i))
    combo_boxes_upgrade.append(combo_box_upgrade)

    button = ttk.Button(root, text="Select Coordinates", style="Custom.TButton", command=lambda i=i: selectCoordinate(i), takefocus=0)
    button.place(x=i%3*106, y=i//3*181+125, width=100, height=25)
    label = Label(root, text='X: {} Y: {}'.format(int(units[i][0]),int(units[i][1])), font=("Arial", 10))
    label.place(x=i%3*106, y=i//3*181+150, width=100, height=25)
    labels.append(label)

    labelPrice = Label(root, text=f"Slot {i+1}: ")
    labelPrice.place(x=i%3*100+10,y=i//3*20+400)
    entryPrice = Entry(root)
    entryPrice.place(x=i%3*100+45,y=i//3*20+400,width=60, height=20)
    entryPrice.insert(0,"1000")
    entries.append(entryPrice)
    
Label(root, text="Enter slot prices:",font=("Arial", 10)).place(x=10,y=380)
Label(root, text="Start Macro: F1",font=("Arial", 10)).place(x=10,y=450)
Label(root, text="Stop Macro: F3",font=("Arial", 10)).place(x=10,y=470)

def save_entries():
    for i in range(len(entries)):
        unitPrices[i] = (entries[i].get())

macro_active = False

def startMacro():
    global upgradeLvl
    global macro_active
    global cash
    pyautogui.moveTo(410,160)
    time.sleep(0.1)
    pyautogui.leftClick()
    while cash == 0:
        pyautogui.leftClick()
        time.sleep(0.1)
    save_entries()
    time.sleep(2)
    cash = 0
    for i in range(len(unitsBool)):
        if unitsBool[i]:
            if unitActions[i] == "Place & Upgrade":
                print(f"price: {unitPrices[int(unitSlots[i])-1]}")
                print(f"cash: {cash}")
                while int(unitPrices[int(unitSlots[i])-1]) > int(cash):
                    if not macro_active:
                        return
                    time.sleep(0.1)
                placement.placement(units[i],unitSlots[i])
                time.sleep(2)
                while str(unitUpgrades[i]) != upgradeLvl:
                    if not macro_active:
                        return
                    upgrade.upgrade(units[i])
                    currentUpgrade()
                    time.sleep(2)
                pyautogui.moveTo(310, 373)
                pyautogui.leftClick()
            else:
                while str(unitUpgrades[i]) != upgradeLvl:
                    if not macro_active:
                        return
                    upgrade.upgrade(units[i])
                    currentUpgrade()
                    time.sleep(2)
                pyautogui.moveTo(310, 373)
                pyautogui.leftClick()
            time.sleep(2)
        upgradeLvl = "0"
    return

def on_press(key):
    global macro_active
    if key == keyboard.Key.f1:
        print("Start Macro triggered!")
        macro_active = True
        macro_thread = threading.Thread(target=startMacro, daemon=True)
        macro_thread.start()
    elif key == keyboard.Key.f3:
        macro_active = False
        print("Stop Macro triggered!")

import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)
old_wave = ""
total_wave= ""
cash = 0
upgradeLvl = "0"

def waveRead():
    global old_wave
    global total_wave
    global macro_active
    while True:
        try:
            screenshot = pyautogui.screenshot(region=(223, 50, 110, 20))
            screenshot_array = np.array(screenshot)
            result = reader.readtext(screenshot_array, detail=0,allowlist="Wave0123456789/")
            if result:
                text = result[0]
                if "Wave" in text and "/" in text:
                    try: 
                        wave_part = text.split()[1]
                    except:
                        wave_part = text[4:]
                    if wave_part[0] == "/":
                        wave_part = wave_part[1:]
                    print(wave_part)
                    try:
                        total_wave = wave_part.split("/")[1]
                        current_wave = wave_part.split("/")[0]
                    except:
                        print(f"wave read failed: {text}")
                    if current_wave != old_wave:
                        print(f"New wave detected: {current_wave}")
                        print(total_wave)
                        old_wave = current_wave
            elif old_wave == total_wave:
                gameResult()
                pyautogui.moveTo(450,450)
                time.sleep(0.1)
                pyautogui.click(button='left', clicks=10, interval=0.50,)
            gameResult()
            time.sleep(10)
        except Exception as e:
            print(e)

def gameResult():
    global macro_active
    global old_wave
    global cash
    victoryScreenshot = pyautogui.screenshot(region=(250, 314, 140, 30))
    victoryScreenshot_array = np.array(victoryScreenshot)
    victoryResult = reader.readtext(victoryScreenshot_array, detail=0)
    if victoryResult:
        print(victoryResult[0])
        if "VICTORY" in victoryResult[0]:
            print("Victory")
            macro_active = False
            time.sleep(5)
            pyautogui.moveTo(557,606)
            time.sleep(0.1)
            pyautogui.leftClick()
            macro_active = True
            macro_thread = threading.Thread(target=startMacro, daemon=True)
            macro_thread.start()
            old_wave = ""
            cash = 0
        elif "FAIL" in victoryResult[0]:
            print("Failed")
            macro_active = False
            time.sleep(5)
            pyautogui.moveTo(557,606)
            time.sleep(0.1)
            pyautogui.leftClick()
            macro_active = True
            macro_thread = threading.Thread(target=startMacro, daemon=True)
            macro_thread.start()
            old_wave = ""
            cash = 0

def is_one_digit_apart(a: str, b: str) -> bool:
    if a == b:
        return False  
    len_diff = abs(len(a) - len(b))
    if len_diff == 1:
        if len(a) < len(b):
            a, b = b, a  
        for i in range(len(a)):
            if a[:i] + a[i+1:] == b:
                return True
    elif len_diff == 0:
        mismatch_count = sum(1 for x, y in zip(a, b) if x != y)
        if mismatch_count == 1:
            return True
    return False

def currentMoney():
    global cash
    previous_monies = []
    newcash = 0
    while True:
        try:
            screenshot = pyautogui.screenshot(region=(400, 785, 100, 25))
            screenshot_array = np.array(screenshot)
            result = reader.readtext(screenshot_array, detail=0, allowlist="0123456789Yy,.")
            if result:
                text = result[0]
                print(f"raw: {text}")
                text = text.lower()
                if "," in text:
                    hundres = text.split(",")[1]
                    if len(hundres) == 3:
                        text = "".join(text.split(","))
                        text = text[:-1]
                        if text.isnumeric():
                            previous_monies.append(text)
                            if len(previous_monies) > 5:
                                previous_monies.pop(0)
                            if len(previous_monies) > 1:
                                for prev in previous_monies[:-1]:  # Compare with previous reads
                                    if is_one_digit_apart(prev, text):
                                        newcash = min(prev, text, key=int)
                                        break
                                if newcash:
                                    if cash == 0:
                                        if newcash == 600:
                                            cash = newcash
                                            print(cash)
                                    else:
                                        cash = newcash
                                        print(cash)
                                else:
                                    if cash == 0:
                                        if text == "600":
                                            cash = int(text)
                                            print(cash)
                                    else:
                                        cash = int(text)
                                        print(cash)
                    elif len(hundres) != 4:
                        print("not valid read")
                    else:
                        text = "".join(text.split(","))
                        text = text[:-1]
                        if text.isnumeric():
                            previous_monies.append(text)
                            if len(previous_monies) > 5:
                                previous_monies.pop(0)
                            if len(previous_monies) > 1:
                                for prev in previous_monies[:-1]:  # Compare with previous reads
                                    if is_one_digit_apart(prev, text):
                                        newcash = min(prev, text, key=int)
                                        break
                                if newcash:
                                    if cash == 0:
                                        if newcash == 600:
                                            cash = newcash
                                            print(cash)
                                    else:
                                        cash = newcash
                                        print(cash)
                                else:
                                    if cash == 0:
                                        if text == "600":
                                            cash = int(text)
                                            print(cash)
                                    else:
                                        cash = int(text)
                                        print(cash)
                else:
                    text = text[:-1]
                    print(text)
                    if text.isnumeric():
                        previous_monies.append(text)
                        if len(previous_monies) > 5:
                            previous_monies.pop(0)
                        if len(previous_monies) > 1:
                            for prev in previous_monies[:-1]:  # Compare with previous reads
                                if is_one_digit_apart(prev, text):
                                    newcash = min(prev, text, key=int)
                                    break
                            if newcash:
                                if cash == 0:
                                    if newcash == 600:
                                        cash = newcash
                                        print(cash)
                                else:
                                    cash = newcash
                                    print(cash)
                            else:
                                if cash == 0:
                                    if text == "600":
                                        cash = int(text)
                                        print(cash)
                                else:
                                    cash = int(text)
                                    print(cash)
            newcash = 0
            time.sleep(0.5)
        except Exception as e:
            print(f"moneyread failed: {e}")       

def currentUpgrade():
    global upgradeLvl
    screenshot = pyautogui.screenshot(region=(160, 375, 120, 25))
    screenshot_array = np.array(screenshot)
    result = reader.readtext(screenshot_array, detail=0)
    if result:
        text = result[0]
        upgradeLvl = text[text.find("[") + 1 : text.find("]")]
import subprocess
script = f'''
    tell application "System Events"
        tell application "Roblox" to activate
        tell process "Roblox"
            set position of window 1 to {{{0}, {0}}}
            set size of window 1 to {{{900}, {900}}}
        end tell
    end tell
    '''
subprocess.run(["osascript", "-e", script])

listener = keyboard.Listener(on_press=on_press)
listener.start()

current_money = threading.Thread(target=currentMoney, daemon=True)
current_money.start()

wave_read = threading.Thread(target=waveRead, daemon=True)
wave_read.start()

# 223,50 333,69 wave
#217,315 682 547 cards
#410 160 start button
#250, 314 390,340 victory
#557 606 retry
#400 785 100 25 cash
#160 375 100 25 upgrade
#310 373 close
root.mainloop()