import numpy as np
import cv2

MIN_MATCH_COUNT=30

detector = cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDITREE=0
flannParam=dict(algorithm=FLANN_INDEX_KDITREE,tree=5)
flann=cv2.FlannBasedMatcher(flannParam,{})

trainImg=cv2.imread("box.png",0)
trainKP,trainDesc=detector.detectAndCompute(trainImg,None)

QueryImg = cv2.imread("boxCena.png",0)
queryKP,queryDesc = detector.detectAndCompute(QueryImg,None)
matches=flann.knnMatch(queryDesc,trainDesc,k=2)

goodMatch=[]

for m,n in matches:
	if(m.distance < 0.75*n.distance):
		goodMatch.append(m)
		
if(len(goodMatch) > MIN_MATCH_COUNT):
	tp=[]
	qp=[]
	for m in goodMatch:
		tp.append(trainKP[m.trainIdx].pt)
		qp.append(queryKP[m.queryIdx].pt)
	tp,qp=np.float32((tp,qp))
	H,status=cv2.findHomography(tp,qp,cv2.RANSAC,3.0)
	h,w=trainImg.shape
	trainBorder=np.float32([[[0,0],[0,h-1],[w-1,h-1],[w-1,0]]])
	queryBorder = cv2.perspectiveTransform(trainBorder,H)
	
	x = 0
	y = 0
	
	array = np.int32(queryBorder)
		
	for i in array[0]:
		x += i[0]
		y += i[1]
		
	x = int(x/4)
	y = int(y/4)
	
	print (x,y) #Centro de massa
	
	cv2.polylines(QueryImg,[np.int32(queryBorder)],True,(0,255,0),5)
	
else:
	print ("Not Enough match found")
	
cv2.imshow('result',QueryImg)
cv2.waitKey(0)
cv2.destroyAllWindows()