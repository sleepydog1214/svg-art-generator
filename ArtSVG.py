
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
        self.colors = self.ip.getColors()

        self.colorList = list(self.colors.keys())
        mid = int(len(self.colorList) / 2)
        rgb = "ffffff"

        BaseSVG.__init__(self, self.width, self.height, rgb)

        self.segments = self.ip.getSegments()
        self.contours = self.ip.getContours()
        self.colorLines = self.ip.getPosterize()


    # ************************************************************************
    # drawSVG() - Create the final svg file
    # ************************************************************************
    def drawSVG(self):
        self.svgCode = self.header
        self.svgCode += self.baseGroupStart
        self.svgCode += self.baseRect

        # 7/2/2107 - best combination for desired visual results so far, but
        # need to speed the code up. One 600 px wide jpeg takes 20 minutes to
        # process and another 20 minutes to show in Inkscape.
        self.drawColorLines()
        #self.drawShapes()
        #self.drawSegmentShapes()
        #aColor = self.colorList[0]
        #self.drawSegments(aColor, "0.75", 1, "0.75")
        #self.drawSegments("150", "2")
        #self.drawSegments("95", "1.5")
        #self.drawSegments("50", "0.5")
        self.drawSegments("0", "1")
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
            polyline += '" style="fill:none;stroke:rgb(0,0,0); stroke-width:1;"'
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
        
        for aLine in self.colorLines:
            line = '<line id = "line' + str(ArtSVG.lineIdx) + '" '
            ArtSVG.lineIdx += 1
            x1 = str(aLine[0])
            y1 = str(aLine[1])
            x2 = str(aLine[2])
            y2 = str(aLine[3])
            rgb = aLine[4]
            line += 'x1="' + x1 + '" '
            line += 'y1="' + y1 + '" '
            line += 'x2="' + x2 + '" '
            line += 'y2="' + y2 + '" '
            line += 'stroke-width="1" '
            line += 'stroke="#' + rgb + '" '
            line += '/>' + "\n"
            self.svgCode += line
        
        self.endGroup()
    
    
    # ************************************************************************
    # drawShapes() - Use the contour list to draw a set of polygons
    # ************************************************************************
    def drawShapes(self):
        self.startGroup()

        for aContour in self.contours:
            polygon = '<polygon id="polygon' + str(ArtSVG.polygonIdx) + '" points="'
            ArtSVG.polygonIdx += 1

            midPoint = int(len(aContour) / 2)
            firstX = aContour[0][1]
            firstY = aContour[0][0]
            rgb = aContour[0][2]

            for i in range(len(aContour)):
                x = aContour[i][1]
                y = aContour[i][0]

                if (i == midPoint):
                    rgb = aContour[i][2]

                polygon += ' ' + x + ',' + y

            polygon += ' ' + firstX + ',' + firstY
            polygon += '" style="fill:#' + rgb + ';'
            polygon += 'stroke(0,0,0);stroke-width:1;" />' + "\n"
            self.svgCode += polygon

        self.endGroup()


    # ************************************************************************
    # drawSegmentShapes() - Use the segment list to draw a set of polygons
    # ************************************************************************
    def drawSegmentShapes(self):
        self.startGroup()

        for aSegment in self.segments:
            polygon = '<polygon id="polygon' + str(ArtSVG.polygonIdx) + '" points="'
            ArtSVG.polygonIdx += 1

            midPoint = int(len(aSegment) / 2)
            firstX = aSegment[0][1]
            firstY = aSegment[0][0]
            rgb = self.ip.getColorAtPixel(float(firstY), float(firstX))

            for i in range(len(aSegment)):
                x = aSegment[i][1]
                y = aSegment[i][0]
                polygon += ' ' + x + ',' + y

            polygon += ' ' + firstX + ',' + firstY
            polygon += '" style="fill:#' + rgb + ';'
            polygon += 'stroke(0,0,0);stroke-width:50;opacity:0.5" />' + "\n"
            self.svgCode += polygon

        self.endGroup()
