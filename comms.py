import socket
import threading

class Comms:

	def __init__(self, ip="255.255.255.255", port=5000):
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Enables Multicast
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.sock.bind((ip, port))
		self.halt = False
		self.messages = []
		self.thread = threading.Thread(target=self.listen)
		
	def listen(self):
		while(self.halt== False):
			data, addr = self.sock.recvfrom(1024)
			msg = data.decode("utf-8")
			self.messages.insert(0, (msg,addr[0]))

	def send(self, msg, target_ip="255.255.255.255", port=5000):
		# Should multicast this to all devices listening to the multicast group (i.e. all of them)
		# message format will be something like the following:
		#   <hostname> <megType> <data associated with msg type>
		# some example msgTypes could be:
		#     HELLO?                                      - asks the network who can hear me
		#     FOUND <thing> <heading> <cur_x> <cur_y> <est. distance>   - reports a target sighting
		#     LISTENUP <target> <command> <duration>    - tells another robot to do a thing (i.e. stop) with arguments that depend on the thing to do
		#        
		msg = self.getHostname() + " " + msg      
		self.sock.sendto(bytes(msg, "utf-8"), (target_ip, port))

	def hasMessage(self):
		if(len(self.messages) != 0):
			return True
		else:
			return False

	def getMessage(self):
		if (self.hasMessage):
			return self.messages.pop()
		else:
			return "You have 0 voice messages."

	def getHostname(self):
		return socket.gethostname()

	def haltThread(self):
		self.halt = True