#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
import socket
from protocols import UDP, TCP
from utils import Logger
import base64
log = Logger(debug=settings.DEBUG)


AVAILABLE_LANGUAGES = []


def _list(args):
	"""Method that handles the list functionality"""
	udp = UDP(args.tcs_name, args.tcs_port)
	response = udp.request("ULQ\n")
	# make pretty response
	data = response.split()
	if "ERR" in data:
		log.error("Error: No valid response was returned.")
	else:
		print("Got {} languages:".format(int(data[1]) - 1)) #CAREFUL OF THIS
		for i, lang in enumerate(data[2:], 1):
			AVAILABLE_LANGUAGES.append(lang)
			print("{}. {}".format(i, lang))

def _saveTCPFile(data):
	with open("from_TCP_with_love.png", "w") as my_file: #check to see if the pictures are the same!
			my_file.write(base64.b64decode(data[2]))

def _request(args, input_data):
	"""Method that handles the request functionality"""
	try:
		# split data into variable
		input_data = input_data.split()
		language = int(input_data[1])
		type = input_data[2]
		if type == "t":
			request_msg = __request_text(input_data)
		elif type == "f":
			request_msg = __request_file(input_data)
		else:
			# not valid request type
			raise SyntaxError
	except (IOError, NameError), e:
		log.error("File \"{}\" not found!".format(input_data[3]))
		return
	except (SyntaxError, ValueError, IndexError), e:
		log.error(e.message)
		log.warning("You're probably not using the correct formating, "
					"please use: \"request n t W1 W2 ... WN\" or \"request n f filename\"")
		return
	# get language from tcs server
	translation = __request_translation(args, input_data, request_msg)
	print translation


def __request_file(input_data):
	"""Build request message to request file translation from TRS Server"""
	filename = input_data[3]
	with open(filename, "rb") as image_file:
		encoded_data = base64.b64encode(image_file.read())
			# if we chose not to encode then simply...
		#encoded_data = image_file.read()
	# filesize = len(encoded_data) #in bytes!
	filesize = len(encoded_data)
	return "TRQ f {} {} {}\n".format(filename, filesize, encoded_data)


def __request_text(input_data):
	"""Build request message to request text translation from TRS Server"""
	words = input_data[3:]
	num_words = len(words)
	if num_words == 0:
		raise ValueError("No words were given to be translated.")
	return "TRQ t {} {}\n".format(num_words, " ".join(words))


def __request_translation(args, input_data, request_msg):
	#import pdb; pdb.set_trace()
	"""Return ipaddress an ipport to later connected with TRS server"""
	log.debug("looking for the IP/port connection to TRS Server!")
	udp = UDP(args.tcs_name, args.tcs_port)
	try:
		language = AVAILABLE_LANGUAGES[int(input_data[1]) - 1]
	except IndexError, e:
		log.error("No such language available.")
		return

	response = udp.request("UNQ {}\n".format(language))
	data = response.split()
	# validate response
	if "ERR" in data:
		log.error("Message not well formated!")
		return
	elif "EOF" in data:
		log.error("Invalid language ID")
		return
	trs_ipaddress = data[1]
	trs_ipport = data[2]
	# and request translation
	tcp = TCP(trs_ipaddress, trs_ipport)
	response = tcp.request(request_msg)
	data = response.split()
	#special case...
	if data[1] == 'f':
		log.info("How lovely, the TCP has sent us a file!, let's save it")
		_saveTCPFile(data[2:])
	return trs_ipaddress + ": " + ", ".join(data[3:])


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
	try:
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
				_request(args, input_data)
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
	except KeyboardInterrupt, e:
		# if CTRL+C is pressed, then go for last step
		log.info("\nCTRL+C - Exiting user application.")
		pass

