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



# CALIBRATION METHOD
def calibrationCalculation(xCorners,yCorners,img):
	objp = np.zeros((xCorners*yCorners,3), np.float32)
	objp[:,:2] = np.mgrid[0:xCorners,0:yCorners].T.reshape(-1,2)

	objpoints = [] # 3d point in real world space
	imgpoints = [] # 2d points in image plane.

	gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	
	ret = True;
	corners= np.array([[[4396,2916]],
[[4192,3040]],
[[3900,3164]],
[[3504,3296]],
[[3000,3384]],
[[2432,3408]],
[[1860,3360]],
[[1380,3244]],
[[1004,3108]],
[[720,2980]],
[[516,2872]],
[[4468,2540]],
[[4276,2628]],
[[3996,2728]],
[[3596,2828]],
[[3064,2900]],
[[2440,2928]],
[[1816,2884]],
[[1308,2792]],
[[920,2692]],
[[656,2600]],
[[456,2516]],
[[4496,2136]],
[[4308,2172]],
[[4036,2212]],
[[3648,2252]],
[[3104,2296]],
[[2452,2300]],
[[1808,2280]],
[[1280,2252]],
[[888,2204]],
[[620,2164]],
[[424,2124]],
[[4472,1724]],
[[4288,1704]],
[[4008,1680]],
[[3616,1660]],
[[3088,1644]],
[[2444,1632]],
[[1808,1648]],
[[1300,1672]],
[[908,1684]],
[[632,1708]],
[[444,1724]],
[[4400,1332]],
[[4204,1272]],
[[3932,1196]],
[[3544,1128]],
[[3040,1068]],
[[2448,1060]],
[[1856,1080]],
[[1356,1140]],
[[976,1216]],
[[704,1291]],
[[500,1348]],
[[4304,996]],
[[4088,900]],
[[3796,800]],
[[3428,700]],
[[2960,632]],
[[2436,612]],
[[1916,640]],
[[1452,720]],
[[1076,816]],
[[804,912]],
[[592,1012]],
[[4168,700]],
[[3956,596]],
[[3672,484]],
[[3320,392]],
[[2900,320]],
[[2432,296]],
[[1972,328]],
[[1548,400]],
[[1200,496]],
[[920,608]],
[[696,716]]], np.float32)

	if ret == True:
		objpoints.append(objp)

		# corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
		imgpoints.append(corners)

		# Draw and display the corners
		boardImg = cv2.drawChessboardCorners(img, (xCorners,yCorners), corners,ret)
		cv2.imwrite('boardDrawn.png',boardImg)

	ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
	k1,k2,p1,p2,k3 = dist[0]


	return k1,k2,p1,p2,k3,mtx[0][0], mtx[1][1], mtx[0][2], mtx[1][2]

# MAIN METHOD
def main():
	img = cv2.imread("fisheye.jpg")
	w  = img.shape[1]
	h = img.shape[0]
	xCorners =11;
	yCorners=7;
	k1, k2, p1, p2, k3, fx, fy, camCenterX,camCenterY = calibrationCalculation(xCorners,yCorners,img)

	# k1 = -0.56221192
	# k2 = 0.80029104
	# p1 = -0.02754566
	# p2 = 0.02465937
	# k3 = -3.19925385

	# camCenterX = w/2.0 
	# camCenterY = h/2.0

	# fx = 423.54421997        
	# fy = 391.90820312 
	img = cv2.imread("fisheye.jpg")
	
	distortionCorrect(k1,k2,p1,p2,k3,fx,fy,camCenterX,camCenterY,img)
	print "Completed distortion correction"

if  __name__ =='__main__':main()
