import camera
import time

cam = camera.Camera()


count = 0
timeSum = 0.0

while (count < 60):
	tealName = "teal%d" % count
	yellowName = "yellow%d" % count
	purpleName = "purple%d" % count
	combinedName = "all%d" % count

	t0 = time.perf_counter()
	cam.saveImage(tealName, yellowName, purpleName, combinedName)
	t1 = time.perf_counter()
	timeSum += t1-t0

timeAvg = (timeSum / 60.0) * 1000.0

print("Average FPS: %f" % timeAvg)