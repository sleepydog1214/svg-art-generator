#!/usr/bin/python

import sys
from ArtSVG import ArtSVG
# import pudb; pu.db

# ******************************************************************************
# getUserFile() -
# *****************************************************************************
def getUserFile():
    "This gets the name of the image file to process."
    try:
        name = input("enter image file: ")
        tmp = name.lower()

        # file must be a jpeg or png file
        if not tmp.endswith('.jpg') and \
           not tmp.endswith('.jpeg') and \
           not tmp.endswith('.png'):
            raise IOError

    except IOError:
        print("Input IO error (file must be jpg or png)")
        sys.exit(1)

    return name

# *****************************************************************************
# main() -
# *****************************************************************************
def main():
    "Program start."

    name = getUserFile()

    artSVG = ArtSVG(name)
    artSVG.drawSVG()

    return

# *****************************************************************************
# Begin program
# *****************************************************************************
if __name__ == "__main__":
    main()
