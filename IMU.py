import TomLSM303C
import threading
import time
from math import atan2, degrees
from mag_offsets import mag_x_offset, mag_y_offset, mag_z_offset

class IMU:

	def __init__(self):
		self.IMU = TomLSM303C.LSM303C() #check it with sudo i2cdetect -y 1 (should be 1D, 1E)
		self.updateIMU()

		self.headingList = [0] * 20
		self.headingSum = 0.0
		# So Control+C kills them, but in a bad way because im lazy
		self.thread = threading.Thread(target=self.headingThread).start()
		self.halt = False
		# Fresh update variables
		self.prevMag = self.mag
		self.prevAccel = self.accel
		# Bearing and feedback
		self.bearing = None


	def getError(self):
		actual = self.getHeading()
		target = self.bearing
		error = target - actual

		if (error >= 180.0):
			error = -360 + error
		elif (error <= -180.0):
			error = error + 360
		return error
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
		while(self.halt == False):
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
	def haltThread(self):
		self.halt = True
		time.sleep(0.2)
		self.thread.stop()

