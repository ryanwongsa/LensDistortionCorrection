import numpy as np
import cv2

img = cv2.imread("fisheye.jpg")
w  = img.shape[1]
h = img.shape[0]

dist = np.zeros((5,1),np.float64)

# distortion coefficients for opencv
dist[0,0] = 0.0; # k1
dist[1,0] = 0.0; # k2
dist[2,0] = 0.0; # p1
dist[3,0] = 0.0; # p2
dist[4,0] = 0.0; # k3

# camera matrix
camMtx = np.eye(3,dtype=np.float32)

# Center
camMtx[0,2] = w/2.0  
camMtx[1,2] = h/2.0 
# Focal length
camMtx[0,0] = 12        
camMtx[1,1] = 12        

# applying undistortion using camera matrix and distorition coefficience using OpenCV library
result = cv2.undistort(img,camMtx,dist)
cv2.imwrite('result.png',result)