import gpiozero
import threading
from time import sleep



class Motors:

	def __init__(self, leftOn=17, leftDir=27, rightOn=23, rightDir=24, modePin=22):
		# Motor Stuff
		self.leftMotor = gpiozero.PWMLED(leftOn, frequency=50)
		self.leftDir = gpiozero.LED(leftDir)

		self.rightMotor = gpiozero.PWMLED(rightOn, frequency=50)
		self.rightDir = gpiozero.LED(rightDir)

		self.mode = gpiozero.LED(modePin)
		self.mode.on()

	def stop(self):
		self.leftDir.off()
		self.rightDir.off()

		self.rightMotor.value = 0
		self.leftMotor.value = 0

	def start(self, leftVal=1, rightVal=1, time=0):
		self.rightMotor.value = leftVal
		self.leftMotor.value = rightVal

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

	def turnLeft(self, angle=90.0):

		self.spinLeft()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle - angle) % 360
		self.spinLeft()
		while (currentAngle < targetAngle -3 or currentAngle > targetAngle + 3):
			currentAngle = self.getHeading()
		self.stop() 


	def turnRight(self, angle=90.0):
		
		self.spinRight()

		currentAngle = self.getHeading()
		targetAngle = (currentAngle + angle) % 360
		while (currentAngle < targetAngle -3 or currentAngle > targetAngle + 3):
			currentAngle = self.getHeading()
		self.stop()