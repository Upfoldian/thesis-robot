
msg = {'from':'test', 'opcode': 'HELLO!', 'args': ['blue', '180', '30.56', '0','1']}

sender = msg["from"]
opcode = msg["opcode"]
args = msg["args"]

if opcode == "HELLO?":
	# If you hear a robot saying hello?, you send back hi! to let them know you can hear them
	#reply = "HI! %s" % self.name
	#senderName = args[0]
	#self.nearbyRobots.add(senderName)
	#self.comms.send(sender, reply)
	print("hello?")
elif opcode == "HI!":
	# If you hear a robot saying Hi!, back to something
	#senderName = args[0]
	# If they replied to you, they can hear you
	# if not, don't add them
	print("hi! %s" % sender)
elif opcode == "FOUND":
	# Report to the network that you've found a target and the position you found it
	target, heading, estDist, curX, curY = args
	print("found: %s %s %s %s %s" % (target,heading,estDist,curX,curY))
elif opcode == "LISTEN":
	# Boss another robot around
	#targetRobot, command = args
	print("listen")
elif opcode == "IAMHERE":
	# Let another robot know where you are
	#curX, curY = args
	print("iamhere")
elif opcode == "CLAIM":
	# Claim exclusive use of a target
	target, estDist = args
	print("claim")
elif opcode == "LOCK":
	# Lock in exclusive use of a target
	target = args
	print("lock")
elif opcode == "START":
	# Start an experiment, intended to be sent by a non-robot controller (i.e. person at a laptop)
	print("start")
elif opcode == "STOP":
	# Stop an experiment, intended to be sent by a non-robot controller (i.e. person at a laptop)
	print("stop")
else:
	#what the heck is this
	print("yuck")