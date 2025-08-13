from macro import upgrade, placement, coordinate
import tkinter as tk
from tkinter import *
from tkinter import ttk

class unit:
    def __init__(self, bool:bool, coords:tuple, slot:int, action:str, upgradeLevel:str):
        self.bool = bool
        self.coords = coords
        self.slot = slot
        self.action = action
        self.upgradeLevel = upgradeLevel
    def upgrade(self):
        upgrade.upgrade(self.coords)
    def place(self):
        placement.placement(self.coords,self.slot)
slotPrices = [1000,1000,1000,1000,1000,1000]
infiniteMode = False
portalMode = True
infiniteResetWave = 10
units = []
units.append(unit(False,(1,1),1,"Place & Upgrade","0"))
root = tk.Tk()
root.title("SAV Macro")
root.geometry("540x600+900+0")
root.minsize(540,600)
style = ttk.Style()

root.tk.call("source", "./ttk_theme/azure.tcl")  
root.tk.call("set_theme", "dark")
style.configure(
    "Add.TButton",  
    foreground="white", 
    background="#444444", 
    font=("Arial",15),
    padding=0
)
style.configure(
    "Select.TButton",  
    foreground="white", 
    background="#444444", 
    font=("Arial",10),
    padding=0
)
def selectUnit(i):
    units[i].bool = not units[i].bool

def selectSlot(event, i):
    units[i].slot = int(combo_boxes_slot[i].get())

def selectAction(event, i):
    units[i].action = combo_boxes_action[i].get()

def selectUpgrade(event, i):
    units[i].upgradeLevel = combo_boxes_upgrade[i].get()

def saveEntries():
    for i in range(len(xEntries)):
        units[i].coords = (int(xEntries[i].get()), int(yEntries[i].get()))
        
def savePrices():
    for i in range(6):
        slotPrices[i] = int(priceEntries[i].get())

def loadPrices():
    for i in range(6):
        priceEntries[i].delete(0, "end")
        priceEntries[i].insert(0, slotPrices[i])

def toggleInfinite():
    global infiniteMode
    infiniteMode = not infiniteMode

def selectCoordinate(i):
    units[i].coords = coordinate.coordinate()
    xEntries[i].delete(0, "end")
    xEntries[i].insert(0, round(units[i].coords[0]))
    yEntries[i].delete(0, "end")
    yEntries[i].insert(0, round(units[i].coords[1]))

def addUnit():
    saveEntries()
    units.append(unit(False,(1,1),1,"Place & Upgrade","0"))
    generate()

