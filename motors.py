import gpiozero
import threading
from time import sleep

"""
Basic class that implements a lot of the movement options for the robot. Uses the gpiozero PWM library for simplicity.
Setting a motor value to 1 indicates full power, and 0 no power, with default operation, and when reverse, full power is 0 and no power is 1.
"""

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

	def spinLeft(self, power=1, time=0):
		self.rightMotor.value = power
		self.leftMotor.value = 1-power
		self.leftDir.on()

		if (time != 0):
			sleep(time)
			self.stop()

	def spinRight(self, power=1,time=0):
		self.leftMotor.value = power
		self.rightMotor.value = 1-power
		self.rightDir.on()

		if (time != 0):
			sleep(time)
			self.stop()
		
	def reverse(self, power=1, time=0):
		self.leftMotor.value = 1-power
		self.rightMotor.value = 1-power
		self.leftDir.on()
		self.rightDir.on()

		if(time != 0):
			sleep(time)
			self.stop()

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