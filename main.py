#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 16:43:46 2019

@author: jude
"""

import numpy as np
import matplotlib.pyplot as plt
import random

canvaHeight = 50 # px
canvaWidth = 50 # px
 
global cellBornMin, cellBornMax, cellOverpop

cellOverpop = 3
cellBornMin = 2
cellSolitude = cellBornMin
cellBornMax = cellOverpop

def createCanva(canvaHeight,canvaWidth):
    return np.zeros((canvaHeight,canvaWidth), dtype=int)

def randomInit(canva):
    for x in np.nditer(canva, op_flags=['readwrite']):
        x[...] = random.getrandbits(1)
    return canva
    
def lifeOrDeath(canva,x,y):
    sumCell = \
        canva[x - 1, y - 1] + canva[x + 0, y - 1]   + canva[x + 1, y - 1] + \
        canva[x - 1, y + 0]                         + canva[x + 1, y + 0] + \
        canva[x - 1, y + 1] + canva[x + 0, y + 1]   + canva[x + 1, y + 1]
    # death by overpopulation
    if canva[x,y] and sumCell >= cellOverpop:
        return 0
    elif canva[x,y] and sumCell <= cellSolitude:
        return 0
    # born
    elif not canva[x,y] and all([sumCell >= cellBornMin,sumCell <= cellBornMax]):
        return 1
    else:
        return canva[x,y] 

def applyNextGen(canva):
    canvaTmp = canva
    for x in range(len(canva) - 1 ):
        for y in range(len(canva[x]) - 1):
            canvaTmp[x,y]=lifeOrDeath(canva, x, y)
    return canvaTmp

    
    
# def __main__():
canva = createCanva(canvaHeight,canvaWidth)
canva = randomInit(canva)
plt.imshow(canva)

canva = applyNextGen(canva)
plt.imshow(canva)