elements = []
combo_boxes_slot = []
combo_boxes_action = []
combo_boxes_upgrade = []
xEntries = []
yEntries = []
priceEntries = []
runNumber = 0
def generate():
    for i in elements+combo_boxes_slot+combo_boxes_action+combo_boxes_upgrade+yEntries+xEntries:
        i.destroy()
    elements.clear()
    combo_boxes_slot.clear()
    combo_boxes_action.clear()
    combo_boxes_upgrade.clear()
    xEntries.clear()
    yEntries.clear()
    for i in range(len(units)):
        checkButton = tk.Checkbutton(root, text="Unit {}".format(i+1), font=("Arial", 10), command=lambda i=i: selectUnit(i))
        if units[i].bool:
            checkButton.select()
        checkButton.place(x=5, y=i*30, width=60, height=30)
        elements.append(checkButton)

        slotLabel = tk.Label(root,text="Slot:",font=("Arial", 10))
        slotLabel.place(x=60, y=i*30, width=50, height=30)
        elements.append(slotLabel)

        combo_box_slot = ttk.Combobox(root,font=("Arial",10), values=[1,2,3,4,5,6], width=4, state="readonly", takefocus=0)
        combo_box_slot.place(x=100, y=i*30+3, height=25)
        combo_box_slot.set(units[i].slot)
        combo_box_slot.bind("<<ComboboxSelected>>", lambda event,i=i: selectSlot(event,i))
        combo_boxes_slot.append(combo_box_slot)

        actionLabel = tk.Label(root,text="Action:",font=("Arial", 10))
        actionLabel.place(x=145, y=i*30, width=50, height=30)
        elements.append(actionLabel)
        
        combo_box_action = ttk.Combobox(root,font=("Arial",10), values=["Place & Upgrade","Upgrade"], width=10, state="readonly", takefocus=0)
        combo_box_action.place(x=190, y=i*30+3, height=25)
        combo_box_action.set(units[i].action)
        combo_box_action.bind("<<ComboboxSelected>>", lambda event,i=i: selectAction(event,i))
        combo_boxes_action.append(combo_box_action)

        upgradeLabel = tk.Label(root,text="Upgrade:",font=("Arial", 10))
        upgradeLabel.place(x=270, y=i*30, width=50, height=30)
        elements.append(upgradeLabel)
        
        combo_box_upgrade = ttk.Combobox(root,font=("Arial",10), values=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,"MAX"], width=5, state="readonly", takefocus=0)
        combo_box_upgrade.place(x=320, y=i*30+3, height=25)
        combo_box_upgrade.set(units[i].upgradeLevel)
        combo_box_upgrade.bind("<<ComboboxSelected>>", lambda event,i=i: selectUpgrade(event,i))
        combo_boxes_upgrade.append(combo_box_upgrade)

        xLabel = tk.Label(root,text="X:",font=("Arial", 10))
        xLabel.place(x=370, y=i*30, height=30)
        elements.append(xLabel)

        xEntry = tk.Entry(root)
        xEntry.insert(0, round(units[i].coords[0]))
        xEntry.place(x=390, y=i*30, height=30,width=30)
        xEntries.append(xEntry)

        yLabel = tk.Label(root,text="Y:",font=("Arial", 10))
        yLabel.place(x=420, y=i*30, height=30)
        elements.append(yLabel)

        yEntry = tk.Entry(root)
        yEntry.insert(0, round(units[i].coords[1]))
        yEntry.place(x=440, y=i*30, height=30,width=30)
        yEntries.append(yEntry)

        coordButton = ttk.Button(root, text="Select", style="Select.TButton")
        coordButton.config(command=lambda i=i: selectCoordinate(i))
        coordButton.place(x=480, y=i*30+3, height=25,width=55)

    addButton = ttk.Button(root, text="+", style="Add.TButton")
    addButton.config(command=lambda: addUnit())
    addButton.place(x=255, y=len(units)*30+3, width=25, height=25)
    elements.append(addButton)

infiniteButton = tk.Checkbutton(root, text="Infinite Mode, enter wave to reset at:", font=("Arial", 10), command=lambda:toggleInfinite())
infiniteButton.place(x=240, y=550)
infiniteEntry = tk.Entry(root, textvariable=infiniteResetWave)
infiniteEntry.insert(0, 10)
infiniteEntry.place(x=430, y=545, height=30, width=30)

Label(root, text="Enter slot prices: ", font=("Arial",10)).place(y=470, height=30)

for i in range(6):
    priceLabel = tk.Label(root, text="Slot {}:".format(i+1), font=("Arial",10))
    priceLabel.place(x=i*90, y=500, height=30)
        
    priceEntry = tk.Entry(root)
    priceEntry.insert(0, 1000)
    priceEntry.place(x=i*90+30, y=500, height=30, width=60)
    priceEntries.append(priceEntry)

Label(root, text="Start Macro: F1",font=("Arial", 10)).place(y=540)
Label(root, text="Stop Macro: F3",font=("Arial", 10)).place(y=560)

saveButton = ttk.Button(root, text="Save", style="Select.TButton")
saveButton.config(command=lambda: saveFile())
saveButton.place(x=90, y=550,)

saveButton = ttk.Button(root, text="Load", style="Select.TButton")
saveButton.config(command=lambda: loadFile())
saveButton.place(x=160, y=550,)

