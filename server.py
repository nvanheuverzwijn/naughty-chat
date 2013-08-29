import socket
import os
import select
import sys
import commands
import parsers
import clients
import string

class Server(object):
	"""The chat server. It relays communication between client."""

	_port = 0
	_bind = ""
	_server_socket = None
	_buffer_size = 0
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
	def server_socket(self):
		return self._server_socket

	@property
	def buffer_size(self):
		return self._buffer_size
	@buffer_size.setter
	def buffer_size(self, value):
		self._buffer_size = value
	
	@property
	def clients(self):
		return self._clients

	def __init__(self, port=9999, bind="0.0.0.0", buffer_size=4096, parser=None):
		self.port = port
		self.bind = bind
		self.buffer_size = buffer_size
		if parser is not None:
			try:
				klass = getattr(parsers, parser)
				self.parser = klass()
			except AttributeError, e:
				print "Could not instantiate '" + parser + "'. Are you sure it's declared properly in parsers.py?"
	def listen(self):
		self._server_socket = socket.socket(socket.AF_INET) 
		self._server_socket.bind((self.bind, self.port))
		self._server_socket.listen(10)

		while True:
			inputready, outputready, exceptready = select.select(self.clients + [self.server_socket],[],[])
			for sock in inputready:
				if sock == self.server_socket:
					self.__handle_new_connection()
				else:
					self.__handle_request(sock)
	def __handle_new_connection(self):
		"""This is called whenever a new connection is initiated"""
		socket, address = self.server_socket.accept()
		client = clients.Client(ip=address[0], name=address[0], protocol="RAW", socket=socket)
		self.clients.append(client)
		cmd = commands.Broadcast(self, client, "HERE COMES DADDY!\n".format(address[0]))
		cmd.execute()
	def __handle_request(self, caller):
		"""This is called whenever data is received from one of the client."""
		data = caller.socket.recv(self.buffer_size).strip("\n")
		if data:
			cmd = self.parser.parse(data)
			if not isinstance(cmd, commands.Command):
				cmd = commands.Broadcast(self, caller, data)
			else:
				cmd.server = self
				cmd.caller = caller
				cmd.arguments = data.split(' ')[1:]
			cmd.execute()



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='kronos-chat server')
	parser.add_argument("--port", metavar="PORT", type=int, help="the port to listen to")
	parser.add_argument("--bind", metavar="IP", type=str, help="the ip to listen on")

	args = parser.parse_args()

	s = Server(parser = "Parser")
	s.listen()
