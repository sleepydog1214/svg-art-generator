#!/usr/bin/python

import sys
from ArtSVG import ArtSVG
from Setup import Setup

# *****************************************************************************
# main() - Start the svg generator program
# To run on Windows command line:
# $ /c/ProgramData/Anaconda3/python main.py <filename>
# *****************************************************************************
def main():
    "Program start."

    setup = Setup()
    name = setup.GetArgs()

    artSVG = ArtSVG(name)
    artSVG.drawSVG()

    return


# *****************************************************************************
# Begin program
# *****************************************************************************
if __name__ == "__main__":
    main()
