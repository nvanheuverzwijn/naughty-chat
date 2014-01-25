from . import Command
from . import ArgumentsValidationError

class Help(Command):
	"""
	Provides the list of executable command.
	"""
	def _execute(self):
		import os
		import glob
		import inspect
		import sys
		self.caller.send("Available commands are:")
		for module in [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py") if not os.path.basename(f).startswith('_')]:
			classes = inspect.getmembers(sys.modules[__package__+"."+module], inspect.isclass) 
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
		elif len(self.arguments[0]) == 0:
			raise ArgumentsValidationError("The first argument cannot be empty")
		else:
			for client in self.server.clients:
				if self.arguments[0] == client.name and client != self.caller:
					raise ArgumentsValidationError("The name '{0}' is already used.".format(self.arguments[0]))

	def _execute(self):
		self.server.whisp_client("Changing your name from '{0}' to '{1}'".format(self.caller.name, self.arguments[0]), self.caller)
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
			if client.socket != self.caller.socket and client.name not in self.arguments[1]:
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
