#!/usr/bin/python
import os
import sys
import string
import argparse
import server
import json
import ssl
import logging
import logging.config

def parse_configuration_file(kwdefault_args, path):
	class Mock(object):
		def __init__(self, kwdefault_args, kwargs):
			self.__dict__.update(kwdefault_args)
			self.__dict__.update(kwargs)
			
	try:
		json_data = json.load(open(path, "r"))
	except ValueError as e:
		print("There seems to be an error in the configuration file '" + path + "'. Synthax error maybe? Here the exception message: '" + e.message + "'")
		print("Default config shall be used.")
		json_data = {}
	return Mock(kwdefault_args, json_data)

# Arguments and options definition
parser = argparse.ArgumentParser(description="naughty-chat server")
parser.add_argument("--port", default=9999, dest="port", metavar="PORT", type=int, help="the port to listen to")
parser.add_argument("--bind", default="127.0.0.1", dest="bind", metavar="IP", type=str, help="the ip to listen on")
parser.add_argument("--parser", default="Parser", dest="parser", metavar="PARSER", type=str, help="the parser to be used")
parser.add_argument("--encoders", default=["Raw"], dest="encoders", metavar="ENC", type=json.loads, nargs="+", help="a list of encoders that will encode the data in the order it is specified here")
parser.add_argument("--ssl-configuration", default={}, dest="ssl", metavar="SSLCONF", type=json.loads, help="json object representing the ssl configuration i.e. '{\"keyfile\":\"/key/file\", etc.}'")
parser.add_argument("--log", default={}, dest="log", metavar="LOGCONF", type=json.loads, help="json object representing the log configuration look config.sample.json for an example.")
parser.add_argument("--configuration-file", dest="configuration_file", metavar="FILEPATH", type=str, help="path to a json configuration file")

# Parse default configuration
args = parser.parse_args()
if args.configuration_file:
	args = parse_configuration_file(vars(args), args.configuration_file)



# If ssl enabled, parse configuration ssl string value and get the corresponding enum value in the ssl package.
if args.ssl:
	if "cert_reqs" in args.ssl:
		args.ssl["cert_reqs"] = getattr(ssl, args.ssl["cert_reqs"])
	if "ssl_version" in args.ssl:
		args.ssl["ssl_version"] = getattr(ssl, args.ssl["ssl_version"])

# Configure the log.
if args.log:
	logging.config.dictConfig(args.log)
else:
	logging.basicConfig(level=logging.DEBUG)

# Start listenning
s = server.Server(parser=args.parser, port=args.port, bind=args.bind, encoders=args.encoders, ssl_configuration=args.ssl)

try:
	s.listen()
except KeyboardInterrupt as e:
	pass
except Exception as e:
	logging.exception(e)
	print(e)
finally:
	s.stop()

