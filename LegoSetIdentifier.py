# GUI libraries
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkscrolledframe import ScrolledFrame
import webbrowser
import tkinter.font as tkFont

# API access
from RebrickableApi import *           

class LegoSetIdentifier:

    mPartsList = []

    def __init__(self, apiKey):
        self.mRbApi = RebrickableApi(apiKey)
        colorDict = self.mRbApi.getColors()
        self.mColorList = sorted(colorDict.keys())
        
        self.mainWindow = tk.Tk()
        self.mainWindow.title('Set Identifier')
        self.mainWidth = 0
        
        title = tk.Frame(self.mainWindow)
        pnLabel = ttk.Label(title, text="Part Number", width=20)
        pnLabel.pack(side="left")
        colorLabel = ttk.Label(title, text="Color", width=25)
        colorLabel.pack(side="left")
        submitButton = tk.Button(title, text="Submit", command=self.compareParts)
        submitButton.pack(side="right")
        addPartButton = tk.Button(title, text="Add Part", command = self.addPart)
        addPartButton.pack(side="right")
        title.pack()


    def addPart(self):
        #Create new frame to hold part entry items
        newFrame = tk.Frame(self.mainWindow)

        # Create text entry box for part number
        partNumber = tk.StringVar()
        partNumberEntry = Entry(newFrame, textvariable=partNumber)
        partNumberEntry.pack(side="left")

        # Create combobox for color selection
        color = tk.StringVar()
        colorSelection = ttk.Combobox(newFrame, textvariable=color)
        colorSelection['values'] = self.mColorList
        colorSelection['state'] = 'readonly'
        colorSelection.pack(side="left")
        part = [partNumber,color]
        self.mPartsList.append(part)
        newFrame.pack(side="top", anchor=NW)

        
    def compareParts(self):
        
        setList = []
        for x in range(len(self.mPartsList)) :
            if x == 0 :
                setList = self.mRbApi.getSetsContaining(self.mPartsList[0][0].get(), self.mPartsList[0][1].get())
            else :
                newList = self.mRbApi.getSetsContaining(self.mPartsList[x][0].get(), self.mPartsList[x][1].get())
                print("new: ",len(newList))
                setList = [x for x in setList if x in newList]
            print("set: ",len(setList))

        #numList = [x["set_num"] for x in setList]
        #urlList = [x["set_url"] for x in setList]
        for x in range(len(setList)):
            self.addResult(setList[x]["set_num"], setList[x]["set_url"])

    def openUrl(self, url):
        webbrowser.open_new(url)

    def addResult(self, setNum, setUrl):
        result = tk.Label(self.mainWindow, text=setNum, fg='blue')
        # Underline text
        underFont = tkFont.Font(result, result.cget("font"))
        underFont.configure(underline = True)
        result.configure(font=underFont)
        result.pack(side=TOP, anchor=NW)
        result.bind("<Button-1>", lambda e: self.openUrl(setUrl))
        
        
#---- Main ----
ident = LegoSetIdentifier()
ident.addPart()




