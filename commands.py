class Command(object):
	_server = None
	_caller = None
	_arguments = []
	
	@property
	def server(self):
		"""The server in which this command is executed"""
		return self._server
	@server.setter
	def server(self, value):
		self._server = value

	@property
	def caller(self):
		"""The socket representing the caller of this command"""
		return self._caller
	@caller.setter
	def caller(self, value):
		self._caller = value

	@property
	def arguments(self):
		"""The arguments passed to the command"""
		return self._arguments
	@arguments.setter
	def arguments(self, value):
		self._arguments = value

	def __init__(self, server = None, caller = None, *args):
		self.server = server
		self.caller = caller
		self.arguments = args

	def execute(self):
		"""Overide this method"""
		raise NotImplementedError()

class Exit(Command):
	"""
	Remove the caller from the server socket list and close it's connection.
	args:Takes no args
	"""
	def execute(self):
		self.server.socket_list.remove(self.caller)
		self.caller.close()

class Broadcast(Command):
	"""
	Broadcast a message to all current connected socket of the server.
	args[0]:The message to broadcast
	"""
	def execute(self):
		for socket in self.server.socket_list:
			if socket != self.server.server_socket and socket != self.caller:
				try:
					socket.sendall(self.arguments[0])
				except Exception, e:
					socket.close()
					self.server.socket_list.remove(socket)
