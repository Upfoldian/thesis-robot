import time
import robot

# Some sanity testing for the LSM303C sampling rate



robot = robot.Robot()

count = 0
pollCount = 0
timeSum = 0.0
print("Starting Accel...")
while(count < 500):
	t0 = time.perf_counter()

	x,y,z = robot.getAccel()
	x2,y2,z2 = robot.getAccel()

	while((x == x2) and (y == y2) and (z == z2)):
		pollCount += 1
		x2,y2,z2 = robot.getAccel()

	t1 = time.perf_counter()
	diff = t1 - t0
	#print("Test %d: %f" % (count, diff) )
	timeSum += diff
	count += 1

avg = (timeSum / 500.0) * 1000.0
pollAvg = pollCount / 500.0

print("ACCEL: Avg Sample Time (ms): %f\nAvg Polls per Sample: %f" % (avg, pollAvg))


count = 0
pollCount = 0
timeSum = 0.0
print("Starting Mag...")
while(count < 500):
	t0 = time.perf_counter()

	x,y,z = robot.getMag()
	x2,y2,z2 = robot.getMag()

	while((x == x2) and (y == y2) and (z == z2)):
		pollCount += 1
		x2,y2,z2 = robot.getMag()

	t1 = time.perf_counter()
	diff = t1 - t0
	#print("Test %d: %f" % (count, diff) )
	timeSum += diff
	count += 1

avg = (timeSum / 500.0) * 1000.0
pollAvg = pollCount / 500.0

print("MAG: Avg Sample Time (ms): %f\nAvg Polls per Sample: %f" % (avg, pollAvg))
