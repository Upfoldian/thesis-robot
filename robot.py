import comms
import camera
import motors
import IMU
import threading
import time
from numpy import interp

class Robot:
	def __init__(self):

		self.motors = motors.Motors()
		self.IMU = IMU.IMU()
		self.comms = comms.Comms()
		self.name = self.comms.getHostname()
		self.camera = camera.Camera()

		self.nearbyRobots = {}
		self.knownTargets = {}
	def hasMessage(self):
		return self.comms.hasMessage()

	def readMessage(self):
		msg = self.comms.getMessage
		args = msg.split(" ")
		message = {"from": args[0], "opcode": args[1], "args": args[2:-1]}
		return message
		

	def feedbackMoveExperiment(self, bearing, time=1, speed=1):
		bearing = bearing % 360
		startTime = time.perf_counter()
		curTime = time.perf_counter()

		print("Starting feedback experiment, current bearing is: %f" % self.IMU.getHeading())

		while(curTime - startTime < time):
			error = self.IMU.getError(bearing)
			magnitude = abs(error)
			leftVal = speed
			rightVal = speed
			if(magnitude > 3.5):
				response = numpy.interp(magnitude, [0, 180], [0,speed])
				if error > 0:
					leftVal = response
					rightVal = -response
				else:
					leftVal = -response
					rightVal = response
			self.motor.start(leftVal, rightVal)
		self.motor.stop()
		time.sleep(1)
		print("Experiment complete, final heading is: %f" % self.IMU.getHeading())


	def targetFound(self, box):
		
	def parseMessage(self, msg):
		sender = msg["from"]
		opcode = msg["opcode"]
		args = msg["args"]

		if opcode == "HELLO?":
			# If you hear a robot saying hello?, you send back hi! to let them know you can hear them
			reply = "HI! %s" % self.name
			senderName = args[0]
			self.nearbyRobots.add(senderName)
			self.comms.send(sender, reply)
		elif opcode == "HI!":
			# If you hear a robot saying Hi!, back to something
			senderName = args[0]
			# If they replied to you, they can hear you
			# if not, don't add them
			if (senderName == self.name):
				self.nearbyRobots.add(senderName)
		elif opcode == "FOUND":
			# Report to the network that you've found a target and the position you found it
			target, heading, estDist, curX, curY = args

		elif opcode == "LISTEN":
			# Boss another robot around
			targetRobot, command = args
		elif opcode == "IAMHERE":
			# Let another robot know where you are
			curX, curY = args
		elif opcode == "CLAIM":
			# Claim exclusive use of a target
			target, estDist = args
		elif opcode == "LOCK":
			# Lock in exclusive use of a target
			target = args
		elif opcode == "START":
			# Start an experiment, intended to be sent by a non-robot controller (i.e. person at a laptop)
		elif opcode == "STOP":
			# Stop an experiment, intended to be sent by a non-robot controller (i.e. person at a laptop)
		else:
			#what the heck is this

	def exit(self):
		""" Stops all the threads running all over the place. """
		self.IMU.haltThread()
		self.camera.haltThread()
		self.comms.haltThread()
		time.sleep(2)


	
