import numpy as np
import cv2

#im=cv2.imread('C:/Users/Personal/Desktop/pixelate/arena.jpg')

def start(img):

    im = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)   #hsv
    r = cv2.selectROI(img)
    imcrop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])] #bgr

    hmin=imcrop[:,:,0].min()
    hmax=imcrop[:,:,0].max()
    smin=imcrop[:,:,1].min()
    smax=imcrop[:,:,1].max()
    vmin=imcrop[:,:,2].min()
    vmax=imcrop[:,:,2].max()

    thresh= 15
    minihsv = np.array([hmin,smin,vmin])
    maxihsv=np.array([hmax,smax,vmax])

    minihsv1=np.array([minihsv[0]-thresh,minihsv[1]-thresh,minihsv[2]-thresh])
    maxihsv1=np.array([maxihsv[0]+thresh,maxihsv[1]+thresh,maxihsv[2]+thresh])

    mat =np.array([minihsv1,maxihsv1])
    return mat

def threshold(img,mat):
    maskhsv=cv2.inRange(img , mat[0] , mat[1])
    kernel = np.ones((4,4),np.uint8)
    erosion = cv2.erode(maskhsv,kernel,iterations =2)
    mask = cv2.dilate(erosion,kernel,iterations = 2)
    return mask
