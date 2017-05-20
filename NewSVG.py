
from ImageProcessing import ImageProcessing
from BaseSVG import BaseSVG


class NewSVG(BaseSVG):
    "Class to create the new SVG files based on input image."

    def __init__(self, name):
        self.ip = ImageProcessing(name)

        self.width = self.ip.width
        self.height = self.ip.height
        BaseSVG.__init__(self, self.width, self.height)

        self.contours = self.ip.getContours()
        self.colors = self.ip.getColors()


    def drawSVG(self):
        self.svgCode = self.header
        self.svgCode = self.svgCode + self.baseRect
        self.svgCode = self.svgCode + self.groupStart
        #self.drawLines()
        self.drawShapes()
        self.svgCode = self.svgCode + self.groupEnd
        self.svgCode = self.svgCode + self.footer
        self.writeFile()


    def drawLines(self):
        for aContour in self.contours:
            polyline = '<polyline id="polyline1" points="'
            for pixel in aContour:
                x = pixel[0]
                y = pixel[1]
                polyline = polyline + ' ' + x + ',' + y
            polyline = polyline + '''" style="fill:none;stroke:rgb(0,0,0);
stroke-width:1;"'''
            polyline = polyline + '/>' + "\n"
            self.svgCode = self.svgCode + polyline
            

    def drawShapes(self):
        for aCounter in self.contours:
            polygon = '<polygon id="polygon1" points="'
            for pixel in aCounter:
                x = pixel[0]
                y = pixel[1]
                rgb = pixel[2]
                polygon = polygon + ' ' + x + ',' + y
            polygon = polygon + '" style="fill:#' + rgb + ';stroke(0,0,0);stroke-width:1;" />' + "\n"
            self.svgCode = self.svgCode + polygon
             
