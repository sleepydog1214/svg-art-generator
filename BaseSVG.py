import time
import math
import datetime

class BaseSVG:
    "Class to create a basic svg file"

    def __init__(self, width, height):
        w = str(width)
        h = str(height)

        timestamp = str(math.ceil(time.time()))
        today = datetime.date.today()
        year = str(today.year)
        today = str(today)
        
        self.filename = 'tsart-generated-' + timestamp + '.svg'
        
        self.svgCode = ''
        
        self.header = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
    version="1.1"
    width="''' + w + '"' + "\n"
        self.header = self.header + '    height="' + h + '"' + "\n"
        self.header = self.header + '    viewBox="0 0 '
        self.header = self.header + w + ' ' + h + '">' + "\n"
        self.header = self.header + '<title>TS SVG Art Generator</title>' + "\n"
        self.header = self.header + '<desc>SVG Art Creator by Thomas Suchyta on ' + today + "\n"
        self.header = self.header + 'Filename: ' + self.filename + "\n" 
        self.header = self.header + 'Copyright ' + year + '</desc>' + "\n"

        self.groupStart = '<g id="group1" style="opacity:1">' + "\n"
        self.groupEnd = '</g>' + "\n"
        
        self.baseRect = '<g><rect id="baseRect" x="0" y="0" '
        self.baseRect = self.baseRect + 'width="' + w + '" '
        self.baseRect = self.baseRect + 'height="' + h + '" '
        self.baseRect = self.baseRect + 'style="fill:rgb(255,255,255)" /></g>' + "\n"

        self.footer = '</svg>' + "\n"

    def writeFile(self):
        file = open(self.filename, 'w')
        file.write(self.svgCode)
        file.close()
        