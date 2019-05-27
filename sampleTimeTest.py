import time
import robot

robot = robot.Robot()



count = 0
pollCount = 0
timeSum = 0.0
print("Starting...")
while(count < 50):
	t0 = time.perf_counter()

	x,y,z = robot.getAccel()
	x2,y2,z2 = robot.getAccel()

	while((x == x2) and (y == y2) and (z == z2)):
		pollCount += 1
		x2,y2,z2 = robot.getAccel()

	t1 = time.perf_counter()
	diff = t1 - t0
	print("Test %d: %f" (count, diff) )
	timeSum += diff

avg = timeSum / 50.0
pollAvg = pollCount / 50.0

print("Avg Sample Time: %f\nAvg Polls per Sample: %f" % (avg, pollAvg))

