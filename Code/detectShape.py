import numpy as np
import cv2

n = 9
mat = np.zeros([n,n])

'''
1 -> red triangle
2 -> red square
3 -> red circle
4 -> yellow triangle
5 -> yellow square
6 -> yellow circle
'''

def detect(img,redmask,yellowmask):
    row,col,_ = img.shape
    contours,h = cv2.findContours(redmask,1,2)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>200:
            approx = cv2.approxPolyDP(cnt,0.045*cv2.arcLength(cnt,True),True)
            M = cv2.moments(cnt)
            cntX = int(M["m10"] / M["m00"])
            cntY = int(M["m01"] / M["m00"])
            r = int((cntY*n)/row)
            c = int((cntX*n)/col)
            #print (len(approx))
            if len(approx)==3:
                #print ("triangle")
                cv2.drawContours(img,[cnt],0,(0,255,0),5)
                mat[r,c]=1
            elif len(approx)==4:
                #print ("square")
                cv2.drawContours(img,[cnt],0,(0,255,0),5)
                mat[r,c]=2

            else :
                #print ("circle")
                cv2.drawContours(img,[cnt],0,(0,255,0),-1)
                mat[r,c]=3
    print("FNWJK")
    contours,h = cv2.findContours(yellowmask,1,2)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>200:
            approx = cv2.approxPolyDP(cnt,0.045*cv2.arcLength(cnt,True),True)
            M = cv2.moments(cnt)
            cntX = int(M["m10"] / M["m00"])
            cntY = int(M["m01"] / M["m00"])
            r = int((cntY*n)/row)
            c = int((cntX*n)/col)
            #print (len(approx))
            if len(approx)==3 :
                cv2.drawContours(img,[cnt],0,(0,255,0),5)
                mat[r,c]=4

            elif len(approx)==4 and mat[r,c]!=4:
                #print ("square")
                cv2.drawContours(img,[cnt],0,(0,255,0),5)
                mat[r,c]=5

            elif len(approx)>4 and mat[r,c]!=4:
                #print ("circle")
                cv2.drawContours(img,[cnt],0,(0,255,0),-1)
                mat[r,c]=6

        

    #cv2.imshow('img',img)
    return mat
