# GUI libraries
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from tkscrolledframe import ScrolledFrame
import configparser
from os.path import exists
# CSV parser
import os
import csv
# Data structures
from LegoClasses import *
from RebrickableApi import *  

class LegoSetInventoryTool:

    def __init__(self):
        self.loadInventory = None
        self.setNum = None
        self.rbApiKey = None
        
        # Check for config file
        if ( not os.path.exists("./legoTools.ini")) :
            # Ask for api key
            self.askForRbApiKey()
        else :
            config = configparser.ConfigParser()
            config.read("legoTools.ini")
            self.rbApiKey = config["DEFAULT"]["RebrickableApiKey"]
            self.mRbApi = RebrickableApi(self.rbApiKey)
            self.loadInitialPopup()

#************** Popup to ask user for Rebrickable API Key **************************************
    def askForRbApiKey(self) :
        self.rbApiKeyPopup = tk.Tk()
        self.rbApiKeyPopup.wm_title("API Key")
        apiLabel = tk.Label(self.rbApiKeyPopup, text="Please enter Rebrickable API key:")
        apiLabel.pack(side=TOP)
        self.apiKeyVar = tk.StringVar()
        apiKeyEntry = Entry(self.rbApiKeyPopup, textvariable=self.apiKeyVar)
        apiKeyEntry.pack(side=LEFT)
        submitButton = tk.Button(self.rbApiKeyPopup, text="Submit", command=self.submitApiKey)
        submitButton.pack(side=LEFT)

    def submitApiKey(self) :
        self.rbApiKey = self.apiKeyVar.get()
        self.rbApiKeyPopup.destroy()
        self.saveApiKey()

    def saveApiKey(self) :
        config = configparser.ConfigParser()
        config["DEFAULT"] = {'RebrickableApiKey' : self.rbApiKey}
        with open("legoTools.ini", "w") as configFile :
            config.write(configFile)
        self.mRbApi = RebrickableApi(self.rbApiKey)
        self.loadInitialPopup()

#************** Popup to ask whether to create new inventory or load existing ******************
    def loadInitialPopup(self) :
        # Pop up to ask to create new inventory or open existing
        self.initialPopup = tk.Tk()
        setNumberLabel = tk.Label(self.initialPopup, text="Create new inventory or load existing?")
        setNumberLabel.pack(side=TOP)
        selectionFrame = tk.Frame()
        newButton = tk.Button(selectionFrame, text="New", command=self.selectNew, height=6, width=12)
        newButton.pack(side=LEFT)
        loadButton = tk.Button(selectionFrame, text="Load", command=self.selectLoad, height=6, width=12)
        loadButton.pack(side=LEFT)
        selectionFrame.pack(side=TOP)
        self.initialPopup.mainloop()

    def selectNew(self) :
        self.loadInventory = False
        self.initialPopup.destroy()
        self.getSetNumber()

    def selectLoad(self) :
        self.loadInventory = True
        self.initialPopup.destroy()
        self.loadMainWindow()

#************** Popup to ask user for Lego set number **************************************
    def getSetNumber(self) :
        self.getSetNumberPopup = tk.Tk()
        setNumberLabel = tk.Label(self.getSetNumberPopup, text="Please enter set number:")
        setNumberLabel.pack(side=TOP)
        entryFrame = tk.Frame()
        self.setNumVar = tk.StringVar()
        setNumEntry = Entry(entryFrame, textvariable=self.setNumVar)
        setNumEntry.pack(side=LEFT)
        createButton = tk.Button(entryFrame, text="Create Inventory", command=self.pressCreate)
        createButton.pack(side=LEFT)
        entryFrame.pack(side=TOP)
        noteLabel = tk.Label(self.getSetNumberPopup, text="NOTE: Tool will append -1 to entered set number unless a version is provided")
        noteLabel.pack(side=BOTTOM)

    def pressCreate(self) :
        self.setNum = self.setNumVar.get()
        self.getSetNumberPopup.destroy()
        self.loadMainWindow()

