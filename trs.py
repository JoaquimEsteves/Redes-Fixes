#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from utils import Logger
log = Logger(debug=settings.DEBUG)

# SRG
# language
# IPTRS portTRS

class TRSHandler(object):
    """Class to wrap all functionality of TRS 'servers' """
    def __init__(self, host=settings.DEFAULT_TRS_NAME, port=settings.DEFAULT_TRS_PORT, language):
        """inits udp instance (TCS SERVER)"""
		self._IPTRS = host;
		self._portTRS = port;
        #self.UDP = UDP(host, port)
		self._language = language
		#init TCP object here too!
		self._SRG = False

	def introduce_myself(self, host=settings.DEFAULT_TCS_NAME, port=settings.DEFAULT_TCS_NAME):
		"""Time to make myself known to the TCS!"""
		message_to_send = "SRG " + self._language + " " + self._IPTRS + " " + self._portTRS + "\n"
		try:
			udp = UDP(host,port) #Create this in init?
			response = udp.request(message_to_send)
			if not response.startswith("SRR"):
				log.error("SRR ERR")
				log.info("Message from the TCR doesn't start with SRR!")
				raise SyntaxError
			response.split()
			if response[1] == "OK"
				self._SRG = True
			elif response[1] == "NOK"
				log.error("THE TCS SERVER REFUSED MY GREETINGS! MAYBE TRY AGAIN LATER")

	def retire(self, host=settings.DEFAULT_TCS_NAME, port = settings.DEFAULT_TCS_PORT):
		"""Inform the TCS server I don't really have it in me anymore"""
		message_to_send = "SUN " + self._language + " " + self._IPTRS + " " + self._portTRS + "\n"
		try:
			udp = UDP(host,port) #Create this in init?
			response = udp.request(message_to_send)
			if not response.startswith("SUR"):
				log.error("SUR ERR")
				log.info("Message from the TCR doesn't start with SUR!")
				raise SyntaxError
			response.split()
			if response[1] == "OK"
				self._SRG = False
			elif response[1] == "NOK"
				log.error("THE TCS SERVER REFUSED MY RETIREMENT! MAYBE TRY AGAIN LATER")
	def respond_to_users(self):
		if self._SRG:
            pass
		else:
            log.error("Attemped to respond to users when I have no connection to the TCS")


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
    args = parser.parse_args()  # validate them
    # print information just to make sure
    log.debug("Using Language = {}, TRS Port = {}, TCS Name = {}, TCS Port = {}.".format(
        args.language, args.trs_port, args.tcs_name, args.tcs_port))

    # running server
    tcp = TCP(settings.DEFAULT_TRS_NAME, args.trs_port)
    tcp.run(handler=TRSHandler())
