
from ImageProcessing import ImageProcessing
from BaseSVG import BaseSVG
import math


# *****************************************************************************
# ArtSVG class -
# *****************************************************************************
class ArtSVG(BaseSVG):
    "Class to create the new SVG files based on input image."
    
    polylineIdx = 1
    polygonIdx = 1

    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, name):
        self.ip = ImageProcessing(name)

        self.width = self.ip.width
        self.height = self.ip.height
        self.colors = self.ip.getColors()
        
        colorList = list(self.colors.keys())
        mid = int(len(colorList) / 2)
        rgb = colorList[mid]
            
        BaseSVG.__init__(self, self.width, self.height, rgb)

        self.contours = self.ip.getContours()


    # ************************************************************************
    # drawSVG() - 
    # ************************************************************************
    def drawSVG(self):
        self.svgCode = self.header
        self.svgCode += self.baseGroupStart
        self.svgCode += self.baseRect

        self.drawShapes()
        self.drawLines()

        self.svgCode += self.baseGroupEnd
        self.svgCode += self.footer

        self.writeFile()


    # ************************************************************************
    # drawLines() - 
    # ************************************************************************
    def drawLines(self):
        self.startGroup()
        
        for aContour in self.contours:
            polyline = '<polyline id="polyline' + str(ArtSVG.polylineIdx) + '" points="'
            ArtSVG.polylineIdx += 1
            
            for pixel in aContour:
                x = pixel[0]
                y = pixel[1]
                polyline += ' ' + x + ',' + y
            polyline += '" style="fill:none;stroke:rgb(0,0,0); stroke-width:2;"'
            polyline += '/>' + "\n"
            self.svgCode += polyline
            
        self.endGroup()
            

    # ************************************************************************
    # drawShapes() - 
    # ************************************************************************
    def drawShapes(self):
        self.startGroup()

        for aContour in self.contours:
            polygon = '<polygon id="polygon' + str(ArtSVG.polygonIdx) + '" points="'
            ArtSVG.polygonIdx += 1
            
            midPoint = int(len(aContour) / 2)
            firstX = aContour[0][0]
            firstY = aContour[0][1]
            rgb = aContour[0][2]
            
            for i in range(len(aContour)):
                x = aContour[i][0]
                y = aContour[i][1]
                
                if (i == midPoint):
                    rgb = aContour[i][2]
                
                polygon += ' ' + x + ',' + y

            polygon += ' ' + firstX + ',' + firstY
            polygon += '" style="fill:#' + rgb + ';'
            polygon += 'stroke(0,0,0);stroke-width:1;" />' + "\n"
            self.svgCode += polygon

        self.endGroup()
        
        