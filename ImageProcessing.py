# Use the scikit-image collection of algorithms, see scikit-image.org
# Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias,
# François Boulogne,
# Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the
# scikit-image
# contributors. scikit-image: Image processing in Python. PeerJ 2:e453 (2014)
# http://dx.doi.org/10.7717/peerj.453

from skimage.color import rgb2gray
from skimage import io
from skimage.measure import find_contours
from skimage.exposure import rescale_intensity
import numpy as np

# *****************************************************************************
# ImageProcessing class -
# *****************************************************************************


class ImageProcessing:
    "Class to handle scikit-image calls"

    # ************************************************************************
    # Constructor
    # ************************************************************************
    def __init__(self, name):
        try:
            self.fileArray = io.imread(name)

            self.width = self.fileArray.shape[0]
            self.height = self.fileArray.shape[1]

            # print(self.width)
            # print(self.height)

        except IOError:
            print("File %s open error" % name)

    # ************************************************************************
    # getContours() - return ndarray of contour values
    # ************************************************************************
    def getContours(self):
        contourList = []

        tmpImage = rescale_intensity(self.fileArray)
        imgGray = rgb2gray(tmpImage)

        contours = find_contours(imgGray, 0.5)

        for c in contours:
            # print(c.shape)
            it = np.nditer(c, flags=['multi_index'])
            while not it.finished:
                x = str(it[0])
                it.iternext()
                y = str(it[0])
                it.iternext()
                xy = x + ',' + y
                contourList.append(xy)

        # print(contours)
        return contourList

    # ************************************************************************
    # getColors() - return dictionary of rgb colors in original image
    # ************************************************************************
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
            # rgb = int(rgbStr, 16)

            if rgbStr in colorList:
                colorList[rgbStr] += 1
            else:
                colorList[rgbStr] = 1

            # print("0x%X " % rgb)
            it.iternext()

        return colorList
