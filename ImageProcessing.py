# Use the scikit-image collection of algorithms, see scikit-image.org
# Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias,
# François Boulogne,
# Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the
# scikit-image
# contributors. scikit-image: Image processing in Python. PeerJ 2:e453 (2014)
# http://dx.doi.org/10.7717/peerj.453

from skimage.color import rgb2gray
from skimage import io
from skimage.measure import find_contours, approximate_polygon
from skimage.exposure import rescale_intensity
from skimage.filters import sobel
from skimage.morphology import watershed
import numpy as np
import math
import sys
from pygments.lexers.esoteric import CAmkESLexer
from decorator import append

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
            self.segmentList = []

            self.width = self.fileArray.shape[0]
            self.height = self.fileArray.shape[1]
            self.depth = self.fileArray.shape[2]

            # print(self.width)
            # print(self.height)

        except IOError:
            print("File %s open error" % name)
            sys.exit(1)

    # ************************************************************************
    # getContours() - return ndarray of contour values
    # ************************************************************************
    def getContours(self):
        tmpImage = rescale_intensity(self.fileArray)
        imgGray = rgb2gray(tmpImage)
        return self.findContours(imgGray)
        
    def findContours(self, imgArray):
        contourList = []
        contours = find_contours(imgArray, 0.5)

        for c in contours:
            # print(c.shape)
            aContour = []
            p = approximate_polygon(c, 0.8)

            #it = np.nditer(c, flags=['multi_index'])
            it = np.nditer(p, flags=['multi_index'])
            while not it.finished:
                x = it[0]
                xStr = str(x)
                
                it.iternext()

                y = it[0]
                yStr = str(y)

                it.iternext()

                rgb = self.getColorAtPixel(x, y)
                xyz = (xStr, yStr, rgb)

                aContour.append(xyz)

            contourList.append(aContour)

        # print(contours)
        return contourList

    def getSegments(self):
        segmentList = []
        
        imgGray = rgb2gray(self.fileArray)
        elevationMap = sobel(imgGray)

        markers = np.zeros_like(imgGray)

        for (i, x) in enumerate(imgGray):
            for(j, y) in enumerate(x):
                if imgGray[i][j] < 0.1:
                    markers[i][j] = 1.0
                elif imgGray[i][j] >= 0.1 and imgGray[i][j] < 0.2:
                    markers[i][j] = 2.0
                elif imgGray[i][j] >= 0.2 and imgGray[i][j] < 0.3:
                    markers[i][j] = 3.0
                elif imgGray[i][j] >= 0.3 and imgGray[i][j] < 0.4:
                    markers[i][j] = 4.0
                elif imgGray[i][j] >= 0.4 and imgGray[i][j] < 0.5:
                    markers[i][j] = 5.0
                elif imgGray[i][j] >= 0.5 and imgGray[i][j] < 0.6:
                    markers[i][j] = 6.0
                elif imgGray[i][j] >= 0.6 and imgGray[i][j] < 0.7:
                    markers[i][j] = 7.0
                elif imgGray[i][j] >= 0.7 and imgGray[i][j] < 0.8:
                    markers[i][j] = 8.0
                elif imgGray[i][j] >= 0.8 and imgGray[i][j] < 0.9:
                    markers[i][j] = 9.0
                else:
                    markers[i][j] = 10.0
                
        segmentation = watershed(elevationMap, markers)
        
        #initialize the segment list
        shape = segmentation.shape
        numOfCols = shape[0]
        numOfRows = shape[1]
        for i in range(numOfCols):
            segmentCols = []
            for j in range(numOfRows):
                segmentCols.append(0)
            segmentList.append(segmentCols)
            
        # fill in the columns
        x = 0
        y = 0
        for s in np.nditer(segmentation, order='F'):
            if x == 0:
                currPoint = s
            
            if s != currPoint:
                    segmentList[x][y] = 1
                    currPoint = s

            x = x + 1
            if x % numOfCols == 0:
                x = 0
                y = y + 1

        # fill in the rows
        x = 0
        y = 0
        for s in np.nditer(segmentation, order='C'):
            if y == 0:
                currPoint = s

            if s != currPoint:
                    segmentList[x][y] = 1
                    currPoint = s

            y = y + 1
            if y % numOfRows == 0:
                y = 0
                x = x + 1

        #print(segmentList)
        return self.findContours(segmentList)
            
        
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
    
    
    # ************************************************************************
    # getColorAtPixel() - return rgb color at requested pixel location
    # ************************************************************************
    def getColorAtPixel(self, x, y):
        
        x = math.ceil(x)
        y = math.ceil(y)
        
        if x > self.width:
            x = self.width
        if y > self.height:
            y = self.height
            
        r = hex(self.fileArray[x, y, 0])
        g = hex(self.fileArray[x, y, 1])
        b = hex(self.fileArray[x, y, 2])
        rgbStr = r[2:] + g[2:] + b[2:]
        return rgbStr
                    