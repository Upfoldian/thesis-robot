import threading
import cv2
from time import sleep
from colour_mask import tealupper, teallower, yellowupper, yellowlower, purpleupper1, purplelower1, purpleupper2, purplelower2
from picamera.array import PiRGBArray
from picamera import PiCamera

class Camera:
	def __init__(self):
		#Camera Stuff
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		self.camera.framerate = 24
		self.rows = 256
		self.cols = 192
		self.rawCapture = PiRGBArray(self.camera, size=(self.rows, self.cols))
		self.image = None
		self.imageID = 0
		self.targets = []
		self.halt = False
		self.thread = threading.Thread(target=self.cameraThread).start()
		sleep(0.5)
	def cameraThread(self):
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True, resize=(self.rows,self.cols)):
			if (self.halt == True):
				break
			self.image = frame.array
			self.image =self.image[80:256, 0:256]
			self.processImage()
			#TODO: process image
			self.imageID += 1
			if (self.imageID > 100):
				self.imageID = 0

			self.rawCapture.truncate()
			self.rawCapture.seek(0)

	def processImage(self):

		teal, purple, yellow, combined = self.colourMask()
		masks = [('teal', teal), ('purple', purple), ('yellow', yellow)]
		boxes = [self.getBoxDims(mask[1]) for mask in masks]
		targets = []
		for i in range(len(masks)):
			if (boxes[i] == None):
				continue
			boxInfo = {'targetName': masks[i][0], 'dims': boxes[i]}
			targets.append(boxInfo)
		self.targets = targets
	def saveImage(self, boxes=True, tealName="teal", yellowName="yellow", purpleName="purple", combinedName="all", originalName = "original"):
		original = self.image
		teal, purple, yellow, combined = self.colourMask()
		# Draw Bounding boxes if flag is true
		if (boxes == True):
			masks = [teal, purple, yellow]
			boxes = [self.getBoxDims(mask) for mask in masks]

			for i in range(len(masks)):
				if (boxes[i] == None):
					continue
				(x, y, w, h) = boxes[i]
				cv2.rectangle(masks[i], (x, y), (x+w, y+h), (255, 255, 0), 2)
				cv2.rectangle(combined, (x, y), (x+w, y+h), (255, 255, 0), 2)
				cv2.rectangle(original, (x, y), (x+w, y+h), (255, 255, 0), 2)
		# Write images to file

		cv2.imwrite("./img/%s.png" % (tealName), teal)
		cv2.imwrite("./img/%s.png" % (purpleName), purple)
		cv2.imwrite("./img/%s.png" % (yellowName), yellow)
		cv2.imwrite("./img/%s.png" % (combinedName), combined)
		cv2.imwrite("./img/%s.png" % (originalName), original)

	def colourMask(self):
		#red
		image = self.image
		image = cv2.medianBlur(image,5)	
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		#works alright for teal?
		maskteal  	= cv2.inRange(hsv, teallower, tealupper)
		maskpurple 	= cv2.inRange(hsv, purplelower1, purpleupper1)
		maskpurple 	= maskpurple + cv2.inRange(hsv, purplelower2, purpleupper2)
		maskyellow 	= cv2.inRange(hsv, yellowlower, yellowupper)
		#maskred = cv2.dilate(frame,dilatekernel,iterations = 1)

		teal 		= cv2.bitwise_and(image,image, mask=maskteal)
		purple 		= cv2.bitwise_and(image,image, mask=maskpurple)
		yellow 		= cv2.bitwise_and(image,image, mask=maskyellow)
		combined 	= cv2.bitwise_and(image,image, mask=maskteal+maskpurple+maskyellow)
		return teal, purple, yellow, combined

	def getBiggestCont(self, contours):
		maxArea = 0.0
		maxCont = ()
		for cont in contours:
			curArea = cv2.contourArea(cont)
			if (curArea < 700):
				continue
			if (curArea > maxArea):
				maxArea = curArea
				maxCont = cont
		return maxCont

	def getBoxDims(self, mask):
		greyMask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
		contours, hiers = cv2.findContours(greyMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
		cont = self.getBiggestCont(contours)
		if (len(cont) != 0):
			x, y, w, h = cv2.boundingRect(cont)
			return (x, y, w, h)
		else:
			return None
	def hasTargets(self):
		return len(self.targets) > 0

	def haltThread(self):
		self.halt = True