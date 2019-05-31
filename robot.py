import comms
import camera
import motors
import IMU
import threading


class Robot:
	def __init__(self):

		self.motors = motors.Motors()
		self.IMU = IMU.IMU()
		self.comms = comms.Comms()
		self.name = self.comms.getHostname()
		self.camera = camera.Camera()

	def hasMessage(self):
		return self.comms.hasMessage()

	def readMessage(self):
		msg = self.comms.getMessage
		args = msg.split(" ")
		message = {"from": args[0], "command": args[1], "args": args[2:-1]}
		return message

		
	def feedbackMove(self, bearing, time=0):
		bearing = bearing % 360

	def exit(self):
		""" Stops all the threads running all over the place. """
		self.IMU.haltThread()
		self.camera.haltThread()
		self.comms.haltThread()


	
