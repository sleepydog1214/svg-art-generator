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
from skimage.restoration import denoise_tv_bregman, denoise_tv_chambolle
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
            # Convert input image into np array
            self.fileArray = io.imread(name)

            # Save the dimensions of the image
            self.height = self.fileArray.shape[0]
            self.width = self.fileArray.shape[1]
            self.depth = self.fileArray.shape[2]
            self.points = []
            self.posterArray = []


        except IOError:
            print("File %s open error" % name)
            sys.exit(1)


    # ************************************************************************
    # getContours() - return ndarray of contour values
    # ************************************************************************
    def getContours(self):
        # Increase color intensity prior to convertung to a grayscale
        tmpImage = rescale_intensity(self.fileArray)
        imgGray = rgb2gray(tmpImage)
        return self.findContours(imgGray)


    # ************************************************************************
    # findContours() - return ndarray of contour values
    # ************************************************************************
    def findContours(self, imgArray):
        contourList = []
        contours = find_contours(imgArray, 0.5)

        for c in contours:
            aContour = []
            
            # Concert the contour to a polygon
            p = approximate_polygon(c, 0.8)

            # Save each x,y point and rgb color in the contour/polygon
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

        return contourList


    # ************************************************************************
    # getSegments() - Find segments through firsts finding the elevation map,
    #                 then dividing the grayscale into 10 different gray values.
    #                 The gray value markers and elevation map are used to find
    #                 each distinct segment. Equivalent values in the segmentation
    #                 are grouped together to build the segment list.
    # ************************************************************************
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
            r = hex(int(it[0]))
            it.iternext()
            g = hex(int(it[0]))
            it.iternext()
            b = hex(int(it[0]))

            # Create an rgb string and the rgb hex value. The rgb
            # string will be the key into the color table.
            rgbStr = r[2:].zfill(2) + g[2:].zfill(2) + b[2:].zfill(2)
            # rgb = int(rgbStr, 16)

            if rgbStr in colorList:
                colorList[rgbStr] += 1
            else:
                colorList[rgbStr] = 1

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

        r = hex(int(self.fileArray[x, y, 0]))
        g = hex(int(self.fileArray[x, y, 1]))
        b = hex(int(self.fileArray[x, y, 2]))
        rgbStr = r[2:] + g[2:] + b[2:]
        return rgbStr


    # ************************************************************************
    # getPosterize() - Convert image to a posterized version of 25 colors
    # ************************************************************************
    def getPosterize(self):
        # Set number of colors sto posterize
        n = 8

        # List all colors, 0 to 255, a list of size 256
        indices = np.arange(0,256)

        # Get a divider to quantize the colors, 10.2 for n = 25
        # Evenly divide the values from 0 to 255, by n + 1, take the
        # second value in that array
        divider = np.linspace(0,255,n+1)[1]

        # Get the set of quantization colors
        # A list of size n, evenly spaced between 0 and 255
        quantiz = np.int0(np.linspace(0,255,n))

        # Set the color levels
        # Take each value in indices, divide by divider, convert the result
        # to ints.
        # Then clip (limit) each value to a value between 0 and 24
        color_levels = np.clip(np.int0(indices/divider),0,n-1)

        # Create the palette
        # Replace each value in color_levels to the value in the same location
        # in the quantiz list
        palette = quantiz[color_levels]

        # Apply the palette to the image
        # Replace each color value in the image with its corresponding color
        # at that color value location in palette
        im2 = palette[self.fileArray]
        self.posterArray = im2

        # Now need a column size list where each entry in the list is an
        # array of x,y start point, x,y end point, and fill color
        # [[[0,0, 5,0, afafaf], [6,0, 12,0, ef0022], [13,0, 25,0, ffaaff]],
        #  [[0,1, 8,1, 554433], [9,1, 15,1, 99ddaa], [16,1, 25,1, 11aa44]]]
        yIdx = 1
        x = 1
        y = 0
        currentRGB = ""
        startX = 0
        startY = 0
        lineList = []
        it = np.nditer(im2, flags=['multi_index'])
        while not it.finished:
            r = hex(int(it[0]))
            it.iternext()
            g = hex(int(it[0]))
            it.iternext()
            b = hex(int(it[0]))
            rgbStr = r[2:].zfill(2) + g[2:].zfill(2) + b[2:].zfill(2)

            if x == 1:
                startX = 0
                startY = y
                currentRGB = rgbStr

            elif rgbStr != currentRGB and startY == y:
                aLine = [startX, startY, x - 1, y, currentRGB]
                onePoint = [x - 1, y]
                self.points.append(onePoint)
                lineList.append(aLine)
                startX = x - 1
                startY = y
                currentRGB = rgbStr

            if yIdx % self.width == 0:
                aLine = [startX, startY, x, y, rgbStr]
                lineList.append(aLine)
                y += 1
                yIdx = 1
            else:
                yIdx += 1

            if x % self.width == 0:
                x = 1
            else:
                x += 1

            it.iternext()

        return lineList
        
