import comms
import camera
import motors
import IMU
import threading
import time
import numpy

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
		

	def feedbackMoveExperiment(self, bearing, duration=1, speed=1):
		bearing = bearing % 360
		startTime = time.perf_counter()
		curTime = time.perf_counter()

		print("Starting feedback experiment, current bearing is: %f" % self.IMU.getHeading())

		while(curTime - startTime < duration):
			error = self.IMU.getError(bearing)
			magnitude = abs(error)
			leftVal = speed
			rightVal = speed
			self.motors.stop()
			if(magnitude > 3.5):
				response = numpy.interp(magnitude, [0, 180], [0,speed])
				self.motors.stop()
				if error < 0:
					leftVal = response
					rightVal = 1-response
					self.motors.rightDir.on()
				else:
					leftVal = 1-response
					rightVal = response
					self.motors.leftDir.on()
			self.motors.start(leftVal, rightVal)
			curTime = time.perf_counter()
			print("\tcurrent: %f" % self.IMU.getHeading())
		self.motors.stop()
		time.sleep(1)
		print("Experiment complete, final heading is: %f" % self.IMU.getHeading())


	def targetFound(self, box):
		pass
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
			pass
		elif opcode == "STOP":
			# Stop an experiment, intended to be sent by a non-robot controller (i.e. person at a laptop)
			pass
		else:
			#what the heck is this
			pass
	def calibrateCompass(self, calibrationTime=10):
		""" 
		Function that calibrates the internal compass on the IMU. It spins the robot for a specified
		amount of time (10s default) and collects readings on all axes. It then calculates the range seen
		across the spin and calculates the midpoint value to add/subtract to the values to get a balanced
		range of readings across a full rotation. It then writes the values to mag_offsets.py
		"""
		xReadings = []
		yReadings = []
		zReadings = []

		t0 = time.time()
		t1 = time.time()
		self.motors.spinLeft()
		while((t1 - t0) < calibrationTime):
			x,y,z = self.IMU.getMag()
			xReadings.append(x)
			yReadings.append(y)
			zReadings.append(z)
			t1 = time.time()

		xMax, yMax, zMax = max(xReadings), max(yReadings), max(zReadings)
		xMin, yMin, zMin = min(xReadings), min(yReadings), min(zReadings)

		xOffset = (round((xMax - xMin)/2.0) + xMin) + self.IMU.xOff
		yOffset = (round((yMax - yMin)/2.0) + yMin) + self.IMU.yOff
		zOffset = (round((zMax - zMin)/2.0) + zMin) + self.IMU.zOff

		f = open("mag_offsets.py", "w")
		f.write("mag_x_offset = %f\nmag_y_offset = %f\nmag_z_offset = %f\n" % (xOffset, yOffset, zOffset))
		f.close()

		self.motors.stop()

	def exit(self):
		""" Stops all the threads running all over the place. """
		self.IMU.haltThread()
		self.camera.haltThread()
		self.comms.haltThread()
		time.sleep(0.5)


	
