import numpy as np
import cv2

# DISTORTION CORRECTION METHOD
def distortionCorrect(k1,k2,p1,p2,k3,fx,fy,camCenterX,camCenterY,img):
	dist = np.zeros((5,1),np.float64)

	# distortion coefficients for opencv
	dist[0,0] = k1
	dist[1,0] = k2
	dist[2,0] = p1
	dist[3,0] = p2
	dist[4,0] = k3
	      
	# camera matrix
	camMtx = np.eye(3,dtype=np.float32)

	# Center
	camMtx[0,2] = camCenterX 
	camMtx[1,2] = camCenterY
	# Focal length
	camMtx[0,0] = fx       
	camMtx[1,1] = fy     

	# applying undistortion using camera matrix and distorition coefficience using OpenCV library
	result = cv2.undistort(img,camMtx,dist)
	cv2.imwrite('result.png',result)


# MAIN METHOD
def main():
	img = cv2.imread("fisheye.jpg")
	w  = img.shape[1]
	h = img.shape[0]

	k1 = -0.56221192
	k2 = 0.80029104
	p1 = -0.02754566
	p2 = 0.02465937
	k3 = -3.19925385

	camCenterX = 294.3132191 
	camCenterY = 331.04559839

	fx = 423.54421997        
	fy = 391.90820312 

	distortionCorrect(k1,k2,p1,p2,k3,fx,fy,camCenterX,camCenterY,img)
	print "Completed distortion correction"

if  __name__ =='__main__':main()
