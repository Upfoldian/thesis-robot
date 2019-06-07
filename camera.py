import threading
import cv2
from time import sleep
from colour_mask import tealupper, teallower, blueupper, bluelower, purpleupper1, purplelower1, purpleupper2, purplelower2
from picamera.array import PiRGBArray
from picamera import PiCamera
"""
Main class for all camera functionalty. Uses PiCamera and OpenCV
"""
class Camera:
	def __init__(self):
		#Camera Stuff
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		self.camera.framerate = 24
		self.cols = 256
		self.rows = 192
		self.rawCapture = PiRGBArray(self.camera, size=(self.cols, self.rows))
		self.image = None
		self.imageID = 0
		self.targets = []
		self.halt = False
		self.thread = threading.Thread(target=self.cameraThread).start()
		sleep(1)
	def cameraThread(self):
		"""
		Continuously captures and processes an image, and stores the result in self.image. Also updates self.imageID when a new image is
		read to allow for image detection
		"""
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True, resize=(self.cols,self.rows)):
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
		"""
		Runs the various image processing options required for the project. This includes colour masking, contour searching
		and bounding box dimensions.
		"""
		teal, purple, blue, combined = self.colourMask()
		masks = [('teal', teal), ('purple', purple), ('blue', blue)]
		boxes = [self.getBoxDims(mask[1]) for mask in masks]
		targets = []
		for i in range(len(masks)):
			if (boxes[i] == None):
				continue
			boxInfo = {'targetName': masks[i][0], 'dims': boxes[i]}
			targets.append(boxInfo)
		self.targets = targets
		
	def saveImage(self, boxes=True, tealName="teal", blueName="blue", purpleName="purple", combinedName="all", originalName = "original"):
		"""
			Saves the current image in the img/ directory. Saves a version of each colour mask, plus the combined mask, plus the original image
		"""
		original = self.image
		teal, purple, blue, combined = self.colourMask()
		# Draw Bounding boxes if flag is true
		if (boxes == True):
			masks = [teal, purple, blue]
			boxes = [self.getBoxDims(mask) for mask in masks]

			for i in range(len(masks)):
				if (boxes[i] == None):
					continue
				(x, y, w, h) = boxes[i]
				colour = (255,255,255)
				if (i == 0):
					colour = (0, 255, 0)
				elif (i == 1):
					colour = (255, 0, 255)
				elif (i == 2):
					colour = (255, 255, 0)
				cv2.rectangle(masks[i], (x, y), (x+w, y+h), colour, 2)
				cv2.rectangle(combined, (x, y), (x+w, y+h), colour, 2)
				cv2.rectangle(original, (x, y), (x+w, y+h), colour, 2)
		# Write images to file

		cv2.imwrite("./img/%s.png" % (tealName), teal)
		cv2.imwrite("./img/%s.png" % (purpleName), purple)
		cv2.imwrite("./img/%s.png" % (blueName), blue)
		cv2.imwrite("./img/%s.png" % (combinedName), combined)
		cv2.imwrite("./img/%s.png" % (originalName), original)

	def colourMask(self):
		"""
		Applies various colour masks to the current image
		"""
		#red
		image = self.image
		image = cv2.medianBlur(image,5)	
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		#works alright for teal?
		maskteal  	= cv2.inRange(hsv, teallower, tealupper)
		maskpurple 	= cv2.inRange(hsv, purplelower1, purpleupper1)
		maskpurple 	= maskpurple + cv2.inRange(hsv, purplelower2, purpleupper2)
		maskblue 	= cv2.inRange(hsv, bluelower, blueupper)
		#maskred = cv2.dilate(frame,dilatekernel,iterations = 1)

		teal 		= cv2.bitwise_and(image,image, mask=maskteal)
		purple 		= cv2.bitwise_and(image,image, mask=maskpurple)
		blue 		= cv2.bitwise_and(image,image, mask=maskblue)
		combined 	= cv2.bitwise_and(image,image, mask=maskteal+maskpurple+maskblue)
		return teal, purple, blue, combined

	def getBiggestCont(self, contours):
		"""
		Finds the contour with the biggest area within a given contor list
		"""
		maxArea = 0.0
		maxCont = ()
		for cont in contours:
			curArea = cv2.contourArea(cont)
			if (curArea < 300):
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