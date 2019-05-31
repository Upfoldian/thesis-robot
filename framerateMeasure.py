import camera
import time

print("Starting...")
cam = camera.Camera()
time.sleep(0.5)

count = 0
timeSum = 0.0

try:
	while (count < 60):
		print("Run %d" % count)
		# tealName = "teal%d" % count
		# yellowName = "yellow%d" % count
		# purpleName = "purple%d" % count
		# combinedName = "all%d" % count

		# t0 = time.perf_counter()
		# cam.saveImage(True, tealName, yellowName, purpleName, combinedName)
		# t1 = time.perf_counter()
		# timeSum += t1-t0
		# count += 1
		t0 = time.perf_counter()
		curID = camera.imageID
		while(curID == camera.imageID):
			pass
		t1 = time.perf_counter()
		timeSum += t1 - t0

	timeAvg = (timeSum / 60.0) * 1000.0

	print("Average FPS: %f" % timeAvg)
except:
	cam.haltThread()
else:
	cam.haltThread()