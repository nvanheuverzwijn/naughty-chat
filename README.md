naughty-chat
============

Simple chat in python 2.7.5.

Usage
=====

Copy the configuration file `config.sample.json` to `config.json` and modify it to fit your need.
Start the server with `./start.py`.
Use netcat to connect to it with `nc 127.0.0.1 9999`.
When in chat, type `/help` to see available command.

How it works
============
The server listen for connection. Once a client is connected, a new `clients.Client` is instanciated. 
Any data that is sent from the client is passed through the protocol, which returns one string. 
That string is then crunched by the parser that returns metadata about what command should be executed. 
These metadata are then converted by the server into and executable command.

The workflow is as follow:

`client` sends `(protocol-wrapped-message)` to `server` sends `(protocol-wrapped-message)` to `protocol` sends `(message)` to `parser` which analyse `(message)` and sends `(metadata)` to `server` which instantiate and execute `command` depending on what the metadata is.

Protocols
=========
protocols.py contains protocols that a client speak. Protocol is where the message form is controlled.

Parsers
=======
parsers.py contains the parser of data that the protocol returns and return metadata about what command should be executed.

Commands
========
commands.py contains commands that clients can execute. There commands are executed by the server with the help of the parser metadata.

