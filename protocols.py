import base64

def get_protocol(protocol_name):
	"""
        Try to instantiate a protocol from the protocol_name.
	If protocol_name is a list, this will return a list of the protocol found in the list.
	If protocol_name is already an instance of Protocol, protocol_name is returned
	protocol_name: The name of the protocol to instantiate.
	throws: NameError, if the protocol is not found
	returns: A Parser object|list of Parser object.
	"""
	if isinstance(protocol_name, list):
		protocols = []
		for v in protocol_name:
			protocols.append(get_protocol(v))
		return protocols
	if isinstance(protocol_name, Protocol):
		return protocol_name
	try:
		return globals()[protocol_name]()
	except KeyError, e:
		raise NameError("The parser '"+protocol_name+"' was not found. Is it properly defined in protocols.py? Is it correctly spelled?")



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
class BaseSixtyFour(Protocol):

	def encode(self, data):
		try:
			return base64.b64encode(data)
		except Exception, e:
			raise ProtocolIsNotRespectedError("Could not encode the data received to base64 using `base64` module.", e)
	def decode(self, data):
		try:
			return base64.b64decode(data)
		except TypeError, e:
			raise ProtocolIsNotRespectedError("Could not decode the data received using `base64` module.", e)

