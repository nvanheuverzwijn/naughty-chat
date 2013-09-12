def getCommand(command_name, server=None, caller=None, arguments=[]):
	"""
	Try to instantiate a command from the command_name
	command_name: The name of the command to instantiate.
	throws: NameError, if the command is not found
	returns: A Command object.
	"""
	try:
		return globals()[command_name](server, caller, arguments)
	except KeyError, e:
		raise NameError("The command '"+command_name+"' was not found. Is it properly defined in commands.py? Is it correctly spelled?")

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
		"""The Client representing the caller of this command"""
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

	def __init__(self, server = None, caller = None, arguments=[]):
		self.server = server
		self.caller = caller
		self.arguments = arguments

	def execute(self):
		"""Overide this method"""
		raise NotImplementedError()

class Help(Command):
	def execute(self):
		import inspect
		import sys
		classes = inspect.getmembers(sys.modules[__name__], inspect.isclass) 
		self.caller.send("Available commands are:")		
		for class_info in classes:
			if issubclass(class_info[1], Command) and class_info[0] != "Command":
				self.caller.send("/"+class_info[0].lower())		

class Exit(Command):
	"""
	Remove the caller from the server socket list and close it's connection.
	arguments:Takes no args
	"""
	def execute(self):
		self.server.disconnect_client(self.caller)

class Rename(Command):
	"""
	Set the name of the caller to the specified argument.
	arguments[0]:The new name for the caller
	"""
	def execute(self):
		if self.arguments[0]:
			self.caller.send("Changing your name from '{0}' to '{1}'\n".format(self.caller.name, self.arguments[0]))
			self.caller.name = self.arguments[0]
		else:
			self.caller.socket.sendall("No name specified =(\n")


class Broadcast(Command):
	"""
	Broadcast a message to all current connected socket of the server.
	arguments[0]:The message to broadcast
	"""
	def execute(self):
		for client in self.server.clients:
			if client.socket != self.caller.socket:
				client.send(self.caller.format(self.arguments[0]))
