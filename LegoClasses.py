from html.parser import HTMLParser
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import requests
import os
import sys

class LegoElement:
    name = ""
    partNumber = ""
    currentAmount = 0
    requiredAmount = 0
    color = ""
    imgPath = None
    photo = None

    def __init__(self, name, partNumber, bricklinkPartNumber, requiredAmount, color, colorId, bricklinkColorId, imgPath, currentAmount=0):
        self.name = name
        self.partNumber = partNumber
        self.bricklinkPartNumber = bricklinkPartNumber
        self.requiredAmount = requiredAmount
        self.color = color
        self.colorId = colorId
        self.bricklinkColorId = bricklinkColorId
        if( imgPath != None and "http" in imgPath ) :
            self.imgPath = imgPath
            self.image = Image.open(requests.get(self.imgPath, stream=True).raw)
        else:
            self.imgPath = self.getPath("./x.png")
            self.image = Image.open(self.imgPath)
        self.image = self.image.resize((85,85))
        self.photo = ImageTk.PhotoImage(self.image)
        self.currentAmount = currentAmount
    
    def getPath(self, filename):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, filename)
        else:
            return filename

class RebrickableHtmlTableParser(HTMLParser):
    dataOrder = ['partNumber', 'requiredAmount', 'color', 'name']
    dataIndex = 0
    
    elements = []
    imgPath = None
    partNumber = ""
    requiredAmount = 0
    color = ""
    name = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'data-src':
                    self.imgPath = attr[1]

    def handle_data(self, data):
        if not data.strip():
            return
        
        curData = self.dataOrder[self.dataIndex]
        if curData == 'partNumber':
            self.partNumber = data
        elif curData == 'requiredAmount':
            self.requiredAmount = data
        elif curData == 'color':
            self.color = data
        elif curData == 'name':
            self.name = data
            tmpElement = LegoElement(self.name, self.partNumber, self.requiredAmount, self.color, self.imgPath)
            self.elements.append(tmpElement)

        self.dataIndex = (self.dataIndex + 1) % len(self.dataOrder)

    def getElements(self):
        return self.elements
    
class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
