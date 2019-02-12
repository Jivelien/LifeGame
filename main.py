import numpy as np
import matplotlib.pyplot as plt
import random


global canvaY, canvaX, cellBornMin, cellBornMax, cellOverpop

canvaY = 50 # px
canvaX = 50 # px
cellOverpop = 3
cellBornMin = 2
cellSolitude = cellBornMin
cellBornMax = cellOverpop

def createCanva():
    return np.zeros((canvaY,canvaX), dtype=int)

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
    plt.imshow(canvaTmp, animated=True)
    return canvaTmp
    

canva = createCanva()
canva = randomInit(canva)
plt.imshow(canva, animated=True)
canva = applyNextGen(canva)
