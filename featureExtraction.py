import numpy as np
import cv2
import sys

def horizontalCenterPointsFinder(centerHLine,xCenter,edges,realXcenter,removalfactor):
	whiteCount=0;
	listOfXPositionsCenter =[]
	# start from center and work backwards
	for x in range(xCenter, 0, -1):
		# count 10 white pixels then mark as feature
		# print centerHLine[y]
		if centerHLine[x]==255:
			whiteCount+=1

		if whiteCount==10:
			# ensure that the block sizes are decreasing
			if len(listOfXPositionsCenter)>0:
				xTempBefore = listOfXPositionsCenter[-1]
				sizeBlock = xTempBefore-x

				if len(listOfXPositionsCenter)==1:
					xTemp2Before = xCenter
				else:
					xTemp2Before = listOfXPositionsCenter[-2]
				sizeBlock2 = xTemp2Before- xTempBefore
				# print sizeBlock2, sizeBlock
				if sizeBlock2< sizeBlock:
					break # stop if error as blocks are increasing

			listOfXPositionsCenter.append(x);
			whiteCount=0

	listOfXPositionsCenter.reverse()

	# add real center
	listOfXPositionsCenter.append(realXcenter)

	
	listOfXPositionsCenter=listOfXPositionsCenter[removalfactor:]
	# print listOfXPositionsCenter
	return listOfXPositionsCenter

def verticalCenterPointsFinder(centerVLine,yCenter,edges,realYcenter,removalfactor):

	whiteCount=0;
	listOfYPositionsCenter =[]
	# start from center and work upwards
	for y in range(yCenter, 0, -1):
		# count 10 white pixels then mark as feature
		# print centerHLine[y]
		if centerVLine[y]==255:
			whiteCount+=1

		if whiteCount==20:
			# print "gotem: ", y;
			# ensure that the block sizes are decreasing
			if len(listOfYPositionsCenter)>0:
				yTempBefore = listOfYPositionsCenter[-1]
				sizeBlock = yTempBefore-y

				if len(listOfYPositionsCenter)==1:
					yTemp2Before = realYcenter
				else:
					yTemp2Before = listOfYPositionsCenter[-2]
				sizeBlock2 = yTemp2Before- yTempBefore
				# print sizeBlock2, sizeBlock
				if sizeBlock2< sizeBlock:
					break # stop if error as blocks are increasing

			listOfYPositionsCenter.append(y);
			whiteCount=0

	
	listOfYPositionsCenter.reverse()
	# add real center
	listOfYPositionsCenter.append(realYcenter)

	listOfYPositionsCenter=listOfYPositionsCenter[removalfactor:]
	# print listOfYPositionsCenter

	return listOfYPositionsCenter

def contourFollowing(edges,cValueX,yCenter,topCount):
	
	currPos = [yCenter,cValueX]

	# CRAWLING UP
	currCount=0;
	miniBlocks =10;
	currMini=0;
	listOfCorners = []
	while(currCount<topCount):
		while(currMini<miniBlocks):
			if edges[currPos[0]-1][currPos[1]]==255:
				currPos[0]=currPos[0]-1
				# print currPos
			elif edges[currPos[0]-1][currPos[1]-1]==255:
				currPos[1]=currPos[1]-1
				currPos[0]=currPos[0]-1
			elif edges[currPos[0]-1][currPos[1]+1]==255:
				currPos[1]=currPos[1]+1
				currPos[0]=currPos[0]-1
			else:
				# print currPos
				# print "EndFound"
				currMini+=1;
				# Moving to next mini block

				while(edges[currPos[0]-1][currPos[1]]==0): 
					currPos[0]=currPos[0]-1
				# print currPos
				# shifting to the right to find corner of miniblock
				shifting=True
				while(shifting):
					if edges[currPos[0]][currPos[1]+1]==255:
						currPos[1]=currPos[1]+1
					elif edges[currPos[0]-1][currPos[1]+1]==255:
						currPos[0]=currPos[0]-1
						currPos[1]=currPos[1]+1
					elif edges[currPos[0]+1][currPos[1]+1]==255:
						currPos[0]=currPos[0]+1
						currPos[1]=currPos[1]+1
					else:
						shifting=False;

		currCount+=1;
		currMini=0;
		# print currPos
		listOfCorners.append((currPos[0],currPos[1]));
	listOfCorners.reverse()
	return listOfCorners


