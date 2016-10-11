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
	def __init__(self, language, host=settings.DEFAULT_TRS_NAME, port=settings.DEFAULT_TRS_PORT):
		"""inits udp instance (TRS SERVER)"""
		self.TCP = TCP(host, port)
		self.language = language

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
		if protocol == "TRQ":
			data = self._TRQ(data)
		else:
			data = "ERR"
		# put back the \n
		data += "\n"
		return data

	def _TRQ(self,data):
		"""Translation request!"""
		ttype = data[0]
		if ttype == "t":
			return self._TRQtext(data[1:])
		elif ttype == "f":
			return self._TRQfile(data[1:])

		log.error("Got neither t nor an f from the input!")
		return "TRR ERR"

	def _TRQtext(self, data):
		# data = [<num_words>, <words>]"
		def _translate(word):
			"""go to this TRS translation file and search for the given word translation"""
			translate_file = settings.TRANSLATE_DB_FILENAME.format(self.language)
			with open(translate_file, "r") as f:
				for row in f.readlines():
					source_word, target_word = row.rstrip().split("\t")
					if word == source_word:
						return target_word
			return None
		num_words = data[0]
		words = data[1:]
		# validations of input
		try:
			num_words = int(num_words)
		except ValueError, e:
			log.error("Number of words is not an integer!")
			return "TRR ERR"
		if num_words != len(words):
			log.error("Number of words doesn't match with the amount of words given!")
			return "TRR ERR"
		if num_words > settings.TRANSLATE_MAX_LIMIT:
			log.error("Only translate {} words per request!".format(settings.TRANSLATE_MAX_LIMIT))
			return "TRR ERR"

		# translate words
		trans_words = list()
		for w in words:
			tw = _translate(w)
			if tw is None:
				return "TRR NTA"
			trans_words.append(tw)

		if num_words != len(trans_words):
			log.error("This should never happen but ohwell")
			return "TRR ERR"
		return "TRR t {} {}".format(len(trans_words), " ".join(trans_words))


	def _TRQfile(self, data):
		"""Request file translation"""
		filename = data[0]
		filesize = data[1]
		encoded_data = data[2]
		if len(encoded_data) != int(filesize):
			log.error("File seems to be missing a few bytes!")
			return "TRR ERR"

		filename = ".".join(filename.split(".")[:-1]) + "_translated.png"
		with open(filename, "rb") as image_file:
			send_data = base64.b64encode(image_file.read())
			new_filesize = len(encoded_data) #in bytes!
		return "TRQ f {} {} {}".format(filename, new_filesize, send_data)


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
	if response == "SRR OK":
		log.error("TCS Server register TRS Server \"{}\" successfully.".format(args.language))
	elif response == "SRR NOK":
		log.error("TCS Server was not able to register TRS Server \"{}\". Already register.".format(args.language))
		log.info("Exiting TRS Server...")
		sys.exit()
	else:
		log.error("TCS Response not valid. Res: \"{}\"".format(response))
		log.info("Exiting TRS Server...")
		sys.exit()

	# 2º - keep TCP server running
	try:
		# keep TRS waiting for any incoming requests
		tcp.run(handler=TRSHandler(args.language, settings.DEFAULT_TRS_NAME, args.trs_port))
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		log.info("Exiting TRS Server... {}".format(e))
	except SocketError, e:
		# if error is from "Address already in use", just go for last step
		log.info("Exiting TRS Server... {}".format(e))

	# 3º - when quiting connection, unregister this server from TCS database
	response = udp.request("SUN {} {} {}\n".format(args.language, settings.DEFAULT_TRS_NAME, args.trs_port))
	if response == "SUR OK":
		log.error("TCS Server unregister TRS Server \"{}\" successfully.".format(args.language))
	elif response == "SUR NOK":
		log.error("TCS Server was not able to unregister TRS Server \"{}\".".format(args.language))
		log.info("Exiting TRS Server...")
		sys.exit()
	else:
		log.error("TCS Response not valid. Res: \"{}\"".format(response))
		log.info("Exiting TRS Server...")
		sys.exit()
