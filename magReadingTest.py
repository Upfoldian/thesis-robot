import robot
import time

robot = robot.Robot()

print("mag_x, mag_y, mag_z")
prevSample = robot.getMag()
robot.startLeft(31)
startTime = time.perf_counter()
while(time.perf_counter() - startTime > 30):
	curSample = robot.getMag()
	mag_x, mag_y, mag_z = curSample
	if ((prevSample[0] != mag_x) or (prevSample[1] != mag_y) or (prevSample[2] != mag_z)):
		print("%f, %f, %f" % (mag_x, mag_y, mag_z))
		prevSample = curSample
