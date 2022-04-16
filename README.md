# legoTools
Over the past year I've start making bulk purchases of Legos for when my kids are older. I found myself wanting to sort out one or two sets from each bulk lot but I couldn't find a good tool for tracking the pieces as I found them. So I threw together a quick python script to help me keep an inventory of the set pieces as I found them. I thought other people might find this useful so I made it a bit more user friendly and I think I'm ready to share. I've only tested on Windows so I don't know how it will perform on other operating systems. Feel free to report bugs you find, but I'll warn you I have a young toddler and another one the way so bug fixes will happen sporadically at best.

***********************************************
LEGO SET INVENTORY TOOL
***********************************************
This tool was designed to help sort out pieces for a specific set from a large quantity of bulk Lego. Allows users to input a Lego set number to retrieve a parts inventory from Rebrickable. Pictures of parts are displayed in a grid along with current/required amounts. Once the required quantity for a part is reached the part is removed from the grid to declutter. Amounts are automatically saved to a csv file adjacent to the script in the form <Lego Set Name>.csv. Parts still needed can be exported to BrickLink or Rebrickable format. The BrickLink format will be output to <Lego Set Name>.xml adjacent to the script. The contents of that file can be copied into this webpage for import: https://www.bricklink.com/v2/wanted/upload.page 

How to run:  
First you'll need a Rebrickable API key. After creating a Rebrickable account you can generate one via the 'Generate an API key' link here: https://rebrickable.com/api/

Then to run the script:  

Option A: Easy Mode  
    - Download and run the latest release executable here: https://github.com/meequalspirate/legoTools/releases

Option B: If you're familiar with python/command line  
    - Install python 3.10.2: https://www.python.org/downloads/release/python-3102/  
    - Open a command line and run the following commands to install the dependencies:  
        pip install Pillow  
        pip install requests  
        pip install tkScrolledFrame  
    - Download/clone this repository  
    - Run the 'LegoSetInventoryTool.py' script  

Dependencies:  
    Python 3.10.2  
    Pillow 9.0.1  
    requests 2.27.1  
    tkScrolledFrame 1.0.4  


If this tool was useful or saved you some time feel free to donate(I told myself if this tool was popular enough I'd buy one of the UCS Star Destroyers):
[![Donate](https://img.shields.io/badge/Donate-via%20Square-brightgreen)](https://square.link/u/mq6dSYJS)

