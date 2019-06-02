import TomLSM303C
import threading
from math import atan2, degrees
from mag_offsets import mag_x_offset, mag_y_offset, mag_z_offset

class IMU:

	def __init__(self):
		self.IMU = TomLSM303C.LSM303C() #check it with sudo i2cdetect -y 1 (should be 1D, 1E)

		self.headingSamples = 5
		self.headingList = [0] * self.headingSamples
		self.headingSum = 0.0
		self.avgHeading = 0.0

		self.xOff = mag_x_offset
		self.yOff = mag_y_offset
		self.zOff = mag_z_offset

		self.updateIMU()
		self.prevMag = self.mag
		self.prevAccel = self.accel

		self.halt = False
		self.thread = threading.Thread(target=self.headingThread).start()


	def getError(self, bearing):
		actual = self.avgHeading
		target = bearing
		error = target - actual
		#Positive error implies clockwise movement
		# Negative counterclockwise
		if (error >= 180.0):
			error = -360 + error
		elif (error <= -180.0):
			error = error + 360
		return error
	def updateIMU(self):
		self.IMU.read()
		accel = self.IMU.curAccel
		mag = self.IMU.curMag
		mag_x, mag_y, mag_z = mag

		mag_x -= self.xOff
		mag_y -= self.yOff
		mag_z -= self.zOff

		self.accel = accel
		self.mag = (mag_x, mag_y, mag_z)

	def headingThread(self):
		index = 0
		while(self.halt == False):
			self.avgHeading = round(self.headingSum/self.headingSamples)
			self.headingSum -= self.headingList[index]
			mag_x, mag_y, mag_z = self.getMag()
			curHeading = round(degrees(atan2(mag_y, mag_x)), 0) % 360

			# All these if statements handle the crossover point from 359 to 0 degrees
			# They do a little bit of magic to solve that (picks a point either side of
			# 0 to do the transision before it becomes a problem)

			if (self.avgHeading > 300 and curHeading < 120):
				self.headingList[index] = 360 + curHeading
			elif (self.avgHeading < 60 and curHeading > 250):
				self.headingList[index] = curHeading - 360
			else:
				self.headingList[index] = curHeading

			self.headingSum += self.headingList[index]

			if (self.avgHeading >= 370):
				self.headingList = [10] * self.headingSamples
				self.headingSum = 10.0 * self.headingSamples
			if (self.avgHeading <= -10):
				self.headingList = [350] * self.headingSamples
				self.headingSum = 350.0 * self.headingSamples

			index+=1
			if (index >= self.headingSamples):
				index = 0


	def getHeading(self):
		return self.avgHeading % 360
		
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
	def haltThread(self):
		self.halt = True

