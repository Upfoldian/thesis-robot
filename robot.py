import TomLSM303C
import gpiozero
from math import atan2, degrees

from time import sleep

class Robot:

	def __init__(self, leftOn, leftDir, rightOn, rightDir, modePin):
		self.leftMotor = gpiozero.PWMLED(leftMotorPin, frequency=50)
		self.leftDir = gpiozero.LED(leftMotorDirPin)

		self.rightMotor = gpiozero.PWMLED(rightMotorPin, frequency=50)
		self.rightDir = gpiozero.LED(rightMotorDirPin)

		self.mode = gpiozero.LED(22)

		self.IMU = TomLSM303C.LSM303C() #check it with sudo i2cdetect -y 1 (should be 1D, 1E)
		self.updateIMU()
		mode.on()

	def stop(self):
		rightMotor.value = 0
		leftMotor.value = 0

	def start(self):
		rightMotor.value = 1
		leftMotor.value = 1


	def moveForward(self, distance=0.5):

		leftDir.off()
		rightDir.off()

		currentDistance = 0
		while(currentDistance < distance):
			self.start()

		self.stop()

	def moveBack(self, distance=0.5):
		leftDir.on()
		rightDir.on()

		currentDistance = 0

		while(currentDistance < distance):
			self.start()
		self.stop()

	def turnLeft(self, angle=90.0):

		leftDir.off()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle - 90) % 360
		while (currentAngle > targetAngle):
			leftMotor.value = 1
			currentAngle = self.getHeading()
		self.stop()


	def turnRight(self, angle=90.0):
		leftDir.off()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle + 90) % 360
		while (currentAngle < targetAngle):
			rightMotor.value = 1
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
