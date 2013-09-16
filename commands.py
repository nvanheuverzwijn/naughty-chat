def get_command(command_name, server=None, caller=None, arguments=[]):
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

class ExecutionFailedError(Exception):
	"""
	Happens whenever a command raises an unhandled exception.
	"""
	pass
class ArgumentsValidationError(Exception):
	"""
	Happens whenever arguments passed to the command are wrong.
	"""
	pass

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
		self._validate()
		try:
			self._execute()
		except Exception, e:
			raise ExecutionFailedError("Execution failed", e)

	def _execute(self):
		"""Overide this method"""
		raise NotImplementedError()
	def _validate(self):
		"""Here, you get a chance to validate arguments"""
		pass

class Help(Command):
	"""
	Provides the list of executable command.
	"""
	def _execute(self):
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
	def _execute(self):
		self.server.disconnect_client(self.caller)

class Rename(Command):
	"""
	Set the name of the caller to the specified argument.
	arguments[0]:The new name for the caller
	"""
	def _validate(self):
		if len(self.arguments) != 1:
			raise ArgumentsValidationError("The new name needs to be passed as the first argument.")
	def _execute(self):
		self.caller.send("Changing your name from '{0}' to '{1}'\n".format(self.caller.name, self.arguments[0]))
		self.caller.name = self.arguments[0]


class Broadcast(Command):
	"""
	Broadcast a message to all current connected socket of the server.
	arguments[0]:The message to broadcast
	arguments[1]:An array of client name to not broadcast to.
	"""
	def _validate(self):
		if len(self.arguments) == 0 or len(self.arguments) >=3:
			raise ArgumentsValidationError("Wrong number of arguments. Only one or two arguments expected. First is the message to broadcast, the second is a list of client name to ignore.")

	def _execute(self):
		if len(self.arguments) == 1:
			self.arguments.append([])
		for client in self.server.clients:
			print client.name
			print self.arguments
			if client.socket != self.caller.socket and client.name not in self.arguments[1]:
				print client.name
				client.send(self.caller.format(self.arguments[0]))

class Whisper(Command):
	"""
	Whisp to a client.
	arguments[0]:Name of the client
	arguments[1]:Message to send.
	"""
	def _validate(self):
		if len(self.arguments) != 2:
			raise ArgumentsValidationError("First argument must be the name of a client, second must be the message.")
	def _execute(self):
		for client in self.server.clients:
			if client.name == self.arguments[0]:
				client.send(self.caller.format(self.arguments[1]))
