

import comms
import images
import motors
import IMU
import threading
from math import atan2, degrees


class Robot:
	def __init__(self, leftOn=17, leftDir=27, rightOn=23, rightDir=24, modePin=22):

		self.motors = motors.Motors()
		self.IMU = IMU.IMU()
		self.comms = comms.Comms()
		self.name = self.comms.getHostname()
		self.images = images.Images()

	def hasMessage(self):
		return self.comms.hasMessage()

	def readMessage(self):
		msg = self.comms.getMessage
		args = msg.split(" ")
		message = {"from": args[0], "command": args[1], "args": args[2:-1]}
		return message

		
	def feedbackMove(self, bearing, time=0):
		bearing = bearing % 360


	
