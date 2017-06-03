import numpy as np
import cv2

# DISTORTION CORRECTION METHOD
def distortionCorrect(k1,k2,p1,p2,k3,fx,fy,camCenterX,camCenterY,img):
	dist = np.zeros((5,1),np.float64)
	h,  w = img.shape[:2]

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
	print camCenterX,camCenterY
	
	# New camera matrix
	newCamMtx = np.eye(3,dtype=np.float32)

	y_shift = h/2;
	x_shift = w/2;

	# Center
	newCamMtx[0,2] = camCenterX +x_shift
	newCamMtx[1,2] = camCenterY +y_shift
	# Focal length
	newCamMtx[0,0] = fx
	newCamMtx[1,1] = fy


	# applying undistortion using camera matrix and distorition coefficience using OpenCV library
	mapx,mapy = cv2.initUndistortRectifyMap(camMtx,dist,None,newCamMtx,(w+2*x_shift,h+2*y_shift),5)
	result = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)

	cv2.imwrite('result.jpg',result)



# CALIBRATION METHOD
def calibrationCalculation(xCorners,yCorners,img):
	objp = np.zeros((xCorners*yCorners,3), np.float32)
	objp[:,:2] = np.mgrid[0:xCorners,0:yCorners].T.reshape(-1,2)

	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane.

	gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	
	ret = True;
	corners = np.zeros((xCorners*yCorners,1,2), np.float32)

	lines = [line.rstrip('\n') for line in open('handmadefeatures_v2.txt')]

	cornerCount=0;
	for line in lines:
		x,y = [x.strip() for x in line.split(',')]
		# print x,y
		corners[cornerCount][0][0]=x
		corners[cornerCount][0][1]=y
		cornerCount+=1

	# print corners

	if ret == True:
		objpoints.append(objp)

		# corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners)

		# Draw and display the corners
		boardImg = cv2.drawChessboardCorners(img, (xCorners,yCorners), corners,ret)
		cv2.imwrite('boardDrawn.jpg',boardImg)

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
	k1,k2,p1,p2,k3 = dist[0]


	return k1,k2,p1,p2,k3,mtx[0][0], mtx[1][1], mtx[0][2], mtx[1][2]

# MAIN METHOD
def main():
	img = cv2.imread("fisheye.jpg")
	w  = img.shape[1]
	h = img.shape[0]
	xCorners =19;
	yCorners=8;
	k1, k2, p1, p2, k3, fx, fy, camCenterX,camCenterY = calibrationCalculation(xCorners,yCorners,img)

	img = cv2.imread("fisheye.jpg")

	distortionCorrect(k1,k2,p1,p2,k3,fx,fy,camCenterX,camCenterY,img)
	print "Completed distortion correction"

if  __name__ =='__main__':main()
