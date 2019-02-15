#!/usr/bin/python3

import numpy as np
import random
import cv2
from scipy import ndimage
from time import sleep, time
import os
import glob
import moviepy.editor as mpy
import threading
import shutil

def init():
    global canvaY, canvaX, cellBornMin, cellSolitude, cellBornMax, cellOverpop
    canvaY = 50 # px
    canvaX = 70 # px
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
    
def mouseControl(event,x,y,flags,param):
    global drawing, erasing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        canva[y//zoom, x//zoom] = 1
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        
    elif event == cv2.EVENT_RBUTTONDOWN:
        erasing = True
        canva[y//zoom, x//zoom] = 0 
    elif event == cv2.EVENT_RBUTTONUP:
        erasing = False
    
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            canva[y//zoom, x//zoom] = 1
        elif erasing:
            canva[y//zoom, x//zoom] = 0 

def createGif(canvas):
    directory='tmp'+str(int(time()))
    os.mkdir(directory) 
    canvasGif=[]
    for element in canvas:
        canvasGif.append(cv2.cvtColor(element,cv2.COLOR_GRAY2RGB))

    i=0
    for element in canvasGif:
        cv2.imwrite('./'+directory+'/'+"{0:0=10d}".format(i)+'.png',element)
        i+=1
        
    filenames = glob.glob("./"+directory+"/*.png")
    filenames.sort()
    clip = mpy.ImageSequenceClip(filenames, fps=10)
    clip.write_gif('lifegame'+str(int(time()))+'.gif', fps=10)
    shutil.rmtree(directory)
    
def nothing(*args):
    pass

def main():
    try:
        init()
        global canva, canvas, zoom, drawing, erasing
        i=0
        canvas=[]
        pause = True
        save = False
        drawing, erasing = False, False
        zoom = min(1700//canvaX, 900//canvaY)
        canva = createCanva()
        cv2.startWindowThread()
        cv2.namedWindow("life")
        
        cv2.setMouseCallback('life',mouseControl)
        cv2.createTrackbar('lift','life',0,5,nothing)
        cv2.createTrackbar('sleepPeriod','life',0,500,nothing)
        cv2.setTrackbarPos('sleepPeriod','life',100)
        
        while True:
            order = cv2.getTrackbarPos('lift','life')
            sleepPeriod = cv2.getTrackbarPos('sleepPeriod','life')/1000
            
            canvaPic=ndimage.zoom(canva, zoom=zoom,order=order)*255
            
            if save:
                canvas.append(canvaPic)
                cv2.circle(canvaPic,(canvaPic.shape[1]-40,40), 20, (100), -1)
            
            cv2.putText(canvaPic,str(i),(20,50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255),3)
            
            cv2.imshow('life', canvaPic)

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                cv2.destroyAllWindows()
                break
            elif k == ord('r'):
                i=0
                canva = randomInit(canva)
            elif k == ord('i'):
                i=0
                canva = createCanva()
            elif k == ord('p'):
                pause = not pause
            elif k == ord('s'):
                save = not save
                if not save:
                    threading.Thread(target=createGif, args=[canvas]).start()           
                    canvas=[]
            if not pause or k == ord('n'): 
                canva = applyNextGen(canva)
                i+=1
            if not any([drawing,erasing]):
                sleep(sleepPeriod)
            
    except Exception as error:
        print('Error: ' + str(type(error)) + ' - ' + str(error.args))
        cv2.destroyAllWindows()
        
main()