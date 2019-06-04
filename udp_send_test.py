import socket


deets = ('0.0.0.0', 5000)
MESSAGE = "HI!"


print("IP: %s\tPort: %s\tMsg: %s" % (deets[0], deets[1], MESSAGE))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # TCP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind((deets[0], deets[1]))
sock.sendto(bytes(MESSAGE, "utf-8"), deets)
