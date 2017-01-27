import math
import numpy as np
import array
from math import sqrt as sqrt
import random
import sys
import cv2

from skimage.io import imread
import matplotlib.pyplot as plt
from skimage.exposure import histogram

from skimage.filters.rank import threshold
from skimage.filters.rank import otsu
from skimage.morphology import erosion, dilation
from skimage.morphology import square, diamond, disk  # strukturni elementi
from skimage.color import rgb2gray, gray2rgb

from skimage.measure import label
from skimage.measure import regionprops


# imporujemo sve moje f-je
from parseTextFile import *
from parsePicture import *
from Geometry import *
from sorting import *

pathsAndCount = getAllFilePathsAndCount('dataset/info.txt')
paths = pathsAndCount[0]
examplesCount = pathsAndCount[1]
styles = pathsAndCount[2]



for idx,path in enumerate(paths):
    img = getImage(path)

    if styles[idx]=='thin':
        thickness = 1
    else:
        thickness = 3

    img2 = filterColor(img)
    canny = cv2.Canny(img2,90,150)
    str_elem = disk(thickness)  # parametar je poluprecnik diska
    edges = dilation(canny,selem=str_elem)/255.0
    # plt.imshow(edges, 'gray')
    # plt.show()


    [start,horizontal,vertical] = rotateSistem(edges,path)

    (fields,fieldNum) = findFields(edges, [start,horizontal,vertical],path )
    if fieldNum==100:
        rezultat = result(fields,path)
