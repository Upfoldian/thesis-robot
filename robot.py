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

		self.nearbyRobots = set()
		self.knownTargets = set()

	def readMessage(self):
		message = self.comms.getMessage()
		return message
	
	def commsExperiment(self):
		#don't start until the other robot says hi
		friendName = ""
		while(True):
			print("sending HELLO?")
			self.comms.send("HELLO?")
			time.sleep(2)
			if (self.comms.hasMessage()):
				msg = self.readMessage()
				print(msg)
				if (msg['opcode'] == "HI!" and msg['args'][0] == self.name):
					friendName = msg['sender']
					break

		print ("I made a friend! %s is my new best friend." % friendName)

		while(True):

			if (self.comms.hasMessage()):
				msg = self.readMessage()
				if (msg['sender'] == friendName):
					print("%s told me to do this %s %s" % (friendName, msg['opcode'], str(msg['args'])) )
					self.parseMessage(msg)
					self.send("FINISH %s" % targetName)




	def coopExperiment(self, timestep = 0.4, speed = 0.5):
		"""
		Initial Conditions: 3 robots positions in a triangle formation, with each robot as a vertex.
		Targets are places at a random interval between the three robots.
		

		Successful Experiment: The robots each claim a target based on the shortest distance.
		"""

		self.nearbyRobots = set()
		names = ["teal", "purple", "blue"]
		self.sync()
		readings = self.sweep()
		avgs = {"teal": 999, "purple": 999, "blue": 999}

		for name in names:
			if (len(readings[name]) != 0):
				distSum = 0
				bearSum = 0
				for reading in readings[name]:
					bearSum += reading[0]
					distSum += reading[1]
				avgDist = round(distSum / len(readings[name]),1)
				#avgBear = round(bearSum / len(readings[name]),1)
				avgs[name] = avgDist

		graph = {self.comms.getHostname(): avgs}

		best = sorted(avgs, key= lambda x: avgs[x][1])
		
		minTarget = best.pop(0)
		minDist = avgs[minTarget][1]
		#print(readings)
		print(avgs)

		self.sync()
		for targetName in avgs.keys():
			self.comms.send("TARGET %s %d" % (targetName, avgs[targetName][1]))
		time.sleep(1)
		while (self.comms.hasMessage()):
			msg = self.readMessage()
			if (msg['opcode'] == "TARGET"):
				print(msg)
				sender = msg["sender"]
				col = msg["args"][0]
				dist = float(msg["args"][1])
				if sender not in graph:
					graph[sender] = {"teal": 999, "purple": 999, "blue": 999}
				graph[sender][col] = dist
		
		bestPath = 999
		bestAssignment = []
		robotNames = graph.keys()
		# way better ways to do this, i am just very lazy
		for i in names:
			for j in names:
				for k in names:
					if (i == j or j == k):
						continue
					path = 0
					colours = [i,j,k]
					assignemt = []
					for n in len(robotNames):
						r = robotNames[n]
						c = colours[n]
						d = graph[r][c] 
						path += d
						assignment.append((r,c,d))
					if (path < bestPath):
						bestPath = path
						bestAssignemt = assignment




		
		self.sync()
		print(bestAssignment)

	def sync(self, robotsNeeded = 2):
		self.comms.messages = []
		uniqueSyncs = set()
		while(True):
			self.comms.send("SYNC")
			if (self.comms.hasMessage()):
				msg = self.readMessage()
				if (msg['opcode'] == "SYNC"):
					uniqueSyncs.add(msg['sender'])
			if (len(uniqueSyncs) >=2):
				self.comms.messages = []
				break



	def sweep(self, timestep = 0.2, speed = 0.5, arc=120):
		"""
		Robots survey an arc in front of them and collect readings on spotted targets.
		Returns the collection of data found for each target

		"""
		originalHeading = self.IMU.getHeading()
		rightLimit = (originalHeading + arc/2) % 360
		leftLimit = (originalHeading - arc/2) % 360

		readings = {'teal': [], 'purple': [], 'blue': []}

		count = 0
		while(abs(self.IMU.getError(rightLimit)) > 10):
			# Sweep right first
			time.sleep(0.4)
			self.camera.saveImage(originalName=("original%d"%count),combinedName=("all%d"%count))
			count+=1
			targets = self.camera.targets
			heading = self.IMU.getHeading()
			for target in targets:
					targetName = target['targetName']
					x,y,w,h = target['dims']
					headingEst = self.targetBearingEstimate(target['dims'], heading)
					distanceEst = self.targetDistanceEstimate(target['dims'])

					readings[targetName].append((headingEst, distanceEst))
			self.motors.spinRight(speed, timestep)

		while(abs(self.IMU.getError(leftLimit)) > 10):
			# Sweep left second
			time.sleep(0.4)
			self.camera.saveImage(originalName=("original%d"%count),combinedName=("all%d"%count))
			count+=1
			targets = self.camera.targets
			heading = self.IMU.getHeading()
			for target in targets:
					targetName = target['targetName']
					x,y,w,h = target['dims']
					headingEst = self.targetBearingEstimate(target['dims'], heading)
					distanceEst = self.targetDistanceEstimate(target['dims'])

					readings[targetName].append((headingEst, distanceEst))
			self.motors.spinLeft(speed, timestep)

		while(abs(self.IMU.getError(originalHeading)) > 5):
			# Get back to start
			if (self.IMU.getError(originalHeading) > 0):
				self.motors.spinRight(speed,timestep/2)
				time.sleep(0.02)
			else:
				self.motors.spinLeft(speed,timestep/2)
				time.sleep(0.02)

		return readings

	def searchExperiment(self, timestep = 0.4, speed = 0.5):
		""" 
		Robot spins on the spot looking for targets. Once a target is found, the robot stops and obtains
		a bearing and distance estimate of the target. It then broadcasts that infomation to nearby robots.
		Once reporting is complete, it continues spinning to search for new targets. The experiment halts
		once a full rotation has been completed.
		"""
		#Reset targets seen
		self.knownTargets = set()

		# loop until within 5 degrees of finish point
		for i in range(2):
			count = 0
			while(count <= 4):
				targets = self.camera.targets
				heading = self.IMU.getHeading()
				for target in targets:
					targetName = target['targetName']
					x,y,w,h = target['dims']

					headingEst = self.targetBearingEstimate(target['dims'], heading)
					distanceEst = self.targetDistanceEstimate(target['dims'])
					print("Target: %s\tEst Heading: %d\tDistance Est: %d" % (targetName, headingEst, distanceEst))
				if (i == 0):
					self.camera.saveImage(originalName=("originalRight%d"%count),combinedName=("allRight%d"%count))
					self.motors.spinRight(speed, timestep)
				elif (i == 1):
					self.camera.saveImage(originalName=("originalLeft%d"%count),combinedName=("allLeft%d"%count))
					self.motors.spinLeft(speed, timestep)
				time.sleep(1)
				count+=1

		self.motors.stop()


	def targetBearingEstimate(self, dims, heading):
		"""
		Gets an estimated heading from the location of the midpoint of the target in screen. From
		testing, 1 pixel sidewards is approximately 0.21 degrees from current heading. This value
		has been linearised as it's actually close to 0.22 near the center and 0.19 towards the
		edges. However, this results in approximately 2-3 degrees of error worse case, which is 
		about the noise level present in the compass anyway.
		"""
		x,y,w,h = dims
		midpoint = x + w/2
		distFromCenter = midpoint - self.camera.rows
		headingEst = heading + round(distFromCenter * 0.21)
		return headingEst

	def targetDistanceEstimate(self, dims):
		"""
		Gets an estimated distance from from of robot. Strictly speaking, this needs to be combined
		with a bearing to get a true distance, but this is good enough. Matching measured area data
		of the target, the formula to find distance is 76.1*area**-0.695
		"""
		x,y,w,h = dims
		return round((76.1 * (w*h)**-0.695)*100.0)

	def lockTarget(self, targetName):
		target = next((target for target in self.camera.targets if target["targetName"] == targetName), None)
		horizontalMidpoint = self.camera.cols/2
		x,y,w,h = target['dims']
		print("Locking target!")
		while(target != None or abs(horizontalMidpoint - x) > 5):
			print("curX: %d" % x)
			if (x > horizontalMidpoint):
				self.motors.spinLeft(0.4)
			else:
				self.motors.spinRight(0.4)
			target = next((target for target in self.camera.targets if target["targetName"] == targetName), None)
			if (target == None):
				print("wack")
				return False

		self.motors.stop()
		return True


	def feedbackMoveExperiment(self, bearing, duration=1, speed=1):
		# Setup and error checks
		bearing = bearing % 360
		startTime = time.perf_counter()
		curTime = time.perf_counter()

		print("Starting feedback experiment, current bearing is: %f" % self.IMU.getHeading())

		while(curTime - startTime < duration):
			error = self.IMU.getError(bearing)
			magnitude = abs(error)
			leftVal, rightVal = 0,0
			if(magnitude > 5):
				response = numpy.interp(magnitude, [0, 180], [0.4,speed]) # static term

				if error > 0:
					# clockwise
					self.motors.stop()
					self.motors.spinRight(response)
					leftVal, rightVal = 1-response, response
				else:
					# counterclockwise
					self.motors.stop()
					self.motors.spinLeft(response)
					leftVal, rightVal = response, 1-response
			else: 
				self.motors.stop()
				#leftVal = speed
				#rightVal = speed

			self.motors.start(leftVal, rightVal)

			curTime = time.perf_counter()
			print("\terr: %f\tL: %f\tR: %f" % (error, leftVal, rightVal))
		# Clean up
		self.motors.stop()
		time.sleep(1)
		print("Experiment complete, final heading is: %f" % self.IMU.getHeading())

	def stopAndAlign(self, bearing, duration=3, speed=1):
		bearing = bearing % 360
		t0 = time.time()
		t1 = time.time()

		while(t1 - t0 < duration):
			error = self.IMU.getError(bearing)
			magnitude = abs(error)
			leftVal, rightVal = 0,0

			if (magnitude > 4):
				if (magnitude < 10):
					response = numpy.interp(magnitude, [0, 180], [0.4,speed]) # static term
				else:
					response = 0.41
				self.motors.stop()
				if error > 0:
					# clockwise
					self.motors.spinRight(response)
					#leftVal, rightVal = 1-response, response
				else:
					# counterclockwise
					self.motors.spinLeft(response)
					#leftVal, rightVal = response, 1-response
			t1 = time.time()
		self.motors.stop()
	def parseMessage(self, msg):

		sender = msg["sender"]
		opcode = msg["opcode"]
		args = msg["args"]

		if opcode == "HELLO?":
			# If you hear a robot saying hello?, you send back hi! to let them know you can hear them
			reply = "HI! %s" % self.comms.getHostname()
			self.nearbyRobots.add(sender)
			self.comms.send(reply)
		elif opcode == "HI!":
			# If you hear a robot saying Hi!, back to something
			# If they replied to you, they can hear you
			# if not, don't add them
			if (sender == self.comms.getHostname()):
				self.nearbyRobots.add(sender)
		elif opcode == "FOUND":
			# Report to the network that you've found a target and the position you found it
			target, heading, estDist, curX, curY = args
		elif opcode == "LISTEN":
			# Boss another robot around
			targetRobot, command = args
			if (self.name == targetRobot):
				if (command == "MOVE"):
					self.motors.start(time=1)
				elif (command == "SPIN"):
					self.motors.spinLeft(time=2.2)
				else:
					print("what do I do???")
		elif opcode == "FINISH":
			targetRobot, command = args
			if (self.name == targetRobot):
				pass
		elif opcode == "CLAIM":
			# Claim exclusive use of a target
			target, estDist = args
		elif opcode == "LOCK":
			# Lock in exclusive use of a target
			target = args
		else:
			#what the heck is this
			pass
	def calibrateCompass(self, calibrationTime=10, power=1):
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
		self.motors.spinLeft(power)
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
		self.IMU.xOff = xOffset
		self.IMU.yOff = yOffset
		self.IMU.zOff = zOffset

	def exit(self):
		""" Stops all the threads running all over the place. """
		self.IMU.haltThread()
		self.camera.haltThread()
		self.comms.haltThread()
		time.sleep(0.5)


	
