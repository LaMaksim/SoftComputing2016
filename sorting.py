import math
import numpy as np
import array
from math import sqrt as sqrt
import random
import sys
import cv2

from skimage.measure import label
from skimage.measure import regionprops


# imporujemo sve moje f-je
from parseTextFile import *
from parsePicture import *
from Geometry import *

class expando(object): pass


def poX(element):
    return element.x

def poY(element):
    return element.y


def sortSubList(lista,begin,end,dimenzija):
    newList = lista[begin:end]


    if(dimenzija=='x'):
        newList.sort(key=poX)
    if (dimenzija == 'y'):
        newList.sort(key=poY)

    lista[begin:end] = newList
    return  lista
