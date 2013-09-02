class Protocol(object):
	
	_buffer_size = 0

	@property
	def buffer_size(self):
		return self._buffer_size
	@buffer_size.setter
	def buffer_size(self, value):
		self._buffer_size = value

	def __init__(self, buffer_size = 1024):
		self.buffer_size = buffer_size

	def readTcpSocket(self, socket):
		"""
		This is called when the server wants to read data from a client.
		This is where you apply the protocol.
		"""
		raise NotImplementedError()
	def sendTcpSocket(self, data, socket):
		"""
		This is called when the server wants to send data to a client.
		"""
		raise NotImplementedError()

	def encode(self, data):
		"""
		This is called when data needs to be sent.
		If the data is already encoded properly, just return the data.
		"""
		raise NotImplementedError()
	def decode(self, data):
		"""
		This is called when data is received.
		The data returned by this function is passed to the parser.
		This should return a string, however, it can return  string or an object that the parser is waiting for.
		"""
		raise NotImplementedError()

class Raw(Protocol):
	"""
	Message sent with RAW protocol must always end with '\n'.
	"""
	def readTcpSocket(self, socket):
		data = ""
		while(data[-1:] != "\n"):
			data += socket.recv(self.buffer_size)
			if data == "":
				raise Exception("reading the socket sent us an empty string..") 
		return data
	def sendTcpSocket(self, data, socket):
		socket.sendall(data)

	def encode(self, data):
		if(data[-1:] != "\n"):
			data += "\n"
		return data

	def decode(self, data):
		return data.strip("\n")
