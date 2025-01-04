import time
import math
import datetime

# *****************************************************************************
# BaseSVG class -
# *****************************************************************************
class BaseSVG:
    "Class to create a basic svg file"

    groupIdx = 1;
    
    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, width, height, rgb):
        w = str(width)
        h = str(height)

        timestamp = str(math.ceil(time.time()))
        today = datetime.date.today()
        year = str(today.year)
        today = str(today)
        
        self.filename = './gen_svg/tsart-generated-' + timestamp + '.svg'
        
        self.svgCode = ''
        
        self.header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + "\n"
        self.header += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">' + "\n"
        self.header += '<svg' + "\n"
        self.header += 'xmlns="http://www.w3.org/2000/svg"' + "\n"
        self.header += 'version="1.1"' + "\n"
        self.header += 'width="''' + w + '"' + "\n"
        self.header += '    height="' + h + '"' + "\n"
        self.header += '    viewBox="0 0 '
        self.header += w + ' ' + h + '">' + "\n"
        self.header += '<title>TS SVG Art Generator</title>' + "\n"
        self.header += '<desc>SVG Art Creator by Thomas Suchyta on ' + today + "\n"
        self.header += 'Filename: ' + self.filename + "\n" 
        self.header += 'Copyright ' + year + '</desc>' + "\n"

        self.baseGroupStart = '<g id="baseGroup" style="opacity:1">' + "\n"
        self.baseGroupEnd = '</g>' + "\n"
        
        self.baseRect = '<g><rect id="baseRect" x="0" y="0" '
        self.baseRect += 'width="' + w + '" '
        self.baseRect += 'height="' + h + '" '
        self.baseRect += 'style="fill:#' + str(rgb) + '" /></g>' + "\n"

        self.footer = '</svg>' + "\n"
        

    # ************************************************************************
    # startGroup() -  Start a svg group
    # ************************************************************************
    def startGroup(self):
        self.svgCode += '<g id="group' + str(BaseSVG.groupIdx) + '">'
        BaseSVG.groupIdx += 1
        

    # ************************************************************************
    # endGroup() - Close a svg group
    # ************************************************************************
    def endGroup(self):
        self.svgCode += '</g>' + "\n"


    # ************************************************************************
    # writeFile() - Write the svg file.
    # ************************************************************************
    def writeFile(self):
        file = open(self.filename, 'w')
        file.write(self.svgCode)
        file.close()
        