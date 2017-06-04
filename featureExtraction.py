import numpy as np
import cv2

def horizontalCenterPointsFinder(centerHLine,xCenter,edges):
	whiteCount=0;
	listOfXPositionsCenter =[]
	# start from center and work backwards
	for x in range(xCenter, 0, -1):
		# count 10 white pixels then mark as feature
		# print centerHLine[y]
		if centerHLine[x]==255:
			whiteCount+=1

		if whiteCount==10:
			# print "gotem: ", x;
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
	listOfXPositionsCenter.append(2434)
	# print listOfXPositionsCenter
	currentLen= len(listOfXPositionsCenter)

	whiteCount=0;
	intitialwhiteCount=13;
	# start from center and work forward
	for x in range(xCenter, edges.shape[1], 1):
		# count 10 white pixels then mark as feature
		# print centerHLine[y]
		if centerHLine[x]==255:
			whiteCount+=1


		if whiteCount==intitialwhiteCount:
			# print "gotem: ", x;
			# ensure that the block sizes are decreasing
			if len(listOfXPositionsCenter)>currentLen:
				xTempBefore = listOfXPositionsCenter[-1]
				sizeBlock = x-xTempBefore

				if len(listOfXPositionsCenter)==currentLen+1:
					xTemp2Before = xCenter
				else:
					xTemp2Before = listOfXPositionsCenter[-2]
				sizeBlock2 =  xTempBefore-xTemp2Before
				# print sizeBlock2, sizeBlock
				if sizeBlock2< sizeBlock:
					break # stop if error as blocks are increasing

			listOfXPositionsCenter.append(x);
			whiteCount=0
			intitialwhiteCount=10
	# print listOfXPositionsCenter

	removalfactor=2
	listOfXPositionsCenter=listOfXPositionsCenter[removalfactor:len(listOfXPositionsCenter)-removalfactor]
	print listOfXPositionsCenter

	return listOfXPositionsCenter

def verticalCenterPointsFinder(centerVLine,yCenter,edges):

	whiteCount=0;
	listOfYPositionsCenter =[]
	# start from center and work upwards
	for y in range(yCenter, 0, -1):
		# count 10 white pixels then mark as feature
		# print centerHLine[y]
		if centerVLine[y]==255:
			whiteCount+=1

		if whiteCount==8:
			# print "gotem: ", y;
			# ensure that the block sizes are decreasing
			if len(listOfYPositionsCenter)>0:
				yTempBefore = listOfYPositionsCenter[-1]
				sizeBlock = yTempBefore-y

				if len(listOfYPositionsCenter)==1:
					yTemp2Before = 1895
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
	listOfYPositionsCenter.append(1895)
	print listOfYPositionsCenter

	currentLen= len(listOfYPositionsCenter)

	whiteCount=0;
	intitialwhiteCount=9;
	# start from center and work backwards
	for y in range(yCenter, edges.shape[0], 1):
		# count 10 white pixels then mark as feature
		# print centerHLine[y]
		if centerVLine[y]==255:
			whiteCount+=1


		if whiteCount==intitialwhiteCount:
			# print "gotem: ", y;
			# ensure that the block sizes are decreasing
			if len(listOfYPositionsCenter)>currentLen:
				yTempBefore = listOfYPositionsCenter[-1]
				sizeBlock = y-yTempBefore

				if len(listOfYPositionsCenter)==currentLen+1:
					yTemp2Before = yCenter
				else:
					yTemp2Before = listOfYPositionsCenter[-2]
				sizeBlock2 =  yTempBefore-yTemp2Before
				# print sizeBlock2, sizeBlock
				if sizeBlock2< sizeBlock:
					break # stop if error as blocks are increasing

			listOfYPositionsCenter.append(y);
			whiteCount=0
			if intitialwhiteCount==9:
				intitialwhiteCount=10
			else:
				intitialwhiteCount=8
	print listOfYPositionsCenter

	reductionFactor=3
	listOfYPositionsCenter=listOfYPositionsCenter[:len(listOfYPositionsCenter)-reductionFactor]
	print listOfYPositionsCenter

	return listOfYPositionsCenter, currentLen, len(listOfYPositionsCenter)-currentLen

def contourFollowing(edges,cValueX,yCenter,topCount):
	
	currPos = [yCenter,cValueX]
	# CRAWLING UP
	currCount=0;
	miniBlocks =4;
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



def extractFeatures(img,xCorners,yCorners):

	gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
	eqlImg = cv2.equalizeHist(gray)
	blurredImg = cv2.GaussianBlur(eqlImg,(5,5),0)
	edges = cv2.Canny(blurredImg,50,150)
	cv2.imwrite('results/edges.jpg',edges)

	xCenter = 2378
	yCenter = 1865

	realXcenter = 2434
	realYcenter = 1895

	centerHLine = edges[yCenter,:]
	centerHList = horizontalCenterPointsFinder(centerHLine,xCenter,edges)
	
	centerVLine = edges[:,xCenter]
	centerVList,bottomCount,topCount = verticalCenterPointsFinder(centerVLine,yCenter,edges)
	centerVList = centerVList[2:]
	print centerVList

	corners = np.zeros((11,9,2), np.float32)

	for i in range(4):
		listTopLeft=[]
		listTopLeft=contourFollowing(edges,centerHList[i],yCenter,topCount)
	# 	print listTopLeft
		for a in range(len(listTopLeft)):
			corners[a][i][0]=listTopLeft[a][0]
			corners[a][i][1]=listTopLeft[a][1]

			# determine symmetric bottom
			diffT = realYcenter-corners[a][i][0]
			diffToCenterNum = 6+(4-a) # center + (mid - a)
			corners[diffToCenterNum][i][0]=realYcenter+diffT
			corners[diffToCenterNum][i][1]=corners[a][i][1]

		# add middle values
		corners[5][i][0]=realYcenter
		corners[5][i][1]=centerHList[i]

	# # add middle for y values
	for i in range(11):
		corners[i][4][0]=centerVList[i]
		corners[i][4][1]=realXcenter

	# determine symmetric right
	for i in range(11):
		for j in range(4):
			diffT = realXcenter-corners[i][j][1]
			diffToCenterNum = 4+(4-j) # center + (mid - a)
			corners[i][diffToCenterNum][0]=corners[i][j][0]
			corners[i][diffToCenterNum][1]=realXcenter+diffT

	print corners
	return corners

def writeToFile(corners):
	file = open("features.txt","w") 
	for i in range(10,-1,-1):
		for j in range(8,-1,-1):
			# print corners[i][j]
			file.write(str(int(corners[i][j][1]))+","+str(int(corners[i][j][0]))+"\n")
	file.close()  



def main():
	imgStr = "images/fisheye.jpg"
	xCorners =10;
	yCorners=6;
	# file = sys.argv[4]#"handmadefeatures_v2.txt"

	img = cv2.imread(imgStr)
	
	corners = extractFeatures(img,xCorners,yCorners)
	writeToFile(corners);


	print "Completed Feature Extraction"

if  __name__ =='__main__':main()
