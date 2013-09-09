naughty-chat
===========

Simple chat in python

Usage
=====

Start the server with `python server.py`.
Use netcat to connect to it with `nc 127.0.0.1 9999`.

How it works
============
The server listen for connection. Once a client is connected, a new `clients.Client` is instanciated. 
Any data that is sent from the client is passed through the protocol, which returns one string. 
That string is then crunched by the parser that returns metadata about what command should be executed. 
These metadata are then converted by the server into and executable command.

A little graphice:

`client>==>(encoded-message)>==>server>==>protocol>==>decoded-message>==>parser>==>command-metadata>==>server-executing-command`

Protocols
=========
protocols.py contains protocols that a client speak. Protocol is where the message form is controlled.

Parsers
=======
parsers.py contains the parser of data that the protocol returns and return metadata about what command should be executed.

Commands
========
commands.py contains commands that clients can execute. There commands are executed by the server with the help of the parser metadata.