generate()
import time
from pynput import keyboard
import pyautogui
import threading
import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)
old_wave = ""
total_wave= ""
cash = 0
upgradeLvl = "0"
macro_active = False

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
    savePrices()
    saveEntries()
    time.sleep(2)
    cash = 0
    for i in range(len(units)):
        unit = units[i]
        if unit.bool:
            if unit.action == "Place & Upgrade":
                print(f"price: {slotPrices[unit.slot-1]}")
                print(f"cash: {cash}")
                while slotPrices[unit.slot-1] > int(cash):
                    if not macro_active:
                        return
                    time.sleep(0.1)
                unit.place()
                time.sleep(2)
                while unit.upgradeLevel != upgradeLvl:
                    if not macro_active:
                        return
                    unit.upgrade()
                    currentUpgrade()
                    time.sleep(2)
                pyautogui.moveTo(310, 373)
                pyautogui.leftClick()
            else:
                while unit.upgradeLevel != upgradeLvl:
                    if not macro_active:
                        return
                    unit.upgrade()
                    currentUpgrade()
                    time.sleep(2)
                pyautogui.moveTo(310, 373)
                pyautogui.leftClick()
            time.sleep(2)
        upgradeLvl = "0"
    return

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
                        if infiniteMode:
                            try:
                                if int(wave_part) >= infiniteResetWave:
                                    print("restart")
                                    restartMatch()
                                else:
                                    gameResult()
                                    pyautogui.moveTo(450,506)
                                    time.sleep(0.1)
                                    pyautogui.click(button='left', clicks=10, interval=0.50,)
                            except:
                                print("some error")
                    if current_wave != old_wave:
                        print(f"New wave detected: {current_wave}")
                        old_wave = current_wave
                        if infiniteMode:
                            if int(old_wave) >= infiniteResetWave:
                                print("restart")
                                restartMatch()
            elif not infiniteMode and old_wave == total_wave and not portalMode:
                gameResult()
                pyautogui.moveTo(450,450)
                time.sleep(0.1)
                pyautogui.click(button='left', clicks=10, interval=0.50,)
            elif portalMode:
                pyautogui.moveTo(333,510)
                pyautogui.leftClick()
                time.sleep(0.5)
                pyautogui.moveTo(400,510)
                pyautogui.leftClick()
                time.sleep(0.5)
                pyautogui.moveTo(450,500)
                pyautogui.leftClick()
                pyautogui.moveTo(450,450)
                time.sleep(0.1)
                pyautogui.click(button='left', clicks=10, interval=0.50,)
                gameResult()
            gameResult()
            time.sleep(10)
        except Exception as e:
            print(e)

def restartMatch():
    global macro_active
    global old_wave
    global cash
    macro_active = False
    pyautogui.moveTo(450,450)
    pyautogui.leftClick()
    time.sleep(0.5)
    pyautogui.moveTo(21,879)
    pyautogui.leftClick()
    time.sleep(0.5)
    pyautogui.moveTo(781,418)
    pyautogui.leftClick()
    discordResult(2)
    time.sleep(0.5)
    pyautogui.moveTo(384,506)
    pyautogui.leftClick()
    time.sleep(0.5)
    pyautogui.moveTo(450,500)
    pyautogui.leftClick()
    time.sleep(5)
    macro_active = True
    macro_thread = threading.Thread(target=startMacro, daemon=True)
    macro_thread.start()
    old_wave = ""
    cash = 0

