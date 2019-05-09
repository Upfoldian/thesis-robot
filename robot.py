<<<<<<< HEAD
import TomLSM303C
import gpiozero
from math import atan2, degrees

from time import sleep

class Robot:
	def __init__(self, leftOn=17, leftDir=27, rightOn=23, rightDir=24, modePin=22):


		# Left Motor Pin = 
		self.leftMotor = gpiozero.PWMLED(leftOn, frequency=50)
		self.leftDir = gpiozero.LED(leftDir)

		self.rightMotor = gpiozero.PWMLED(rightOn, frequency=50)
		self.rightDir = gpiozero.LED(rightDir)

		self.mode = gpiozero.LED(modePin)

		self.IMU = TomLSM303C.LSM303C() #check it with sudo i2cdetect -y 1 (should be 1D, 1E)
		self.updateIMU()
		self.mode.on()

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
	def spin(self, time=0):
		self.rightMotor.value = 1
		self.leftDir.on()

		if (time != 0):
			sleep(time)
			self.stop()
		
	def backUp(self, time=0):
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

		self.leftDir.off()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle - angle) % 360
		while (currentAngle > targetAngle):
			self.leftMotor.value = 1
			currentAngle = self.getHeading()
		self.stop()


	def turnRight(self, angle=90.0):
		self.leftDir.off()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle + angle) % 360
		while (currentAngle < targetAngle):
			self.rightMotor.value = 1
			currentAngle = self.getHeading()
		self.stop()

	def updateIMU(self):
		accel, mag = self.IMU.read()
		self.accel = accel
		self.mag = mag

	def getHeading(self):
		accel, mag = self.IMU.read()
		mag_x, mag_y, mag_z = mag
		curHeading = round(degrees(atan2(mag_y, mag_x)), 0) % 360
		return curHeading
=======
import TomLSM303C
import gpiozero
from math import atan2, degrees

from time import sleep

class Robot:
	def __init__(self, leftOn=17, leftDir=27, rightOn=23, rightDir=24, modePin=22):


		# Left Motor Pin = 
		self.leftMotor = gpiozero.PWMLED(leftOn, frequency=50)
		self.leftDir = gpiozero.LED(leftDir)

		self.rightMotor = gpiozero.PWMLED(rightOn, frequency=50)
		self.rightDir = gpiozero.LED(rightDir)

		self.mode = gpiozero.LED(modePin)

		self.IMU = TomLSM303C.LSM303C() #check it with sudo i2cdetect -y 1 (should be 1D, 1E)
		self.updateIMU()
		self.mode.on()

	def stop(self):
		self.rightMotor.value = 0
		self.leftMotor.value = 0

	def start(self, time=0):
		self.rightMotor.value = 1
		self.leftMotor.value = 1

		if (time != 0):
			sleep(time)
			self.stop()

	def backUp(self, time=0):
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

		self.leftDir.off()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle - angle) % 360
		while (currentAngle > targetAngle):
			self.leftMotor.value = 1
			currentAngle = self.getHeading()
		self.stop()


	def turnRight(self, angle=90.0):
		self.leftDir.off()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle + angle) % 360
		while (currentAngle < targetAngle):
			self.rightMotor.value = 1
			currentAngle = self.getHeading()
		self.stop()

	def updateIMU(self):
		accel, mag = self.IMU.read()
		self.accel = accel
		self.mag = mag

	def getHeading(self):
		accel, mag = self.IMU.read()
		mag_x, mag_y, mag_z = mag
		curHeading = round(degrees(atan2(mag_y, mag_x)), 0) % 360
		return curHeading
>>>>>>> 1b737d4ef01ab4076773b97f52dbbcba54b4a4cb
