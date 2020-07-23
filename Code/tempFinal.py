import numpy as np
import cv2
import math
import thresh as th1
import thresh2 as th2
import detectShape as ds
import bfs
import time
import serial
import ajcacency_9 as ad
adjMat = ad.adj

def i(steps):
    n=int(9)
    i = int(steps/n)
    j = steps%n
    j = j-1
    if j==-1:
        i=i-1
    return i

def j(steps):
    n=int(9)
    j = steps%n
    j = j-1
    if j==-1:
        j=n-1
    return j


############################################################
def distance(p1,p2):
    #print("DISTANCE !")
    distance=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    
    return distance

def get_bot(arena):
    #b1 = th2.start(arena)
    frontmask = th2.threshold(arena,pink)
    cv2.imshow('bot1',frontmask)
    cv2.waitKey(200)
    
    
    #b2 = th2.start(arena)
    backmask = th2.threshold(arena,brown)
    cv2.imshow('bot2',backmask)
    cv2.waitKey(200)
    #cv2.destroyAllWindows()
    contours, hierarchy = cv2.findContours(frontmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    for cnt in contours:
            M=cv2.moments(cnt)
            if M["m00"]!=0:
                cX1 = int(M["m10"] / M["m00"])
                cY1 = int(M["m01"] / M["m00"])
            else:
                cX1,cY1=0,0
    
    contoursB, hierarchy = cv2.findContours(backmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    for cnt in contoursB:
            M=cv2.moments(cnt)
            if M["m00"]!=0:
                cX2 = int(M["m10"] / M["m00"])
                cY2 = int(M["m01"] / M["m00"])
            else:
                cX2,cY2=0,0
    p1 = np.array([cX1,cY1])
    p2 = np.array([cX2,cY2])
    print("Center1,2:",p1,p2)
    cntr = (p1+p2)/2

    botvector = p1-p2
    #botvector[1] = -botvector[1]
    print("Curr:",cntr)
    return[cntr,botvector]

def get_angle(destvector,botvector):
    print(botvector,destvector)
    c1 = complex(botvector[0],botvector[1])
    c2 = complex(destvector[0],destvector[1])
    #print(c1,c2)
    ang = np.angle(c1/c2)
    ang = ang*180/math.pi
    return ang

def getSnapshot():
    ret,frame = cap.read()
    img = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    return img

############################################################

def Arduino(key,value):
    c1=0.05
    c2=0.05

    if key == 'f':
        print("FORWARD")
        ser.write(b'F')
        time.sleep(0.3)
        print("Stop")
        ser.write(b'S')
    elif key == 'l':
        ser.write(b'L')
        print("left")
        time.sleep(0.1)
        ser.write(b'S')
    elif key == 'r':
        ser.write(b'R')
        print("right")
        time.sleep(0.1)
        ser.write(b'S')
    elif key=='1':
        ser.write(b'1')
        
        

############################################################



def c2n(centroid):
    row1,col1,_ = img.shape
    n=int(9)
    ##print("c2n started")
    c = int((centroid[0]*n)/row1)
    r = int((centroid[1]*n)/col1)
    
    number = n*r+c+1
    print("c2n:",number)
    return number

def n2c(num):
    l1,l2,_ = img.shape
    b = i(num)
    a = j(num)
    #print(,a,b)
    centr = np.array([(2*a+1)*l1/18,(2*b+1)*l2/18])
    print("Center:",centr)
    return centr

###########################################################

def turn(phi):
    if phi>0:
        Arduino('l',phi)
    else:
        Arduino('r',phi)
    

def stepForward(step):
    Arduino('f',step)
    

###########################################################

def allign(endPt):
    erra = 10
    while True:

        img = getSnapshot()
        pos,botVec = get_bot(img)
        destVec = endPt-pos
        
        print("botVec : ",botVec)
        print("destVec : ",destVec)
        
        #print("dest:",destVec)
        phi = get_angle(destVec, botVec)
        print("phi:",phi)
        if abs(phi) < erra:
            break
        turn(phi)


def goto(node):
    print("going to ",node)
    step = 20
    errp = 20
    erra = 5
    endPt = n2c(node)
    print("next node centroid : ",endPt)
    '''
    img = getSnapshot()
    pos,botVec = get_bot(img)
    endPt = n2c(node)
    destVec = endPt-pos

    phi = get_angle(destVec, botVec)


    while True:
        img = getSnapshot()
        pos,botVec = get_bot(img)
        print("pos and botvec: ",pos,botVec)
        destVec = endPt-pos
        phi = get_angle(destVec, botVec)
        if phi < erra:
            break
        turn(phi)
    '''
    while True:
        img = getSnapshot()
        pos,botVec = get_bot(img)
        d = distance(pos,endPt)
        
        if d<errp:
            break
        allign(endPt)
        stepForward(step)
        
        
###########################################################



cap = cv2.VideoCapture(0)
#cap.set(3,960)
#cap.set(4,1280)
ret,frame = cap.read()
#frame=cv2.imread(r"improve.png")
#cv2.imwrite("arena10.jpg",)
r = cv2.selectROI(frame)
img = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

red = th1.startred(img)
yellow = th1.startyellow(img)
pink = th2.start(img)
brown = th2.start(img)

print(red,yellow,pink,brown)

maskr = th1.thresholdred(img,red)
masky = th1.thresholdyellow(img,yellow)
#maskyr=  th1.thresholdred(masky,red)
bot1 = th2.threshold(img,pink)
bot2 = th2.threshold(img,brown)

cv2.imshow('redmask',maskr)
cv2.imshow('yellowmask',masky)
cv2.imshow('bot1',bot1)
cv2.imshow('bot2',bot2)
cv2.waitKey(1000)
cv2.destroyAllWindows()

ser = serial.Serial("COM4",9600)
time.sleep(2)


if __name__ == "__main__":
    '''
    img = getSnapshot()
    print("qwertyuiop")
    shapeMat = ds.detect(img,maskr,masky)
    print(shapeMat)
    #strt = c2n(pos)
    strt = 37
    inp = 1
    path = bfs.bfs(strt,inp,shapeMat)
    print(path)
    for p in path:
        goto(p)
    ser.close()
    '''
    shapeMat = ds.detect(img,maskr,masky)
    print(shapeMat)
    while True:
        img = getSnapshot()
      
        inp = int(input("What Appeared on Dice ?"))
        pos,botVec = get_bot(img)
        print(shapeMat)
        strt = c2n(pos)
        print("START:",strt)
        row = int(strt/9)
        col = int(strt%9)
        col = col-1
        if col== -1:
            row = row-1
            col = 8
        shapeMat[row][col]=0            
        path=bfs.bfs(strt,inp,shapeMat)
        print(path)

        if path:
           
            for p in path:
                goto(p)
        if path[-1]==40:
            #goto(41)
            ser.write(b'F')
            time.sleep(0.2)
            print("we are in the endgame now")
            break

        adjMat[37][28]=0
        adjMat[37][38]=1
        
  
    print("the end")
    Arduino('1',0)
    ser.close()  
