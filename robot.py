import TomLSM303C
import gpiozero
import comms
import threading
import cv2
from math import atan2, degrees
from mag_offsets import mag_x_offset, mag_y_offset, mag_z_offset
from time import sleep
from picamera.array import PiRGBArray
from picamera import PiCamera

class Robot:
	def __init__(self, leftOn=17, leftDir=27, rightOn=23, rightDir=24, modePin=22):


		# Motor Stuff
		self.leftMotor = gpiozero.PWMLED(leftOn, frequency=50)
		self.leftDir = gpiozero.LED(leftDir)

		self.rightMotor = gpiozero.PWMLED(rightOn, frequency=50)
		self.rightDir = gpiozero.LED(rightDir)

		self.mode = gpiozero.LED(modePin)
		self.mode.on()

		#IMU Stuff
		self.IMU = TomLSM303C.LSM303C() #check it with sudo i2cdetect -y 1 (should be 1D, 1E)
		self.updateIMU()

		# Comms stuff
		self.comms = comms.Comms()
		self.name = self.comms.getHostname()

		#Camera Stuff
		self.camera = PiCamera()
		self.camera.resolution = (640, 480)
		self.camera.framerate = 24
		self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
		self.image = None
		self.imageID = -1
		thread = threading.Thread(target=self.cameraThread)
		thread.daemon = True
		thread.start()
		# Heading stuff 
		self.headingList = [0] * 20
		self.headingSum = 0.0
		# So Control+C kills them, but in a bad way because im lazy
		thread = threading.Thread(target=self.headingThread)
		thread.daemon = True
		thread.start()
		# Fresh update variables
		self.prevMag = self.mag
		self.prevAccel = self.accel

	def cameraThread(self):
		for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True, resize=(640,480)):
			self.image = frame.array
			#TODO: process image
			self.imageID += 1
			if (self.imageID > 100):
				self.imageID = 0

			self.rawCapture.truncate()
			self.rawCapture.seek(0)



	def hasMessage(self):
		return self.comms.hasMessage()

	def readMessage(self):
		msg = self.comms.getMessage
		args = msg.split(" ")
		message = {"from": args[0], "command": args[1], "args": args[2:-1]}
		return message

	def stop(self):
		self.leftDir.off()
		self.rightDir.off()

		self.rightMotor.value = 0
		self.leftMotor.value = 0

	def start(self, time=0):
		self.rightMotor.value = 1
		self.leftMotor.value = 1

		if (time != 0):
			sleep(time)
			self.stop()

	def spinLeft(self, time=0):
		self.rightMotor.value = 1
		self.leftDir.on()

		if (time != 0):
			sleep(time)
			self.stop()

	def spinRight(self, time=0):
		self.leftMotor.value = 1
		self.rightDir.on()

		if (time != 0):
			sleep(time)
			self.stop()
		
	def reverse(self, time=0):
		self.leftDir.on()
		self.rightDir.on()

		if(time != 0):
			sleep(time)
			self.stop()

		self.leftDir.off()
		self.rightDir.off()

	def startLeft(self, time=0):
		self.leftMotor.value = 1
		if (time != 0):
			sleep(time)
			self.stop()

	def startRight(self, time=0):
		self.rightMotor.value = 1

		if (time != 0):
			sleep(time)
			self.stop()


	def moveForward(self, distance=0.5):

		self.leftDir.off()
		self.rightDir.off()

		currentDistance = 0
		while(currentDistance < distance):
			self.start()

		self.stop()

	def moveBack(self, distance=0.5):
		self.leftDir.on()
		self.rightDir.on()

		currentDistance = 0

		while(currentDistance < distance):
			self.start()
		self.stop()

	def turnLeft(self, angle=90.0):

		self.spinLeft()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle - angle) % 360
		while (currentAngle != targetAngle):
			currentAngle = self.getHeading()
		self.stop() 


	def turnRight(self, angle=90.0):
		

		self.spinRight()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle + angle) % 360
		while (currentAngle != targetAngle):
			currentAngle = self.getHeading()
		self.stop()

	def updateIMU(self):
		accel, mag = self.IMU.read()
		mag_x, mag_y, mag_z = mag

		mag_x -= mag_x_offset
		mag_y -= mag_y_offset
		mag_z -= mag_z_offset

		self.accel = accel
		self.mag = (mag_x, mag_y, mag_z)

	def headingThread(self):
		index = 0
		while(True):
			self.headingSum -= self.headingList[index]
			mag_x, mag_y, mag_z = self.getMag()
			curHeading = round(degrees(atan2(mag_y, mag_x)), 0) % 360
			avgHeading = round(self.headingSum/20.0)

			# All these if statements handle the crossover point from 359 to 0 degrees
			# They do a little bit of magic to solve that (picks a point either side of
			# 0 to do the transision before it becomes a problem)

			if (avgHeading > 340 and curHeading < 20):
				self.headingList[index] = 360 + curHeading
			elif (avgHeading < 20 and curHeading > 340):
				self.headingList[index] = curHeading - 360
			else:
				self.headingList[index] = curHeading

			self.headingSum += self.headingList[index]

			if (avgHeading >= 370):
				self.headingList = [10] * 20
				self.headingSum = 10 * 20.0
			if (avgHeading <= -10):
				self.headingList = [350] * 20
				self.headingSum = 350 * 20.0

			index+=1
			if (index >= 20):
				index = 0

	def getHeading(self):
		return round(self.headingSum/20.0) % 360
		
	def getMag(self):
		while(self.mag == self.prevMag):
			self.updateIMU()
		self.prevMag = self.mag
		return self.mag

	def getAccel(self):
		while(self.accel == self.prevAccel):
			self.updateIMU()
		self.prevMag = self.mag
		return self.accel
