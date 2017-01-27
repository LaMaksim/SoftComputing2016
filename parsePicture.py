from skimage.io import imread
import matplotlib.pyplot as plt

from skimage.morphology import erosion
from skimage.morphology import square, diamond, disk  # strukturni elementi
from skimage.morphology import remove_small_objects
from skimage.color import rgb2gray,gray2rgb
import cv2

from skimage.measure import label
from skimage.measure import regionprops

import math
import numpy as np
from math import sqrt as sqrt

from Geometry import *
from sorting import *

class expando(object): pass

def getImage(path):
    img = imread(path)
    # plt.imshow(img)
    # plt.show()
    return img

def filterImage(img):
    img[:, :, [0,1] ] = img[:, :, [2,2] ] # skidamo crveno-zelene fleke
    return img


# svaki piksel se oboji njegovom najsvetlijom komponentom (rgb)
def filterColor(img):
    # img[:, :, :] = img[:, :, [2, 2]]  # skidamo crveno-zelene fleke
    rows = img.shape[0]
    cols = img.shape[1]

    row = 0
    while row<rows:
        col = 0
        while col<cols:
            rgb = img[row,col,:]
            max = np.amax(rgb)

            img[row,col,:] = [max,max,max]

            col = col +1
        row = row+1
    return img


# Metoda vraca startni cosak, horizontalni i vertikalni pravac, odredjeno je zakrivljenje...
def rotateSistem(edges,path):
    regions = regionprops(label(edges))  # regionprops ~ labeling ~ segmentation

    max = -1
    for region in regions:
        if region.area > max:
            max = region.area
            maxReg = region

    topY = maxReg.bbox[0]+1
    leftX = maxReg.bbox[1]+1
    bottomY = maxReg.bbox[2]-1
    rightX = maxReg.bbox[3]-1

    # trazimo leftY, spustamo se duz svoje vertikale dok ne dodjemo do bele tacke
    leftY = topY
    while leftY<=bottomY and edges[leftY,leftX]==0:
        # print 'leftY: ',leftY
        leftY = leftY+1

    #isto i za rightY, topX, bottomX
    rightY = topY
    while rightY<=bottomY and edges[rightY,rightX]==0:
        # print 'rightY: ', rightY
        rightY = rightY + 1

    topX = rightX
    while topX>=leftX and edges[topY,topX] == 0:
        # print 'topX: ', topX
        topX = topX - 1

    bottomX = leftX
    while bottomX<=rightX and  edges[bottomY,bottomX] == 0:
        # print 'bottomX: ', bottomX
        bottomX = bottomX + 1

    # leva mala rotacija
    if leftY<rightY:
        start = (leftX,leftY)
        horizontal = (topX,topY)
        vertical = (bottomX,bottomY)
    # desna mala rotacija
    else:
        start = (topX,topY)
        horizontal = (rightX,rightY)
        vertical = (leftX,leftY)

    return [start,horizontal,vertical]


# edges - slika na kojoj su istaknute ivice
# rotation = tacke koje predstavljaju centralnu tacku koordinatnog sistema, krajnju tacku horizontalnog i vertikalnog vektora
# retVal[0] - sva polja matrice, poredjana po horizontali i vertikali
# retVal[1] - broj nadjenih regiona, 100 = ok, 0=failure
def findFields(edges, rotation,path):
    start = rotation[0]
    horizontal = rotation[1]
    vertical = rotation[2]


    invertEdge = 1 - edges


    regions = regionprops(label(invertEdge))  # regionprops ~ labeling ~ segmentation

    cnt = 0
    regioni = []
    for region in regions:

        teziste = [(region.bbox[0]+region.bbox[2])/2 , (region.bbox[1]+region.bbox[3])/2]

        _x = pnt2line([teziste[1],teziste[0]],start,horizontal)
        _y = pnt2line([teziste[1],teziste[0]], start, vertical)

        if _x>0 and _x<1 and _y>0 and _y < 1 and region.area>60 and region.area<4000:
            cnt = cnt + 1

            field = expando()
            field.x = _x
            field.y = _y
            field.content = region
            regioni.append(field)

    retVal = ()
    if cnt==100:

        regioni = sortSubList(regioni,0,100,'y')

        red = 0
        while red < 10:
            regioni = sortSubList(regioni,10*red,10*red+10,'x')
            red = red+1

        retVal =(regioni,100) # regioni su poredjani po 1) Vrsti, 2) Koloni

    else:
        retVal = ([], 0)

    # print 'Path:', path, ', fields: ', cnt
    # plt.imshow(invertEdge, 'gray')
    # plt.show()

    return retVal # regioni su poredjani po 1) Vrsti, 2) Koloni, i drugi parametar je njihov broj


def result(fields, path):
    img = getImage(path)

    rezultat = []
    for idx,field in enumerate(fields):
        da = ne = 0
        for tacka in field.content.coords:
            if isColor(img,tacka[0],tacka[1]):
                da = da+1
            else:
                ne = ne +1

        if da>ne:
            rezultat.append('*')
        else:
            rezultat.append('o')

    rezultat = np.array(rezultat).reshape(10,10)
    np.savetxt(path+'.txt',rezultat,fmt="%s")
    return rezultat;




def isColor(img, row, col):
    r = img[row,col,0]
    g = img[row,col,1]
    b = img[row,col,2]

    avg = r/3 + b/3 + g/3
    max = 1.1*avg
    min = 0.9*avg

    if r>max or r<min or g>max or g<min or b>max or b<min:
        return True
    else:
        return False
