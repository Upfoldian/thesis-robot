import robot
import time

test = robot.Robot()

count = 1
sum = 0
while(True):
	t0 = time.perf_counter()
	curID = test.camera.imageID
	while(curID == test.camera.imageID):
		pass
	t1 = time.perf_counter()
	tms = round((t1 - t0) * 1000)
	sum += tms
	print(sum/count)
	count+=1  