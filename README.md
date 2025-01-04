## Introduction

A python program to generate svg files based on a specific art style.

Uses the scikit-image collection of algorithms. See http://scikit-image.org.

Stéfan van der Walt, Johannes L. Schönberger, Juan Nunez-Iglesias, François Boulogne, Joshua D. Warner, Neil Yager, Emmanuelle Gouillart, Tony Yu and the scikit-image contributors. scikit-image: Image processing in Python. PeerJ 2:e453 (2014) http://dx.doi.org/10.7717/peerj.453

## License
[The MIT License](LICENSE.txt)

To run requires Anaconda 3 and skimage:

$ pyenv versions
* anaconda3-2024.10-1 

$conda install -c conda-forge scikit-image

Then make a gen_svg directory. 

To test:

$python main.py images/check10x10.png
