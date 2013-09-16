import socket
import os
import select
import sys
import commands
import parsers
import clients
import string
import protocols

class Server(object):
	"""The chat server. It relays communication between client."""

	_port = 0
	_bind = ""
	_server_client = None
	_clients = []

	@property
	def port(self):
		return self._port
	@port.setter
	def port(self, value):
		self._port = value

	@property
	def bind(self):
		return self._bind
	@bind.setter
	def bind(self, value):
		self._bind = value
	
	@property
	def server_client(self):
		return self._server_client
	@server_client.setter
	def server_client(self, value):
		self._server_client = value
	
	@property
	def clients(self):
		return self._clients

	def __init__(self, port=9999, bind="0.0.0.0", parser=None):
		self.port = port
		self.bind = bind
		try:
			self.parser = parsers.get_parser(parser)
		except NameError, e:
			print e.message 
			print "Now using default parser"
			self.parser = parsers.get_parser("Parser")
	def disconnect_client(self, client):
		self.clients.remove(client)
		client.socket.close()

	def listen(self):
		self.server_client = clients.Client(ip="", name="[SERVER]", protocol=protocols.Raw(), socket=socket.socket(socket.AF_INET), server=self) 
		self.server_client.socket.bind((self.bind, self.port))
		self.server_client.socket.listen(10)

		while True:
			inputready, outputready, exceptready = select.select(self.clients + [self.server_client],[],[])
			for client in inputready:
				if client == self.server_client:
					self.__handle_new_connection()
				else:
					self.__handle_request(client)
	def __handle_new_connection(self):
		"""This is called whenever a new connection is initiated"""
		socket, address = self.server_client.socket.accept()
		client = clients.Client(ip=address[0], name=address[0], protocol=protocols.Raw(), socket=socket, server=self)
		self.clients.append(client)
		cmd = commands.Broadcast(self, self.server_client, ["{0} has joined the chat!".format(client.ip), [client.name]])
		cmd.execute()
	def __handle_request(self, caller):
		"""This is called whenever data is received from one of the client."""
		try:
			data = caller.receive()
			result = self.parser.parse(data)
			cmd = commands.get_command(result.command_name, self, caller, result.command_arguments)
			cmd.execute()
		except commands.ArgumentsValidationError, e:
			#Command arguments did not validate.
			cmd = commands.Whisper(self, self.server_client, [caller.name, e.message])
			cmd.execute()
		except commands.ExecutionFailedError, e:
			#Tell the client that the command could not be executed properly.
			cmd = commands.Whisper(self, self.server_client, [caller.name, e.message])
			cmd.execute()
		except clients.SocketError, e:
			#Client probably just disconnected.
			self.disconnect_client(caller)
		except clients.ClientIsNotFinishedSendingError, e:
			#Client has not finished sending it's data.  
			pass
		except NameError, e:
			# The command is not recognized.
			cmd = commands.Whisper(self, self.server_client, [caller.name, "Unrecognized command"])
			cmd.execute()



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='kronos-chat server')
	parser.add_argument("--port", metavar="PORT", type=int, help="the port to listen to")
	parser.add_argument("--bind", metavar="IP", type=str, help="the ip to listen on")

	args = parser.parse_args()

	s = Server(parser = "Parser")
	s.listen()
