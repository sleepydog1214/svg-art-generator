
# Use the scikit-image collection of algorithms, see scikit-image.org
# Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne,
# Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the scikit-image
# contributors. scikit-image: Image processing in Python. PeerJ 2:e453 (2014)
# http://dx.doi.org/10.7717/peerj.453
import skimage
from skimage.color import rgb2gray
from skimage import io, feature
from skimage.filters import roberts, sobel
import matplotlib.pyplot as plt
import numpy as np

#******************************************************************************
# ImageProcessing class -
#******************************************************************************
class ImageProcessing:
    "Class to handle scikit-image calls"

    #*************************************************************************
    # Constructor
    #*************************************************************************
    def __init__(self, name):
        try:
            self.fileArray = io.imread(name)
            print(self.fileArray.shape)
            print(self.fileArray.size)

        except IOError:
            print("File %s open error" % name)

    #*************************************************************************
    # getEdges() - return ndarray of edge values
    #*************************************************************************
    def getEdges(self):
        imgGray = rgb2gray(self.fileArray)

        # Detect edges, 3 possible algorithms
        #self.edges = feature.canny(self.imgGray)
        #self.edges = roberts(self.imgGray)
        edges = sobel(imgGray)

        return edges

    #*************************************************************************
    # getColors() - return dictionary of rgb colors in original image
    #*************************************************************************
    def getColors(self):
        # The image is a 3-dimensional array, with the 3 r,g,b pixel
        # values at the [x,y] pixel location. Iterate through the
        # array and create a table of the number of pixels for each
        # rgb color.
        colorList = {}

        it = np.nditer(self.fileArray, flags=['multi_index'])
        while not it.finished:
            r = hex(it[0])
            it.iternext()
            g = hex(it[0])
            it.iternext()
            b = hex(it[0])

            # Create an rgb string and the rgb hex value. The rgb
            # string will be the key into the color table.
            rgbStr = r[2:] + g[2:] + b[2:]
            #rgb = int(rgbStr, 16)

            if rgbStr in colorList:
                colorList[rgbStr] += 1
            else:
                colorList[rgbStr] = 1

            #print("0x%X " % rgb)
            it.iternext()

        return colorList
