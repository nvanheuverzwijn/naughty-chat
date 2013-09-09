class DataCouldNotBeReadError(Exception):
	"""
	This is raised whenever the socket returned an empty string.
	"""
	pass
class ProtocolIsNotRespectedError(Exception):
	"""
	This is raised whenever the protocol is not respected. Raising this exception will not kill the connection but will
	make the server wait for more data.
	"""
	pass

class Protocol(object):
	
	_buffer_size = 0
	_fetched_data = ""

	@property
	def buffer_size(self):
		return self._buffer_size
	@buffer_size.setter
	def buffer_size(self, value):
		self._buffer_size = value

	@property
	def fetched_data(self):
		return self._fetched_data
	@fetched_data.setter
	def fetched_data(self, value):
		self._fetched_data = value

	def __init__(self, buffer_size = 1024):
		self.buffer_size = buffer_size

	def readTcpSocket(self, socket):
		"""
		This is called when the server wants to read data from a client.
		"""
		self.fetched_data += socket.recv(self.buffer_size)
		if self.fetched_data == "":
			raise DataCouldNotBeReadError("Socket returned empty string.") 
		decoded_data = self.decode(self.fetched_data)
		self.fetched_data = ""
		return decoded_data
	def sendTcpSocket(self, data, socket):
		"""
		This is called when the server wants to send data to a client.
		"""
		socket.sendall(self.encode(data))

	def encode(self, data):
		"""
		This is called when data needs to be sent.
		This is where you apply the protocol policy regarding encoding.
		If the data is already encoded properly, just return the data.
		You must throw ProtocolIsNotRespectedError if the protocol cannot be enforced.
		"""
		raise NotImplementedError()
	def decode(self, data):
		"""
		This is called when data is received.
		This is where you apply the protocol policy regarding decoding.
		The data returned by this function is passed to the parser.
		This should return a string, however, it can return  string or an object that the parser is waiting for.
		You must throw ProtocolIsNotRespectedError if the protocol cannot be enforced.
		"""
		raise NotImplementedError()

class Raw(Protocol):
	"""
	Message sent with RAW protocol must always end with '\n'.
	"""

	def encode(self, data):
		try:
			data += "\n"
		except Exception, e:
			raise ProtocolIsNotRespectedError("Could not append \\n to the data.", e)
		return data

	def decode(self, data):
		if data[-1:] != "\n":
			raise ProtocolIsNotRespectedError("The data receive did not end with a line feed.") 
		return data.strip("\n")
