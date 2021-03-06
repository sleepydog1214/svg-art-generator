
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
    lineIdx = 1

    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, name):
        self.ip = ImageProcessing(name)

        self.width = self.ip.width
        self.height = self.ip.height

        rgb = "ffffff"

        BaseSVG.__init__(self, self.width, self.height, rgb)

        self.colorLines = self.ip.getPosterize()
        self.segments = self.ip.getSegments()
        self.contours = self.ip.getContours()


    # ************************************************************************
    # drawSVG() - Create the final svg file
    # ************************************************************************
    def drawSVG(self):
        self.svgCode = self.header
        self.svgCode += self.baseGroupStart
        self.svgCode += self.baseRect

        self.drawColorLines()
        self.drawSegments("0", "2")
        self.drawContours()

        self.svgCode += self.baseGroupEnd
        self.svgCode += self.footer

        self.writeFile()


    # ************************************************************************
    # drawContours() - Use the contour list to draw a set of polylines
    # ************************************************************************
    def drawContours(self):

        self.startGroup()

        for aContour in self.contours:
            polyline = '<polyline id="polyline' + str(ArtSVG.polylineIdx) + '" points="'
            ArtSVG.polylineIdx += 1

            for pixel in aContour:
                x = pixel[1]
                y = pixel[0]
                polyline += ' ' + x + ',' + y
            polyline += '" style="fill:none;stroke:rgb(0,0,0); stroke-width:2;"'
            polyline += '/>' + "\n"
            self.svgCode += polyline

        self.endGroup()


    # ************************************************************************
    # drawSegments() - Use the segment list to draw a set of polylines
    # ************************************************************************
    def drawSegments(self, color, width, setOpacity = 0, opacity = ""):
        self.startGroup()

        for aSegment in self.segments:
            polyline = '<polyline id="polyline' + str(ArtSVG.polylineIdx) + '" points="'
            ArtSVG.polylineIdx += 1

            idx = 1;
            for pixel in aSegment:
                if idx % 2 == 0:
                    x = pixel[1]
                    y = pixel[0]
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
    # drawColorLines() - Draw set of horizontal lines, really lines of color
    # ************************************************************************
    def drawColorLines(self):
        self.startGroup()
        
        idx = 1
        for aLine in self.colorLines:
            if idx % 6 == 1:
                line = '<line id = "line' + str(ArtSVG.lineIdx) + '" '
                ArtSVG.lineIdx += 1
                x1 = aLine[0] - 7
                y1 = aLine[1] - 7
                x2 = x1 + 7
                y2 = y1 + 7
                rgb = aLine[4]
                line += 'x1="' + str(x1) + '" '
                line += 'y1="' + str(y1) + '" '
                line += 'x2="' + str(x2) + '" '
                line += 'y2="' + str(y2) + '" '
                line += 'stroke-width="8" '
                line += 'stroke="#' + rgb + '" '
                line += '/>' + "\n"
                self.svgCode += line
            idx += 1
        
        self.endGroup()