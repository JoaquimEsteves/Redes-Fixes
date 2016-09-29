#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
import socket
from protocols import UDP
from utils import Logger
import base64
log = Logger(debug=settings.DEBUG)

TCS_NAME = "tejo" #SET THESE IN MAIN PLZ
TCS_PORT = "12345" #SET THESE IN MAIN PLZ

def _list(args):
	"""Method that handles the list functionality"""
	udp = UDP(args.tcs_name, args.tcs_port)
	response = udp.request("ULQ\n")
	print response

def _request(input_data):
	"""Method that handles the request functionality"""
	try:
		# import pdb;pdb.set_trace()
		input_data = input_data.split()
		language = int(input_data[1])
		type = input_data[2]
		if type == "t":
			_request_text(input_data[2:],language)
		elif type == "f":
			_request_file(input_data[2:],language)
		else:
			raise SyntaxError
	except (SyntaxError, ValueError):
		log.warning("You're probably not using the correct formating, please use:\n request n t W1 W2 ... WN\n or \n request n f filename ")
		pass
	pass

def _find_TCP_server(language):
	"""Find the TCP server I'm going to communicate with for the language given as a parametre"""
	log.info("looking for the TCP server!")
	message_to_TCS = "UNQ " + LANGUAGE_ARRAY[language] + "\n"
	try:
		udp = UDP(TCS_NAME, TCS_PORT)
		TCS_answer = udp.request(message_to_TCS)
		print response
	except:
		log.error("Error with the bloody TCS connection mate!")
	TCS_answer= TCS_answer.split() #TODO
	if not TCS_answer.startswith("UNR"):
		log.error("We got a really weird message back from the TCS server!")
		log.info(TCS_answer)
	elif TCS[1] != LANGUAGE_ARRAY[language]:
		log.error("We seem to be having a problem here, I want to speak in" + LANGUAGE_ARRAY[language] + " but the server understood it as " + TCS[1] + "\n")
	return TCS_answer

def _request_text(input,language):
	"""Requesting a text translation (TCP)"""
	log.info("requesting text!")
	number_of_words = len(input)
	TCS_info = _find_TCP_server(language)
	try:
		TCPtname = TCS_info[2]
		TCPport = TCS_info[3]
		message_to_TRS = "TRQ t "+ number_of_words+" " + " ".join(str(x) for x in input) + "\n"
	except:
		log.error("TCS server sent us a message with the wrong size. BAD TCS!")
	pass
	#SEND MESSAGE WITH TCP

def _request_file(filename,language):
	"""Requesting a file translation! (TCP)"""
	log.info("requesting a file!")
	try:
		file = open(filename)
		#WE'RE GOING TO USE BASE 64 FOR FILE TRANSFER. THIS IS REALLY IMPORTANT PAY ATTENTION!!!!!!!!!!!!!!
		encoded_data = base64.b64encode(file.readlines())
		filesize = len(encoded_data) #in bytes!
		message_to_TCP = "TRQ f " + filename + " " + filesize + " " + encoded_data + "\n"
		#actually send the data through TCP to TCR
	except:
		log.error("Couldn't open the file mate!")


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
			_list(args)
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
