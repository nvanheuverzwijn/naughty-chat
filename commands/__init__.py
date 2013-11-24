import os
import glob
__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py") if not os.path.basename(f).startswith('_')]

def get_command(command_name, server=None, caller=None, arguments=[]):
	"""
	Try to instantiate a command from the command_name
	command_name: The name of the command to instantiate.
	throws: NameError, if the command is not found
	returns: A Command object.
	"""
	globals_list = globals()
	for module in __all__:
		command = getattr(globals_list[module], command_name, False)
		if command != False:
			return command(server, caller, arguments)
	raise NameError("The command '"+command_name+"' was not found. Is it properly defined in one of the module contained in commands package? Is it correctly spelled?")

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

for module in __all__:
	__import__("commands."+module)
