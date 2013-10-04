import socket
import protocols

class SocketError(Exception):
	pass
class ClientIsNotFinishedSendingError(Exception):
	pass
class CouldNotSendRequestError(Exception):
	pass

class Client(object):
	_ip = ""
	_name = ""
	_protocol = None
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
	
	def __init__(self, ip="", name="", protocol=None, socket=None, server=None):
		self.ip = ip
		self.name = name
		self.protocol = protocol
		self.socket = socket
		self.server = server

	def format(self, message):
		"""
		Here, we apply color, formatting, etc.
		"""
		if type(self.protocol[0]).__name__ == "Raw":
			return self.name + ":" + message
		return message

	def receive(self):
		"""
		Receive the client data.
		"""
		try:
			data = self.protocol[0].readTcpSocket(self.socket)
			if len(self.protocol) > 1:
				for protocol in self.protocol[1:]:
					data = protocol.decode(data)
			
			return data
		except protocols.ProtocolIsNotRespectedError, e:
			raise ClientIsNotFinishedSendingError("The client is not finished sending it's message.", e)
		except protocols.DataCouldNotBeReadError, e:
			raise SocketError("Client socket died", e)
			
	def send(self,data):
		"""
		Send data to this client
		"""
		try:
			if len(self.protocol) > 1:
				for protocol in reversed(self.protocol[1:]):
					data = protocol.encode(data)
			self.protocol[0].sendTcpSocket(data, self.socket)
		except protocols.ProtocolIsNotRespectedError, e:
			raise CouldNotSendRequestError("", e)
		except Exception, e:
			raise SocketError("Client socket died", e)

	def fileno(self):
		"""The socket descriptor integer"""
		return self.socket.fileno()

