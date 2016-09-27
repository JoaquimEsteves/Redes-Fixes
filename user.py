#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from utils import Logger
log = Logger(debug=settings.DEBUG)

def _list():
	"""Method that handles the list functionality"""
	pass


def _request(input_data):
	"""Method that handles the request functionality"""
	try:
		input_data = input_data.split()
		language = int(input_data[1])
		type = input_data[2]
		if type == "t":
			_request_text(input_data[2:],language)
		elif type == "f":
			_request_file(input_data[2:],language)
		else: 
			raise 
	except:
		log.warning("You're probably not using the correct formating, please use:\n request n t W1 W2 ... WN\n or \n request n f filename ")
	pass

def _request_text(input,language):
	number_of_words = len(input)
	message_to_TCS = "UNQ " + LANGUAGE_ARRAY[language] + "\n"
	#send2u #TODO
	receivefromu = "" #TODO
	TCS_answer= receivefromu.split() #TODO
	if not TCS_answer.startswith("UNR"):
		log.error("We got a really weird message back from the TCS server!")
		log.info(receivefromu)
	elif TCS[1] != LANGUAGE_ARRAY[language]:
		log.error("We seem to be having a problem here, I want to speak in" + LANGUAGE_ARRAY[language] + " but the server understood it as " + TCS[1] + "\n")
	try:
		TCPtname = TCS[2]
		TCPport = TCS[3]
	except:
		log.error("TCS server sent us a message with the wrong size. BAD TCS!")
	#send2u
	#receivefromu

def _request_file(input,language):
	pass

if __name__ == "__main__":
	log.info("Starting client...")
	# format of command is ./user [-n TCSname] [-p TCSport] so get those arguments and validate them
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', dest='tcs_name', type=str, default=settings.DEFAULT_TCS_NAME,
						help='Translation Contact Server IP Address.')
	parser.add_argument('-p', dest='tcs_port', type=int, default=settings.DEFAULT_TCS_PORT,
						help='Translation Contact Server Port Address.')
	args = parser.parse_args()	# validate them
	# print information just to make sure
	log.debug("Using TCS Name = {}, TCS Port = {}.".format(args.tcs_name, args.tcs_port))
	log.info("Welcome :).")
	# forever & ever (util "exit")
	while(True):
		# waits for client input:
		input_data = raw_input()
		# handle which command should run
		if input_data.startswith('list'):
			# list - chama o ECP com UDP as protocol. pede a lista de topicos
			log.debug("list - Requesting list of possible translations from TCS server.")
			_list()
		elif input_data.startswith('request'):
			# request - request translation for given language
			log.debug("request - Requesting translation for given arguments")
			_request(input_data)
		elif input_data == 'exit':
			# exit - exit user application
			log.debug("exit - Exiting user application.")
			break
		elif input_data == 'help':
			# help - show list of possible commands
			commands = map(lambda x: '\t> {}'.format(x), [
				'list: Requesting list of possible translations from TCS server.',
				'request: Requesting translation for given arguments.\n\t\t> request n t N W1 W2 ... WN\n\t\t> request n f filename',
				'exit: Exit current user application.',
			])
			log.info("""List of possible commands:\n{}""".format(
				"\n".join(commands)))
		else:
			# validate corner cases
			if input_data.strip() != '':
				log.warning("\"{}\" command does not exist.".format(input_data))