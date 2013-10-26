naughty-chat
============

Simple chat in python 2.7.5.

Usage
=====
<pre>
usage: start.py [-h] [--port PORT] [--bind IP] [--parser PARSER]
                [--encoders ENC [ENC ...]] [--ssl-configuration SSLCONF]
                [--configuration-file FILEPATH]

naughty-chat server

optional arguments:
  -h, --help            show this help message and exit
  --port PORT           the port to listen to
  --bind IP             the ip to listen on
  --parser PARSER       the parser to be used
  --encoders ENC [ENC ...]
                        a list of encoders that will encode the data in the
                        order it is specified here
  --ssl-configuration SSLCONF
                        json object representing the ssl configuration i.e.
                        '{"keyfile":"/key/file", etc..}'
  --configuration-file FILEPATH
                        path to a json configuration file
</pre>
To start the server with default value: `./start.py`.

To start the server with a configuration file: `.start.py --configuration-file config.json`.

Use netcat to connect `nc 127.0.0.1 9999`.
When in chat, type `/help` to see available command.

SSL
===

SSL is supported. Check the `config.sample.json` to see available options.

These options are mainly based on the <a href="http://www.openssl.org/docs/apps/ciphers.html">ssl documentation</a>

Option describe below must be string name of the enumeration and not the integer representing the actual value. 
For example, the `cert_reqs` option should be `CERT_NONE` and not 0 (which is the value associated with `CERT_NONE` in the python enumeration).

Check the <a href="http://www.openssl.org/docs/apps/ciphers.html#CIPHER_STRINGS">cipher strings documentation</a> for valid value for the `cipher` option.

Check the python ssl <a href="http://docs.python.org/2/library/ssl.html#ssl.PROTOCOL_SSLv2">protocol documentation</a> for valid value for the `ssl_version` option.

Check the python ssl <a href="http://docs.python.org/2/library/ssl.html#ssl.CERT_NONE">certificate validation documentation</a> for valid value for the `cert_reqs` option.

How it works
============
The server listen for connection. Once a client is connected, a new `clients.Client` is instanciated. 
Any data that is sent from the client is passed through the protocol, which returns one string. 
That string is then crunched by the parser that returns metadata about what command should be executed. 
These metadata are then converted by the server into and executable command.

The workflow is as follow:

`client` sends `(protocol-wrapped-message)` to `server` sends `(protocol-wrapped-message)` to `protocol` sends `(message)` to `parser` which analyse `(message)` and sends `(metadata)` to `server` which instantiate and execute `command` depending on what the metadata is.

Protocols or Encoders
=====================
protocols.py contains protocols that a client speak. Protocol is where the message form is controlled.

Parsers
=======
parsers.py contains the parser of data that the protocol returns and return metadata about what command should be executed.

Commands
========
commands.py contains commands that clients can execute. There commands are executed by the server with the help of the parser metadata.

Configuration file sample
=========================
Basic server configuration file
<pre>
{
  "bind":"127.0.0.1",
  "encoders":["Raw"],
  "parser":"Parser",
  "port":"9999"
}
</pre>

Server with ssl support
<pre>
{
  "bind":"127.0.0.1",
  "encoders":["Raw"],
  "parser":"Parser",
  "port":"9999",
  "ssl":
  {
    "keyfile":"certificate/server.key",
    "certfile":"certificate/server.crt",
    "cert_reqs":"CERT_OPTIONAL",
    "ssl_version":"PROTOCOL_SSLv23",
    "ca_certs":"/etc/ssl/certs/ca-certificates.crt",
    "ciphers":"ALL"
  }
}
</pre>

Basic Server with multiple encoders
<pre>
{
  "bind":"127.0.0.1",
  "encoders":["Raw", "BaseSixtyFour"],
  "parser":"Parser",
  "port":"9999"
}
</pre>

