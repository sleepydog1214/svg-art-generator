
from ImageProcessing import ImageProcessing
from BaseSVG import BaseSVG


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
        BaseSVG.__init__(self, self.width, self.height)

        self.contours = self.ip.getContours()
        self.colors = self.ip.getColors()


    # ************************************************************************
    # drawSVG() - 
    # ************************************************************************
    def drawSVG(self):
        self.svgCode = self.header
        self.svgCode += self.baseRect
        self.svgCode += self.baseGroupStart

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
                polyline = polyline + ' ' + x + ',' + y
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
            rgb = aContour[0][2]
            
            for i in range(len(aContour)):
                x = aContour[i][0]
                y = aContour[i][1]
                
                if (i == midPoint):
                    rgb = aContour[i][2]
                
                polygon = polygon + ' ' + x + ',' + y

            polygon += '" style="fill:#' + rgb + ';'
            polygon += 'stroke(0,0,0);stroke-width:1;" />' + "\n"
            self.svgCode += polygon

        self.endGroup()
             
