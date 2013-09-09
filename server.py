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
	_server_socket = None
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
	def clients(self):
		return self._clients

	def __init__(self, port=9998, bind="0.0.0.0", parser=None):
		self.port = port
		self.bind = bind
		try:
			self.parser = parsers.getParser(parser)
		except NameError, e:
			print e.message 
			print "Now using default parser"
			self.parser = parsers.getParser("Parser")
	def disconnect_client(self, client):
		self.clients.remove(client)
		client.socket.close()

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
		client = clients.Client(ip=address[0], name=address[0], protocol=protocols.Raw(), socket=socket, server=self)
		self.clients.append(client)
		cmd = commands.Broadcast(self, client, "HERE COMES DADDY!")
		cmd.execute()
	def __handle_request(self, caller):
		"""This is called whenever data is received from one of the client."""
		try:
			data = caller.receive()
			result = self.parser.parse(data)
			cmd = commands.getCommand(result[0], self, caller, result[1])
			try:
				cmd.execute()
			except clients.CouldNotSendRequestError, e:
				#Tell the client that the command could not be executed properly.
				pass
		except clients.SocketError, e:
			self.disconnect_client(caller)
		except clients.ClientIsNotFinishedSendingError, e:
			pass



if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description='kronos-chat server')
	parser.add_argument("--port", metavar="PORT", type=int, help="the port to listen to")
	parser.add_argument("--bind", metavar="IP", type=str, help="the ip to listen on")

	args = parser.parse_args()

	s = Server(parser = "Parser")
	s.listen()
