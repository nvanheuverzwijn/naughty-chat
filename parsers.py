import commands

def getParser(parser_name):
	"""
	Try to instantiate the a parser from the parser_name
	parser_name: The name of the parser to instantiate.
	throws: NameError, if the parser is not found
	returns: A Parser object.
	"""
	try:
		return globals()[parser_name]()
	except KeyError, e:
		raise NameError("The parser '"+parser_name+"' was not found. Is it properly defined in parsers.py? Is it correctly spelled?")

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
		if message[0] != self.trigger_parse_character:
			return None 

		parts = message.split(' ')
		try:
			# get the class from commands, titleize it (class becomes Class) and instantiate it
			return getattr(commands, parts[0][1:].title())()  
		except AttributeError, e:
			return None


#
# Example of parser.
#
class Standard(Parser):

	def parse(self, message):
		if cmd == "leave":
			return commands.Exit()
		return None

class Kronos(Parser):

	def parse(self, message):
		parts = message.split(' ')
		if parts[0] == "exit":
			return commands.Exit()
		if parts[0] == "rename":
			return commands.Rename()
		return None
