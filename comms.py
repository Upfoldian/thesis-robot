import socket
import threading

class Comms:

  def __init__(self, ip="0.0.0.0", port=5000):
    self.ip = ip
    self.port = port
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # Enables Multicast
    self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    self.sock.bind((ip, port))
    self.stop = False
    self.messages = []
    
  def listen(self):
    while(self.stop == False):
      data, addr = self.sock.recvfrom(1024)
      msg = data.decode("utf-8")
      if (msg != "stop"):
        self.messages.insert(0, (msg,addr[0]))
  def start(self):
    self.stop = False
    t = threading.Thread(target=self.listen)
    t.daemon = True
    t.start()

  def halt(self):
    self.stop = True
    self.sock.sendto(bytes("stop", "utf-8"), ("127.0.0.1", 5000))

  def send(self, target_ip, port, msg):
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