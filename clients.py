import socket

class Client(object):
	_ip = ""
	_name = ""
	_protocol = ""
	_socket = None
	_server = None

	@property
	def ip(self):
		return self._ip
	@ip.setter
	def ip(self, value):
		self._ip = value

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def protocol(self):
		return self._protocol
	@protocol.setter
	def protocol(self, value):
		self._protocol = value

	@property
	def socket(self):
		return self._socket
	@socket.setter
	def socket(self, value):
		self._socket = value

	@property
	def server(self):
		return self._server
	@server.setter
	def server(self, value):
		self._server = value
	
	def __init__(self, ip="", name="", protocol="", socket=None, server=None):
		self.ip = ip
		self.name = name
		self.protocol = protocol
		self.socket = socket
		self.server = server

	def _disconnect(self):
		self.server.clients.remove(self)
		self.socket.close()
		
	def format(self, message):
		"""
		Here, we apply color, formatting, etc.
		"""
		if type(self.protocol).__name__ == "Raw":
			return self.name + ":" + message
		return message

	def receive(self):
		"""
		Receive the client data.
		"""
		try:
			return self.protocol.decode(self.protocol.readTcpSocket(self.socket))
		except Exception, e:
			print e.message
			self._disconnect()
			

	def send(self,data):
		"""
		Send data to this client
		"""
		try:
			self.protocol.sendTcpSocket(self.protocol.encode(data), self.socket)
		except Exception, e:
			print e.message
			self._disconnect()


	def fileno(self):
		"""The socket descriptor integer"""
		return self.socket.fileno()

