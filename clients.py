import socket

class Client(object):
	_ip = ""
	_name = ""
	_protocol = ""
	_socket = None

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
	
	def __init__(self, ip="", name="", protocol="", socket=None):
		self.ip = ip
		self.name = name
		self.protocol = protocol
		self.socket = socket

	def format(self, message):
		if self.protocol == "RAW":
			return self.name + ":" + message + "\n"
		return message
	def fileno(self):
		"""The socket descriptor integer"""
		return self.socket.fileno()

