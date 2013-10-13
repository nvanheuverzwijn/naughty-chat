#!/usr/bin/python
import os
import sys
import string
import argparse
import server
import json

def parse_configuration_file(path):
	class Mock(object):
		def __init__(self, kwargs):
			self.__dict__.update(kwargs)
			
	json_data = json.load(open(path, "r"))
	return Mock(json_data)

parser = argparse.ArgumentParser(description="naughty-chat server")
parser.add_argument("--port", default=9999, dest="port", metavar="PORT", type=int, help="the port to listen to")
parser.add_argument("--bind", default="127.0.0.1", dest="bind", metavar="IP", type=str, help="the ip to listen on")
parser.add_argument("--parser", default="Parser", dest="parser", metavar="PARSER", type=str, help="the parser to be used")
parser.add_argument("--encoders", default=["Raw"], dest="encoders", metavar="ENC", type=str, nargs="+", help="a list of encoders that will encode the data in the order it is specified here")
parser.add_argument("--configuration-file", dest="configuration_file", metavar="FILEPATH", type=str, help="path to a json configuration file")

args = parser.parse_args()
if args.configuration_file:
	args = parse_configuration_file(args.configuration_file)

s = server.Server(parser=args.parser, port=args.port, bind=args.bind, encoders=args.encoders)
try:
	s.listen()
except (KeyboardInterrupt, Exception) as e:
	print e
finally:
	s.stop()

