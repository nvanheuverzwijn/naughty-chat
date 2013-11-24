import socket
import os
import ssl
import select
import sys
import commands
import parsers
import clients
import string
import protocols
import logging

class Server(object):
	"""The chat server. It relays communication between client."""

	_port = 0
	_bind = ""
	_parser = None
	_server_client = None
	_clients = []
	_encoders = []
	_ssl_configuration = {}

	@property
	def port(self):
		return self._port
	@port.setter
	def port(self, value):
		self._port = int(value)

	@property
	def bind(self):
		return self._bind
	@bind.setter
	def bind(self, value):
		self._bind = value
	
	@property
	def parser(self):
		return self._parser
	@parser.setter
	def parser(self, value):
		if isinstance(value, parsers.Parser):
			self._parser = value
		else:
			try:
				self.parser = parsers.get_parser(value)
			except NameError, e:
				raise ValueError("parser value '"+str(value)+"' must be an instance of parsers.Parser or a string allowed by parsers.get_parser.")

	@property
	def server_client(self):
		return self._server_client
	@server_client.setter
	def server_client(self, value):
		self._server_client = value
	
	@property
	def clients(self):
		return self._clients

	@property
	def encoders(self):
		return self._encoders
	@encoders.setter
	def encoders(self, value):
		if not isinstance(value, list):
			value = [value]
		try:
			self._encoders = protocols.get_protocol(value)
		except NameError, e:
			raise ValueError("Could not parse value.", e)

	@property
	def ssl_configuration(self):
		return self._ssl_configuration
	@ssl_configuration.setter
	def ssl_configuration(self, value):
		if not isinstance(value, dict):
			raise ValueError("ssl_configuration must be a dict.")

		self._ssl_configuration = value

	def __init__(self, port=9999, bind="0.0.0.0", parser="Parser", encoders=[], ssl_configuration={}):
		"""
		ssl_configuration: this should be a dictionnary of ssl.wrap_socket function parameters.
		"""
		self.port = port
		self.bind = bind
		self.parser = parser
		self.encoders = encoders
		self.ssl_configuration = ssl_configuration

	def whisp_client(self, message, client):
		cmd = commands.get_command("Whisper",self, self.server_client, [client.name, message])
		cmd.execute()

	def disconnect_client(self, client):
		"""
		Disconnect a client and announce it to the world.
		"""
		self.clients.remove(client)
		client.socket.close()
		cmd = commands.get_command("Broadcast", self, self.server_client, ["{0} has left the chat!".format(client.name), [client.name]])
		cmd.execute()

	def kill(self):
		"""Close all client connection and stop the server to listen WHITOUT warning the current connected clients."""
		for client in self.clients:
			self.disconnect_client(client)
		self.server_client.socket.close()

	def stop(self):
		"""Warns the connected client that the server is going down then close all connection"""
		logging.info("Server stopped")
		cmd = commands.get_command("Broadcast", self, self.server_client, ["I AM GOING DOWN."])
		cmd.execute()
		self.kill()

	def listen(self):
		server_socket = socket.socket(socket.AF_INET)

		if self.ssl_configuration:
			logging.info("SSL mode is on")
			server_socket = ssl.wrap_socket(sock=server_socket, server_side=True, **self.ssl_configuration)

		self.server_client = clients.Client(ip="", name="[SERVER]", protocol=self.encoders, socket=server_socket, server=self) 
		self.server_client.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_client.socket.bind((self.bind, self.port))
		self.server_client.socket.listen(10)

		logging.info( "Listenning started on '" + self.bind + "':'" + str(self.port) + "'")

		while True:
			inputready, outputready, exceptready = select.select(self.clients + [self.server_client],[],[])
			for client in inputready:
				if client == self.server_client:
					try:
						self.__handle_new_connection()
					except socket.error, e:
						logging.log(logging.ERROR, "Error occured while handling a new connection:'" + e.message + "'")
				else:
					self.__handle_request(client)
	def __handle_new_connection(self):
		"""This is called whenever a new connection is initiated"""
		sock, address = self.server_client.socket.accept()
		client = clients.Client(ip=address[0], name=address[0], protocol=self.encoders, socket=sock, server=self)
		self.clients.append(client)
		cmd = commands.get_command("Broadcast", self, self.server_client, ["{0} has joined the chat!".format(client.name), [client.name]])
		cmd.execute()

	def __handle_request(self, caller):
		"""This is called whenever data is received from one of the client."""
		try:
			data = caller.receive()
			logging.debug("Parsing this data: '" + data + "'")
			result = self.parser.parse(data)
			logging.debug("Result of parsing: '" + result.command_name + "(" + ",".join(result.command_arguments) + ")'")
			cmd = commands.get_command(result.command_name, self, caller, result.command_arguments)
			cmd.execute()
		except commands.ArgumentsValidationError, e:
			#Command arguments did not validate.
			cmd = commands.get_command("Whisper", self, self.server_client, [caller.name, e.message])
			cmd.execute()
		except commands.ExecutionFailedError, e:
			#Tell the client that the command could not be executed properly.
			cmd = commands.get_command("Whisper", self, self.server_client, [caller.name, "Command execution failed"])
			cmd.execute()
			logging.exception(e)
		except clients.SocketError, e:
			#Client probably just disconnected.
			logging.debug("SocketError while handling request.")
			logging.exception(e)
			self.disconnect_client(caller)
		except clients.ClientIsNotFinishedSendingError, e:
			#Client has not finished sending it's data.  
			pass
		except NameError, e:
			# The command is not recognized.
			cmd = commands.get_command("Whisper", self, self.server_client, [caller.name, "Unrecognized command"])
			cmd.execute()
