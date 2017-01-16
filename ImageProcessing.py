
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

#******************************************************************************
# ImageProcessing class -
#******************************************************************************
class ImageProcessing:
    "Class to handle scikit-image calls"

    def __init__(self, name):
        try:
            self.fileArray = io.imread(name)
            print(self.fileArray.shape)
            print(self.fileArray.size)


        except IOError:
            print("File %s open error" % name)

    def getEdges(self):
        # convert rgb image to 2D grayscale
        imgGray = rgb2gray(self.fileArray)

        # Detect edges, 3 possible algorithms
        #self.edges = feature.canny(self.imgGray)
        #self.edges = roberts(self.imgGray)
        edges = sobel(imgGray)

        print(edges)
        io.imshow(edges)
        plt.tight_layout()
        plt.show()
        return edges
