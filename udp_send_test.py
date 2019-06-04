import socket
import time
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
#message = b"Nero LISTEN Triangle SPIN"
message = b"Nero HI! Triangle"
server.sendto(message, ('255.255.255.255', 5000))
print("sent: HI!")