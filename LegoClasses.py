from html.parser import HTMLParser
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import requests

bricklinkColorDict = {'white' : 1, 
             'very light gray' : 49,
             'very light bluish gray' : 99,
             'light bluish gray' : 86,
             'light gray' : 9,
             'dark gray' : 10,
             'dark bluish gray' : 85,
             'black' : 11,
             'dark red' : 59,
             'red' : 5,
             'rust' : 27,
             'coral' : 220,
             'dark salmon' : 231,
             'salmon' : 25,
             'light salmon' : 26,
             'sand red' : 58,
             'reddish brown' : 88,
             'brown' : 8,
             'dark brown' : 120,
             'dark tan' : 69,
             'tan' : 2,
             'light flesh' : 90,
             'flesh' : 28,
             'medium dark flesh' : 150,
             'dark nougat' : 225,
             'dark flesh' : 91,
             'fabuland brown' : 106,
             'fabuland orange' : 160,
             'earth orange' : 29,
             'dark orange' : 68,
             'neon orange' : 165,
             'orange' : 4,
             'medium orange' : 31,
             'bright light orange' : 110,
             'light orange' : 32,
             'very light orange' : 96,
             'dark yellow' : 161,
             'yellow' : 3,
             'bright light yellow' : 103,
             'light yellow' : 33,
             'light lime' : 35,
             'yellowish green' : 158,
             'neon green' : 166,
             'medium lime' : 76,
             'lime' : 34,
             'olive green' : 155,
             'dark green' : 80,
             'green' : 6,
             'bright green' : 36,
             'medium green' : 37,
             'light green' : 38,
             'sand green' : 48,
             'dark turqoise' : 39,
             'light turqoise' : 40,
             'aqua' : 41,
             'light aqua' : 152,
             'dark blue' : 63,
             'blue' : 7,
             'dark azure' : 153,
             'medium azure' : 156,
             'medium blue' : 42,
             'maersk blue' : 72,
             'bright light blue' : 105,
             'light blue' : 62,
             'sky blue' : 87,
             'sand blue' : 55,
             'blue-violet' : 97,
             'dark blue-violet' : 109,
             'violet' : 43,
             'medium violet' : 73,
             'light violet' : 44,
             'dark purple' : 89,
             'purple' : 24,
             'light purple' : 93,
             'medium lavender' : 157,
             'clikits lavender' : 227,
             'lavender' : 154,
             'sand purple' : 54,
             'magenta' : 71,
             'dark pink' : 47,
             'medium dark pink' : 94,
             'bright pink' : 104,
             'pink' : 23,
             'light pink' : 56,
             'trans-clear' : 12,
             'trans-black' : 13,
             'trans-red' : 17,
             'trans-neon orange' : 18,
             'trans-orange' : 98,
             'trans-light orange' : 164,
             'trans-neon yellow' : 121,
             'trans-yellow' : 19,
             'trans-neon green' : 16,
             'trans-bright green' : 108,
             'trans-light green' : 221,
             'trans-light bright green' : 226,
             'trans-green' : 20,
             'trans-dark blue' : 14,
             'trans-medium blue' : 74,
             'trans-light blue' : 15,
             'trans-aqua' : 113,
             'trans-light purple' : 114,
             'trans-purple' : 51,
             'trans-dark pink' : 50,
             'trans-pink' : 107,
             'chrome gold' : 21,
             'chrome silver' : 22,
             'chrome antique brass' : 57,
             'chrome black' : 122,
             'chrome blue' : 52,
             'chrome green' : 64,
             'chrome pink' : 82,
             'pearl white' : 83,
             'pearl very light gray' : 119,
             'pearl light gray' : 66,
             'flat silver' : 95,
             'pearl dark gray' : 77,
             'pearl light gold' : 61,
             'pearl gold' : 115,
             'flat dark gold' : 81,
             'copper' : 84,
             'metal blue' : 78,
             'metallic silver' : 67,
             'metallic green' : 70,
             'metallic gold' : 65}

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
        self.imgPath = imgPath
        self.image = Image.open(requests.get(self.imgPath, stream=True).raw)
        self.image = self.image.resize((85,85))
        self.photo = ImageTk.PhotoImage(self.image)
        self.currentAmount = currentAmount

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
