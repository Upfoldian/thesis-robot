import TomLSM303C
import gpiozero
import robot


robot = robot.Robot()

print("magx, magy, magz")
for x in range(100000):
	magx, magy, magz = robot.getMag()

	print("%.2f, %.2f, %.2f" % (magx, magy, magz))





