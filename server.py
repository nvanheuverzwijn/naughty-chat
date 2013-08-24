import socket
import os
import select
import sys
import commands
import parsers
import string

class Server(object):
	"""The chat server. It relays communication between client."""

	_port = 9999
	_bind = "0.0.0.0"
	_server_socket = None
	_socket_list = []
	_buffer_size = 4096

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
	def socket_list(self):
		return self._socket_list

	@property
	def buffer_size(self):
		return self._buffer_size
	@buffer_size.setter
	def buffer_size(self, value):
		self._buffer_size = value

	def __init__(self, port=9999, bind="0.0.0.0", buffer_size=4096, parser=None):
		self.port = port
		self.bind = bind
		self.buffer_size = buffer_size
		if parser is not None:
			klass = getattr(parsers, parser)
			if klass is not None:
				self.parser = klass()
	
	def listen(self):
		self._server_socket = socket.socket(socket.AF_INET) 
		self._server_socket.bind((self.bind, self.port))
		self._server_socket.listen(10)
		self._socket_list = [self._server_socket]
		while True:
			inputready, outputready, exceptready = select.select(self.socket_list,[],[])
			for sock in inputready:
				if sock == self.server_socket:
					self.__handle_new_connection()
				else:
					self.__handle_request(sock)
	def __handle_new_connection(self):
		client, address = self.server_socket.accept()
		self.socket_list.append(client)
		cmd = commands.Broadcast(self, client, "[%s:%s] entered room\n" % address)
		cmd.execute()
	def __handle_request(self, caller):
		data = caller.recv(self.buffer_size)
		if data:
			cmd = self.parser.parse(data)
			if not isinstance(cmd, commands.Command):
				cmd = commands.Broadcast(self, caller, data)
			else:
				cmd.server = self
				cmd.caller = caller
				cmd.arguments = string.split(data, " ")
			cmd.execute()



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='kronos-chat server')
	parser.add_argument("--port", metavar="PORT", type=int, help='the port to listen to')
	parser.add_argument('--bind', metavar="IP", type=str, help='the ip to listen on')

	args = parser.parse_args()

	s = Server(parser = "Standard")
	s.listen()
