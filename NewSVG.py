
from ImageProcessing import ImageProcessing

class NewSVG:
    "Class to create the new SVG files based on input image."

    def __init__(self, name):
        self.ip = ImageProcessing(name)
        self.edges = self.ip.getEdges()
        self.colors = self.ip.getColors()
        for key in self.colors:
            print(key, self.colors[key])
