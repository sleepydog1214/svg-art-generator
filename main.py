#!/usr/bin/python

import os
from NewSVG import NewSVG

#******************************************************************************
# getUserFile() -
#******************************************************************************
def getUserFile():
    "This gets the name of the image file to process."
    try:
        name = input("enter image file:")
        tmp = name.lower()

        #file must be a jpeg or png file
        if not tmp.endswith('.jpg') and \
           not tmp.endswith('.jpeg') and \
           not tmp.endswith('.png'):
           raise IOError

    except IOError:
        print("Input IO error (file must be jpg or png)")

    return name

#******************************************************************************
# main() -
#******************************************************************************
def main():
    "Program start."
    print("begin program")

    name = getUserFile()
    print(name)

    new_svg = NewSVG(name)

    return

#******************************************************************************
# Begin program
#******************************************************************************
if __name__ == "__main__":
    main()
