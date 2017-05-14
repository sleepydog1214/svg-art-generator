
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
        print(self.header)
        print(self.groupStart)
        self.drawLines()
        print(self.groupEnd)
        print(self.footer)

    def drawLines(self):
        polyline = '<polyline id="polyline1" points="'
        for line in self.contours:
            polyline = polyline + ' ' + line
        polyline = polyline + '''" style="fill:rgb(0,0,0);stroke:rgb(0,0,0);
stroke-width:1;"'''
        polyline = polyline + '/>'
        print(polyline)

    def __repr__(self):
        svg = ''
        for key in self.colors:
            svg = svg + ',' + str(key) + ',' + str(self.colors[key])
        svg = svg + "\n" + BaseSVG.__repr__(self)
        return svg
