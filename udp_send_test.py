import socket


multicast_group = ("224.1.1.1", 5000)
MESSAGE = "YO!"


print("IP: %s\tPort: %s\tMsg: %s" % (multicast_group[0], multicast_group[1], MESSAGE))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # TCP
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
sock.sendto(bytes(MESSAGE, "utf-8"), multicast_group)