def gameResult():
    global macro_active
    global old_wave
    global cash
    # victoryScreenshot = pyautogui.screenshot(region=(250, 314, 140, 30)) old
    victoryScreenshot = pyautogui.screenshot(region=(157, 265, 100, 30))
    victoryScreenshot_array = np.array(victoryScreenshot)
    victoryResult = reader.readtext(victoryScreenshot_array, detail=0)
    if victoryResult:
        print(victoryResult[0])
        if not infiniteMode:
            if "Victory" in victoryResult[0] or "Viatory" in victoryResult[0]:
                if portalMode:
                    print("Portal run")
                    macro_active = False
                    discordResult(3)
                    time.sleep(5)
                    # pyautogui.moveTo(557,606) old retry
                    pyautogui.moveTo(806,282) # close button
                    time.sleep(0.1)
                    pyautogui.leftClick()
                    macro_active = True
                    macro_thread = threading.Thread(target=startMacro, daemon=True)
                    macro_thread.start()
                    old_wave = ""
                    cash = 0
                else:
                    print("Victory run")
                    macro_active = False
                    discordResult(0)
                    time.sleep(5)
                    # pyautogui.moveTo(557,606) old retry
                    pyautogui.moveTo(380,624) # new retry
                    time.sleep(0.1)
                    pyautogui.leftClick()
                    macro_active = True
                    macro_thread = threading.Thread(target=startMacro, daemon=True)
                    macro_thread.start()
                    old_wave = ""
                    cash = 0
        if "Failed" in victoryResult[0]:
            print("Failed run")
            macro_active = False
            discordResult(1)
            time.sleep(5)
            if infiniteMode:
                pyautogui.moveTo(450, 506)
                time.sleep(0.1)
                pyautogui.click(button='left', clicks=10, interval=0.50,)
            # pyautogui.moveTo(557,606) old retry button
            pyautogui.moveTo(380,624)
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
                                else:
                                    cash = newcash
                            else:
                                if cash == 0:
                                    if text == "600":
                                        cash = int(text)
                                else:
                                    cash = int(text)
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
from tkinter import filedialog
import pickle
def saveFile():
    savePrices()
    saveEntries()
    file = filedialog.asksaveasfile(
        title="Save as a file",
        mode='wb', 
        defaultextension=".pickle",
        filetypes=[("Pickle file", "*.pickle")]
    )
    if file: 
        pickle.dump([units,
                    slotPrices,
                    [infiniteMode,infiniteResetWave]],
                    file)
        file.close()


def loadFile():
    global units
    global slotPrices
    global infiniteMode
    global infiniteResetWave
    file_path = filedialog.askopenfilename(
        title="Select a save file",
        filetypes=(("Pickle file", "*.pickle"),("All files","*."))
    )
    if file_path:
        try:
            with open(file_path, 'rb') as file:
                loaded_object = pickle.load(file)
                units = loaded_object[0]
                slotPrices = loaded_object[1]
                infinite = loaded_object[2]
                infiniteMode = infinite[0]
                infiniteResetWave = int(infinite[1])
                generate()
                loadPrices()
                if infiniteMode:
                    infiniteButton.select()
                infiniteEntry.delete(0, "end")
                infiniteEntry.insert(0, infinite[1])
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
import datetime
import discord
def discordResult(state: int):
    global runNumber
    runNumber += 1
    discordScreenshot = pyautogui.screenshot(region=(0, 0, 900, 900))
    discordScreenshot.save('result.png')
    resultMessages = ["Run Victory",
                      "Run Failed",
                      "Run Restarted",
                      "Portal run"
                      ]
    webhook_url = "" # Replace with your actual webhook URL

    webhook = discord.SyncWebhook.from_url(webhook_url)

    embed = discord.Embed(
        title=resultMessages[state],
        description=f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Run #{runNumber}",
        color=0xF527EE
    )
    embed.set_image(url="attachment://result.png")
    embed.set_footer(text="SAV-Macro 2025")

    with open("result.png", "rb") as f:
        webhook.send(embed=embed, file=discord.File(f, filename="result.png"))

listener = keyboard.Listener(on_press=on_press)
listener.start()

current_money = threading.Thread(target=currentMoney, daemon=True)
current_money.start()

wave_read = threading.Thread(target=waveRead, daemon=True)
wave_read.start()

# 223,50 333,69 wavet
#217,315 682 547 cards
#410 160 start button
#250, 314 390,340 victory
#557 606 retry
#400 785 100 25 cash
#160 375 100 25 upgrade
#310 373 close
#21 879 settings
#781 418 restart
#384 506 confirm restart
#450 500 match has been restarted
#333 510, 450 510, 571 510 select portal

root.mainloop()