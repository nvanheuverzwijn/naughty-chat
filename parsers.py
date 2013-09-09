import commands

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
