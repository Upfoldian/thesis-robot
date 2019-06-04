import TomLSM303C
import gpiozero
import robot
import socket


multicast_group = ("192.168.1.143", 5000)
MESSAGE = "hello"


print("IP: %s\tPort: %s\tMsg: %s" % (multicast_group[0], multicast_group[1], MESSAGE))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # TCP
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.sendto(bytes(MESSAGE, "utf-8"), multicast_group)
