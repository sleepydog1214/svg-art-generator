
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

        self.colorList = list(self.colors.keys())
        #mid = int(len(self.colorList) / 2)
        #rgb = colorList[mid]
        rgb = "ffffff"

        BaseSVG.__init__(self, self.width, self.height, rgb)

        self.segments = self.ip.getSegments()
        self.contours = self.ip.getContours()


    # ************************************************************************
    # drawSVG() -
    # ************************************************************************
    def drawSVG(self):
        self.svgCode = self.header
        self.svgCode += self.baseGroupStart
        self.svgCode += self.baseRect

        #self.drawShapes()
        #self.drawSegmentShapes()
        #aColor = self.colorList[0]
        #self.drawSegments(aColor, "15", 1, "0.75")
        #self.drawSegments("150", "2")
        #self.drawSegments("95", "1.5")
        self.drawSegments("50", "1")
        self.drawSegments("0", "0.5")
        self.drawContours()

        self.svgCode += self.baseGroupEnd
        self.svgCode += self.footer

        self.writeFile()


    # ************************************************************************
    # drawContours() -
    # ************************************************************************
    def drawContours(self):

        self.startGroup()

        for aContour in self.contours:
            polyline = '<polyline id="polyline' + str(ArtSVG.polylineIdx) + '" points="'
            ArtSVG.polylineIdx += 1

            for pixel in aContour:
                x = pixel[0]
                y = pixel[1]
                polyline += ' ' + x + ',' + y
            polyline += '" style="fill:none;stroke:rgb(0,0,0); stroke-width:1;"'
            polyline += '/>' + "\n"
            self.svgCode += polyline

        self.endGroup()


    # ************************************************************************
    # drawSegments() -
    # ************************************************************************
    def drawSegments(self, color, width, setOpacity = 0, opacity = ""):
        self.startGroup()

        for aSegment in self.segments:
            polyline = '<polyline id="polyline' + str(ArtSVG.polylineIdx) + '" points="'
            ArtSVG.polylineIdx += 1

            idx = 1;
            for pixel in aSegment:
                if idx % 2 == 0:
                    x = pixel[0]
                    y = pixel[1]
                    polyline += ' ' + x + ',' + y
                idx = idx + 1

            polyline += '" style="fill:none;'
            if setOpacity == 1:
                polyline += 'opacity:' + opacity + ';'
                polyline += 'stroke:#' + color + ';'
            else:
                polyline += 'stroke:rgb(' + color + ',' + color + ',' + color + ');'
            polyline += 'stroke-width:' + width + ';"'
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

    def drawSegmentShapes(self):
        self.startGroup()

        for aSegment in self.segments:
            polygon = '<polygon id="polygon' + str(ArtSVG.polygonIdx) + '" points="'
            ArtSVG.polygonIdx += 1

            midPoint = int(len(aSegment) / 2)
            firstX = aSegment[0][0]
            firstY = aSegment[0][1]
            rgb = self.ip.getColorAtPixel(float(firstX), float(firstY))

            for i in range(len(aSegment)):
                x = aSegment[i][0]
                y = aSegment[i][1]
                polygon += ' ' + x + ',' + y

            polygon += ' ' + firstX + ',' + firstY
            polygon += '" style="fill:#' + rgb + ';'
            polygon += 'stroke(0,0,0);stroke-width:50;opacity:0.5" />' + "\n"
            self.svgCode += polygon

        self.endGroup()
