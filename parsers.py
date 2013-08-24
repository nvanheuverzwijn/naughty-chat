import commands

class Parser(object):
	def parse(self, message):
		pass

class Standard(Parser):
	def parse(self, message):
		cmd = message.strip("\n")
		if cmd == "leave":
			return commands.Exit()
		return None

class Kronos(Parser):

	def parse(self, message):
		cmd = message.strip("\n")
		if cmd == "exit":
			return commands.Exit()
		return None