def extractFeatures(img,xCenter,yCenter,realXcenter,realYcenter,removalfactorH,removalfactorV):

	gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	eqlImg = cv2.equalizeHist(gray)
	blurredImg = cv2.GaussianBlur(eqlImg,(3,3),0)
	edges = cv2.Canny(blurredImg,50,150)
	cv2.imwrite('results/edges.jpg',edges)


	centerHLine = edges[yCenter,:]
	centerHList = horizontalCenterPointsFinder(centerHLine,xCenter,edges,realXcenter,removalfactorH)

	centerVLine = edges[:,xCenter]
	centerVList= verticalCenterPointsFinder(centerVLine,yCenter,edges,realYcenter,removalfactorV)

	hListLen = len(centerHList)-1
	vListLen = len(centerVList)-1
	corners = np.zeros((vListLen*2+1,hListLen*2+1,2), np.float32)
	

	for i in range(hListLen):
		listTopLeft=contourFollowing(edges,centerHList[i],yCenter,vListLen)
		# print listTopLeft
		for a in range(len(listTopLeft)):
			corners[a][i][0]=listTopLeft[a][0]
			corners[a][i][1]=listTopLeft[a][1]
	# print corners	

	# IMPROVE ROBUSTNESS
	# for i in range(hListLen):
	# q=0
	for q in range(vListLen):
		# print corners[q][0]	, corners[q][hListLen-1]	

		y1,x1=corners[q][0]
		y2,x2=corners[q][hListLen-1]
		m =(float)(y2-y1)/(x2-x1)
		# print m
		c = - m * x1 +y1
		# print c

		for btwn in range(1,hListLen-1):
			# print corners[q][btwn]
			yReq = corners[q][btwn][1]*m+c
			# print yReq, corners[q][btwn][0]
			if yReq < corners[q][btwn][0]:
				corners[q][btwn][0]=yReq


	for i in range(hListLen):
		for a in range(len(listTopLeft)):
			# determine symmetric bottom
			diffT = realYcenter-corners[a][i][0]
			corners[-1-a][i][0]=realYcenter+diffT
			corners[-1-a][i][1]=corners[a][i][1]

		# add middle x values
		corners[vListLen][i][0]=realYcenter
		corners[vListLen][i][1]=centerHList[i]

	# add center value
	corners[vListLen][hListLen][0]=realYcenter
	corners[vListLen][hListLen][1]=realXcenter

	# add middle for y values
	for i in range(vListLen):
		corners[i][hListLen][0]=centerVList[i]
		corners[i][hListLen][1]=realXcenter

	# determine symmetric center y bottom
	for a in range(vListLen):
		diffT = realYcenter-corners[a][hListLen][0]
		corners[-1-a][hListLen][0]=realYcenter+diffT
		corners[-1-a][hListLen][1]=realXcenter

		
	# determine symmetric right
	for i in range(vListLen*2+1):
		for j in range(hListLen):
			diffT = realXcenter-corners[i][j][1]

			corners[i][ -1-j ][0]=corners[i][j][0]
			corners[i][ -1-j ][1]=realXcenter+diffT

	

	return corners

def writeToFile(corners,xCorners,yCorners):
	file = open("features.txt","w") 
	for i in range(yCorners-1,-1,-1):
		for j in range(xCorners-1,-1,-1):
			# print corners[i][j]
			file.write(str(int(corners[i][j][1]))+","+str(int(corners[i][j][0]))+"\n")
	file.close()  


def main():
	imgStr = sys.argv[1]#"images/fisheye.jpg"

	# Must change these for other images but may require tweaking to other areas such as edge detection algorithm
	xCenter = 2378 
	yCenter = 1865

	realXcenter = 2434
	realYcenter = 1895

	removalfactorH = 2
	removalfactorV = 1

	img = cv2.imread(imgStr)
	
	corners = extractFeatures(img,xCenter,yCenter,realXcenter,realYcenter,removalfactorH,removalfactorV)
	print "Grid Dimentions:", corners.shape[1],corners.shape[0]
	writeToFile(corners,corners.shape[1],corners.shape[0])

	print "Completed Feature Extraction"

if  __name__ =='__main__':main()
