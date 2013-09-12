def get_parser(parser_name):
	"""
	Try to instantiate a parser from the parser_name
	parser_name: The name of the parser to instantiate.
	throws: NameError, if the parser is not found
	returns: A Parser object.
	"""
	try:
		return globals()[parser_name]()
	except KeyError, e:
		raise NameError("The parser '"+parser_name+"' was not found. Is it properly defined in parsers.py? Is it correctly spelled?")

class Result(object):
	"""
	This object is the result of a parse operation
	"""
	_command_name = ""
	_command_arguments = []

	@property
	def command_name(self):
		return self._command_name
	@command_name.setter
	def command_name(self, value):
		self._command_name = value

	@property
	def command_arguments(self):
		return self._command_arguments
	@command_arguments.setter
	def command_arguments(self, value):
		self._command_arguments = value

	def __init__(self, command_name="", command_arguments=[]):
		self.command_name = command_name
		self.command_arguments = command_arguments
	
class Parser(object):

	_trigger_parse_character = '/'

	@property
	def trigger_parse_character(self):
		return self._trigger_parse_character
	@trigger_parse_character.setter
	def trigger_parse_character(self, value):
		self._trigger_parse_character = value

	def __init__(self, trigger_parse_character = "/"):
		self.trigger_parse_character = trigger_parse_character

	def parse(self, message):
		"""
		Parse a message and return a tuple of the command that should be executed in the module commands and it's arguments.
		message: the message to parse
		returns: (string to pass to commands.get_command; array of arguments)
		"""
		if len(message) == 0 or message[0] != self.trigger_parse_character:
			return Result("Broadcast", [message])
		else:
			parts = message.split(' ')
			return Result(parts[0][1:].title(), parts[1:])



#
# Example of parser.
#
class Standard(Parser):

	def parse(self, message):
		if cmd == "leave":
			return Result("Exit")
		return Result("Broadcast", message)

class Kronos(Parser):

	def parse(self, message):
		parts = message.split(' ')
		if len(parts) != 0:
			if parts[0] == "exit":
				return Result("Exit")
			if parts[0] == "rename" and len(parts) >= 2:
				return Result("Rename", [parts[1]])
		return Result("Broadcast", message)
