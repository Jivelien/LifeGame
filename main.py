import numpy as np
import matplotlib.pyplot as plt
import random
import cv2
from scipy import ndimage
from time import sleep

def init():
    global canvaY, canvaX, cellBornMin, cellSolitude, cellBornMax, cellOverpop
    canvaY = 50 # px
    canvaX = 50 # px
    cellOverpop = 3
    cellBornMin = 2
    cellSolitude = cellBornMin
    cellBornMax = cellOverpop

def createCanva():
    return np.zeros((canvaY,canvaX), dtype='uint8')

def randomInit(canva):
    for x in np.nditer(canva, op_flags=['readwrite']):
        x[...] = random.getrandbits(1)
    return canva
    
def lifeOrDeath(canva,y,x):
    sumCell = \
        canva[(y - 1)%canvaY, (x - 1)%canvaX] + canva[(y + 0)%canvaY, (x - 1)%canvaX]   + canva[(y + 1)%canvaY, (x - 1)%canvaX] + \
        canva[(y - 1)%canvaY, (x + 0)%canvaX]                                           + canva[(y + 1)%canvaY, (x + 0)%canvaX] + \
        canva[(y - 1)%canvaY, (x + 1)%canvaX] + canva[(y + 0)%canvaY, (x + 1)%canvaX]   + canva[(y + 1)%canvaY, (x + 1)%canvaX]
    # death by overpopulation
    if canva[y,x] and sumCell > cellOverpop:
        return 0
    # death by isolation
    elif canva[y,x] and sumCell < cellSolitude:
        return 0
    # born
    elif not canva[y,x] and all([sumCell > cellBornMin,sumCell <= cellBornMax]):
        return 1
    else:
        return canva[y,x] 
    
def applyNextGen(canva):
    canvaTmp = createCanva()
    for y in range(canvaY):
        for x in range(canvaX):
            canvaTmp[y,x]=lifeOrDeath(canva, y, x)
    #plt.imshow(canvaTmp, animated=True)
    return canvaTmp
    
def main():
    init()
    pause = False
    canva = createCanva()
    canva = randomInit(canva)
    cv2.startWindowThread()
    cv2.namedWindow("life")
    while True:
        cv2.imshow('life', ndimage.zoom(canva, zoom=15,order=5)*255)
        
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            cv2.destroyAllWindows()
            break
        elif k == ord('r'):
            canva = randomInit(canva)
        elif k == ord('p'):
            pause = not pause
            
        if not pause or k == ord('n'): 
            canva = applyNextGen(canva)
        #sleep(0.1)
        
main()
