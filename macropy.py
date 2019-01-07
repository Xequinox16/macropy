import win32api, win32con, win32gui
import os, time, math
from pynput import keyboard
import asyncio
import json
os.system("title Macropy")

Sequences = [[['left', 0, 0, 2], ['right', 2559, 1079, 1]]]
UnixTimeInMilliseconds = 0
UnixTimeInSeconds = 0
lastClickStamp = time.time()
def TvarUpdate():
    global UnixTimeInMilliseconds,UnixTimeInSeconds
    UnixTimeInMilliseconds = int(round(time.time() * 1000))
    UnixTimeInSeconds = int(round(time.time()))
def getCursorPos():
    mouseX, mouseY = win32api.GetCursorPos()
    return(mouseX,mouseY)
def click(x,y,z):
    win32api.SetCursorPos((x,y))
    if z == None or z == False:
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    elif z == True:
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)
def RecordSequence():
    global lastClickStamp
    memory = None
    try:
        RecordCountdown = int(input("Enter record countdown: "))
    except:
        print("ValueError, Retry")
        RecordSequence()
    for i in range(0,RecordCountdown):
        os.system("cls")
        print("Recording in " + str(RecordCountdown - i))
        time.sleep(1)
    os.system("cls")
    print("#"*20)
    print("Recording, Press Q To Mark A Left Click And E To Mark A Right Click, To Stop Recording Press W")
    print("#"*20)
    temp = []
    lastClickStamp = time.time()
    def on_press(key):
        global lastClickStamp
        try:
            if key.char == "q":
                TvarUpdate()
                difference = UnixTimeInSeconds - lastClickStamp
                if difference < 0:
                    difference = 0
                temp.append(
                ["left",
                getCursorPos()[0],
                getCursorPos()[1],
                difference
                ]
                )
                lastClickStamp = time.time()
            elif key.char == "e":
                TvarUpdate()
                difference = UnixTimeInSeconds - lastClickStamp
                if difference < 0:
                    difference = 0
                temp.append(
                ["right",
                getCursorPos()[0],
                getCursorPos()[1],
                difference
                ]
                )
                lastClickStamp = time.time()
            elif key.char == "w":
                return(False)
        except:
            pass
    with keyboard.Listener(
        on_press=on_press) as listener:
            listener.join()
    memory = temp
    print(json.dumps(memory))
def RunSequence():
    Sequence = input("Enter a sequence: ")
    try:
        Sequence = json.loads(Sequence)
    except:
        print("Error with JSON, verify sequence and try again.")
        RunSequence()
    print("JSON SEQUENCE LOADED")
    try:
        RunCountdown = int(input("Enter a run countdown: "))
    except:
        print("ValueError, Retry")
        RunSequence()
    for i in range(0,RunCountdown):
        os.system("cls")
        print("Running Sequence in " + str(RunCountdown - (i + 1)) + " Seconds.")
        time.sleep(1)
    for i in Sequence:
        time.sleep(i[3])
        clickType = False
        if i[0] == "left":
            clickType = False
        else:
            clickType = True
        click(i[1],i[2],clickType)
def EditSequence():
    print("K3")

#MenuSettings
options = ["[1] -> Record a sequence","[2] -> Run a sequence","[3] -> Edit a sequence"]
paddingRight = 10
paddingTop = 5
paddingBottom = 5
#MenuSettings#MenuSettings#MenuSettings#MenuSettings#MenuSettings

borderRadius = 0
highestLength = 0
lastMenuError = ""
for i in options:
    if len(i) > highestLength:
        highestLength = len(i)
borderRadius = highestLength + paddingRight + 1



def drawMenu(takeInput):
    global lastMenuError
    os.system("cls")
    print("#"*borderRadius)
    for i in range(0,paddingTop):
        print(" " * (borderRadius-1) + "#")
    for i in options:
        space = highestLength - len(i)
        print(i + " " * (space + paddingRight) + "#")
    for i in range(0,paddingBottom):
        print(" " * (borderRadius-1) + "#")

    print("#"*borderRadius)
    if lastMenuError != "":
        print("Err: "+lastMenuError)
    if takeInput:
        choice = input(" [:> ")
        return(choice)
    else:
        return(0)

choice = None

def HandleError():
    global lastMenuError,choice
    try:
        choice = int(drawMenu(True))
        if choice > len(options) or choice <= 0:
            raise ValueError()
        else:
            lastMenuError = ""
    except ValueError:
        Err="Invalid Number Range"
        if lastMenuError == Err or lastMenuError[:4] == Err[:4]:
            lastTwo = lastMenuError[-2:]
            if lastTwo[:1] == "x":
                lastMenuError = Err + " x" + str(int(lastTwo[1:])+1)
            elif lastTwo == "10":
                lastMenuError = Err
            else:
                lastMenuError = Err + " x2"
        else:
            lastMenuError = Err
        HandleError()

HandleError()
if choice != None:
    if choice == 1:
        RecordSequence()
    elif choice == 2:
        RunSequence()
    elif choice == 3:
        EditSequence()
    else:
        HandleError()
