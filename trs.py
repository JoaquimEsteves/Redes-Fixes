#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from socket import error as SocketError
from protocols import UDP, TCP
from utils import Logger
import base64
log = Logger(debug=settings.DEBUG)


class TRSHandler(object):
	"""Class to wrap all Endpoints for TRS messages."""
	def __init__(self, host=settings.DEFAULT_TRS_NAME, port=settings.DEFAULT_TRS_PORT):
		"""inits udp instance (TRS SERVER)"""
		self.TCP = TCP(host, port)

	def dispatch(self, data):
		"""this method parses and checks for with feature is the "data" requesting
		this works as a central hub, "switch", where it redirects to the correct
		method. as input is the data from the outside world, output is the
		handled data"""
		# removes \n from string
		data = self.TCP._remove_new_line(data)
		# split data into chunks
		data = data.split(" ")
		# get protocol and rest of the data
		protocol = data[0]
		data = data[1:]
		# dispatch to correct method
		if protocol == "ULQ":
			data = self._ULQ(data)
		if protocol == "TRQ":
			data = self._TRQ(data)
		else:
			data = "ERR"
		# put back the \n
		data += "\n"
		return data

	def _ULQ(self, data):
		""""""
		log.debug("[ULQ] with data=\"{}\"".format(data))
		return "ULR 2 Ingles Frances\n"
	def _TRQ(self,data):
		"""Translation request!"""
		type = data[0]
		if type == "t":
			return _TRQtext(data[1:])
		if type == "f":
			return _TRQfile(data[1:])
		else:
			log.error("Got neither t nor an f from the input!")
			return "ERR"
	
	def _TRQtext(data):
		pass
	def _TRQfile(data):
		filesize = data[1]
		encoded_data = data[2]
		if len(encoded_data) != filesize:
			log.error("Our file seems to be missing a few bytes!")
			return "ERR"
		with open("Output.png", "w") as my_file: #check to see if the pictures are the same!
			my_file.write(base64.b64decode(encoded_data))
		#well then, now that everything is in order!
		filename = "pyrion.PNG" #just an example...
		with open("pyrion.PNG", "rb") as image_file:
			send_data = base64.b64encode(image_file.read())
			new_filesize = len(encoded_data) #in bytes!
		return "TRQ f {} {} {}\n".format(filename, new_filesize, send_data)
		
		
if __name__ == "__main__":
	log.info("Starting TRS server...")
	# format of command is ./trs language [-p TRSport] [-n TCSname] [-e TCSport],
	parser = argparse.ArgumentParser()
	parser.add_argument('language', help='Language of translations.')
	parser.add_argument('-p', dest='trs_port', type=int, default=settings.DEFAULT_TRS_PORT,
						help='Translation Server Port Address.')
	parser.add_argument('-n', dest='tcs_name', type=str, default=settings.DEFAULT_TCS_NAME,
						help='Translation Contact Server IP Address.')
	parser.add_argument('-e', dest='tcs_port', type=int, default=settings.DEFAULT_TCS_PORT,
						help='Translation Contact Server Port Address.')
	args = parser.parse_args()	# validate them
	# print information just to make sure
	log.debug("Using Language = {}, TRS Port = {}, TCS Name = {}, TCS Port = {}.".format(
		args.language, args.trs_port, args.tcs_name, args.tcs_port))

	# for steps 1º and 3º we need an UDP connection
	udp = UDP(args.tcs_name, args.tcs_port)
	# for 2º step, we need a TCP connection
	tcp = TCP(settings.DEFAULT_TRS_NAME, args.trs_port)
	# 1º - register this server into TCS database
	response = udp.request("SRG {} {} {}\n".format(args.language, settings.DEFAULT_TRS_NAME, args.trs_port))
	if not response.startswith("SRR"):
		log.error("SRR ERR")
		log.info("Message from the TCR doesn't start with SRR!")
		raise SyntaxError
	response.split()
	if response[1] == "OK":
		log.error("THE TCS SERVER ACCEPTED MY GREETING!")
	elif response[1] == "NOK":
		log.error("THE TCS SERVER REFUSED MY GREETINGS! MAYBE TRY AGAIN LATER")

	# 2º - keep TCP server running
	try:
		# keep TRS waiting for any incoming requests
		tcp.run(handler=TRSHandler(settings.DEFAULT_TRS_NAME, args.trs_port))
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		log.info("Exiting TRS Server...")
		pass
	except SocketError, e:
		# if error is from "Address already in use", just go for last step
		pass

	# 3º - when quiting connection, unregister this server from TCS database
	response = udp.request("SUN {} {} {}\n".format(args.language, settings.DEFAULT_TRS_NAME, args.trs_port))
	if not response.startswith("SUR"):
		log.error("SUR ERR")
		log.info("Message from the TCR doesn't start with SUR!")
		raise SyntaxError
	response.split()
	if response[1] == "OK":
		log.error("THE TCS SERVER ACCEPTED MY RETIREMENT!")
	elif response[1] == "NOK":
		log.error("THE TCS SERVER REFUSED MY RETIREMENT! MAYBE TRY AGAIN LATER")