#************** Main GUI Window **************************************        
    def loadMainWindow(self) :
        
        self.mainWindow = tk.Tk()
        self.mainWindow.wm_title("Lego Set Inventory Tool")
        self.mainWidth = 0

        # Create a ScrolledFrame widget
        self.sf = ScrolledFrame(self.mainWindow, width=640, height=480)
        self.sf.pack(side="top", expand=1, fill="both")
        self.sf.bind_arrow_keys(self.mainWindow)
        self.sf.bind_scroll_wheel(self.mainWindow)
        
        # Data Structure Creation
        self.requiredElements = []
        if (self.loadInventory) :
            filePath = filedialog.askopenfilename(filetypes=[("Load Files", ".csv .html")])
            fileParts = os.path.basename(filePath).split('.')
            print(fileParts)
            fileName = fileParts[0]
            fileExtension = fileParts[1]
            with open(filePath, 'r+') as inputFile:
                if fileExtension == 'html':
                    # Remove header lines from html
                    lines = inputFile.readlines()
                    inputFile.seek(0)
                    inputFile.truncate()
                    inputFile.writelines(lines[18:])
                    inputFile.seek(0)

                    # Parse file
                    parser = RebrickableHtmlTableParser()
                    parser.feed(inputFile.read())
                    self.requiredElements = parser.getElements()
                    self.legoSetNameText = fileName
                elif fileExtension == 'csv':
                    csvReader = csv.reader(inputFile, delimiter=',')
                    readHeader = False
                    for row in csvReader:
                        if not readHeader :
                            readHeader = True
                            saveFileVersion = row[0]
                            continue
                        tmpElement = LegoElement(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                        self.requiredElements.append(tmpElement)
                        self.legoSetNameText = fileName
        else :
            # Append set version if necessary
            if ( "-" not in self.setNum ) :
                self.setNum = self.setNum + "-1"

            # Get set name
            setDetails = self.mRbApi.getSetDetails(self.setNum)
            self.legoSetNameText = setDetails["name"]
            
            # Get parts list from API
            partsList = self.mRbApi.getSetInventory(self.setNum)

            for part in partsList :
                # Skip spare parts
                if (part["is_spare"]) :
                    continue

                tmpElement = LegoElement(part["part"]["name"], 
                                         part["part"]["part_num"], 
                                         part["part"]["external_ids"]["BrickLink"][0],
                                         part["quantity"], 
                                         part["color"]["name"],
                                         part["color"]["id"],
                                         part["color"]["external_ids"]["BrickLink"]["ext_ids"][0],
                                         part["part"]["part_img_url"])
                self.requiredElements.append(tmpElement)



        # Required Pieces display creation
        self.pieceFrame = self.sf.display_widget(tk.Frame)
        self.maxColumns = 10
        self.pieceButtons = []
        self.btnToolTips = []
        curRow = 0
        curCol = 0
        for element in self.requiredElements:
            tmpButton = tk.Button(master=self.pieceFrame, text = str(element.currentAmount) + "/" + str(element.requiredAmount), image=element.photo, compound=TOP)
            tmpButton.grid(row=curRow, column = curCol)
            tmpButton.bind("<Button-1>", self.leftClick)
            tmpButton.bind("<Button-3>", self.rightClick)
            tmpToolTip = CreateToolTip(tmpButton, element.name + ", " + element.color)
            self.pieceButtons.append(tmpButton)
            self.btnToolTips.append(tmpToolTip)

            curCol += 1
            if curCol == self.maxColumns:
                curCol = 0
                curRow += 1
            

        # Title Creation
        self.titleFrame = tk.Frame()
        self.legoSetName = tk.Label(master=self.titleFrame, text=self.legoSetNameText)
        self.legoSetName.pack(side = tk.LEFT)
        self.showHideBtn = tk.Button(master=self.titleFrame, text="Show All")
        self.showHideBtn.bind("<Button-1>", self.showAll)
        self.showHideBtn.pack(side=RIGHT)
        self.rebrickableExportBtn = tk.Button(master=self.titleFrame, text="Rebrickable Export")
        self.rebrickableExportBtn.bind("<Button-1>", self.rebrickableExport)
        self.rebrickableExportBtn.pack(side=RIGHT)
        self.bricklinkExportBtn = tk.Button(master=self.titleFrame, text="BrickLink Export")
        self.bricklinkExportBtn.bind("<Button-1>", self.bricklinkExport)
        self.bricklinkExportBtn.pack(side=RIGHT)
        self.titleFrame.pack()

        # Resize grid when window size changes
        self.mainWindow.bind("<Configure>", self.resize)

        self.mainWindow.mainloop()

    def redrawGrid(self, allButtons=False):
        curRow = 0
        curCol = 0
        for button in self.pieceButtons:
            btnText = button['text']
            amounts = btnText.split("/")
            if (amounts[0] == amounts[1]) and not allButtons:
                button.grid_forget()
                button.configure(background = "Green")
                continue
            button.grid(row=curRow, column=curCol)
            curCol += 1
            if curCol == self.maxColumns:
                curCol = 0
                curRow += 1

    def resize(self, event):
        if str(event.widget) == ".":
            if self.mainWidth != event.width :
                self.mainWidth = event.width

                self.maxColumns = self.mainWidth // 93
                if self.maxColumns < 5:
                    self.maxColumns = 5
                self.redrawGrid()

    def leftClick(self, event):
        btnText = event.widget['text']
        amounts = btnText.split("/")
        if len(amounts) == 2:
            curAmount = int(amounts[0]) + 1
            reqAmount = amounts[1]
            event.widget.config(text = str(curAmount) + "/" + reqAmount)
            self.save()
            if curAmount == int(reqAmount):
                event.widget.grid_forget()
                self.redrawGrid()
                

    def rightClick(self, event):
        btnText = event.widget['text']
        amounts = btnText.split("/")
        if len(amounts) == 2:
            if amounts[0] == amounts[1]:
                event.widget.configure(background = "SystemButtonFace")
            if int(amounts[0]) > 0:
                curAmount = int(amounts[0]) - 1
                reqAmount = amounts[1]
                event.widget.config(text = str(curAmount) + "/" + reqAmount)
                self.save()

    def showAll(self, event):
        btnText = event.widget['text']
        if btnText == "Show All":
            self.redrawGrid(True)
            event.widget.config(text = "Hide Completed")
        elif btnText == "Hide Completed":
            self.redrawGrid()
            event.widget.config(text = "Show All")

    def save(self):
        outputFile = self.legoSetName['text'] + ".csv"
        with open(outputFile, 'w', newline='') as output:
            csvWriter = csv.writer(output, delimiter=',')
            # Write version info
            headerRow = ["1.0","","","","","","","",""]
            csvWriter.writerow(headerRow)
            for i in range(len(self.requiredElements)):
                row = []
                tmpElement = self.requiredElements[i]
                row.append(tmpElement.name)
                row.append(tmpElement.partNumber)
                row.append(tmpElement.bricklinkPartNumber)
                row.append(tmpElement.requiredAmount)
                row.append(tmpElement.color)
                row.append(tmpElement.colorId)
                row.append(tmpElement.bricklinkColorId)
                row.append(tmpElement.imgPath)
                
                tmpBtn = self.pieceButtons[i]
                btnText = tmpBtn['text']
                curAmount = btnText.split('/')[0]
                row.append(curAmount)
                csvWriter.writerow(row)

#************** Export to Bricklink xml format **************************************                 
    def bricklinkExport(self, event):
        with open(self.legoSetName['text'] + ".xml", "w") as output:
            output.write("<INVENTORY>")

            for i in range(len(self.requiredElements)):
                amounts = self.pieceButtons[i]['text'].split('/')
                cur = int(amounts[0])
                req = int(amounts[1])
                if cur < req:
                    missingAmount = req - cur
                    output.write("<ITEM>")

                    output.write("<ITEMTYPE>P</ITEMTYPE>")
                    output.write("<ITEMID>" + self.requiredElements[i].bricklinkPartNumber + "</ITEMID>")
                    output.write("<COLOR>" + str(self.requiredElements[i].bricklinkColorId) + "</COLOR>")
                    output.write("<MINQTY>" + str(missingAmount) + "</MINQTY>")
            
                    output.write("</ITEM>")

            output.write("</INVENTORY>")

#************** Export to Rebrickable csv format **************************************             
    def rebrickableExport(self, event):
        with open(self.legoSetName['text'] + " missing parts.csv", "w", newline='') as saveFile:
            csvWriter = csv.writer(saveFile, delimiter=',')
            header = ["Part", "Color", "Quantity"]
            csvWriter.writerow(header)
            for i in range(len(self.requiredElements)):
                amounts = self.pieceButtons[i]['text'].split('/')
                cur = int(amounts[0])
                req = int(amounts[1])
                if cur < req:
                    row = []
                    row.append(self.requiredElements[i].partNumber)
                    row.append(self.requiredElements[i].colorId)
                    
                    missingAmount = req - cur
                    row.append(str(missingAmount))
                    csvWriter.writerow(row)

            
        
#---- Main ----
tool = LegoSetInventoryTool()
