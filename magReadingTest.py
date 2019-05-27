import robot
import time

robot = robot.Robot()

print("mag_x, mag_y, mag_z")
prevSample = robot.getMag()
robot.startLeft(31)
startTime = time.perf_counter()
while(time.perf_counter() - startTime > 30):
	mag_x, mag_y, mag_z = robot.getMag()
	if ((prevSample[0] == mag_x) and (prevSample[1] == mag_y) and (prevSample[2] == mag_z)):
		#nothin
	else:
		print("%f, %f, %f" % (robot.getMag()))


