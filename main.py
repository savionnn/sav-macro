from macro import upgrade, coordinate, placement
import importlib
importlib.reload(upgrade)
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk
from pynput import keyboard
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
root.minsize(314,450)

style = ttk.Style()

root.tk.call("source", "/Users/savion/developer/av-macro/ttk_theme/azure.tcl")  
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

Label(root, text="Start Macro: F1",font=("Arial", 10)).place(x=10,y=370)
Label(root, text="Stop Macro: F3",font=("Arial", 10)).place(x=10,y=390)

macro_active = True

def startMacro():
    for i in range(len(unitsBool)):
        if unitsBool[i] and macro_active:
            if unitActions[i] == "Place":
                placement.placement(units[i],unitSlots[i])
            else:
                upgrade.upgrade(units[i])
            time.sleep(2)
    return

def on_press(key):
    global macro_active
    if key == keyboard.Key.f1:
        print("Start Macro triggered!")
        macro_thread = threading.Thread(target=startMacro, daemon=True)
        macro_thread.start()
    elif key == keyboard.Key.f3:
        macro_active = False
        print("Stop Macro triggered!")

listener = keyboard.Listener(on_press=on_press)
listener.start()

root.mainloop()