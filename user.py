#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from utils import Logger
log = Logger(debug=settings.DEBUG)

if __name__ == "__main__":
    log.info("Starting client...")
    # format of command is ./user [-n TCSname] [-p TCSport] so get those arguments and validate them
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', dest='tcs_name', type=str, default=settings.DEFAULT_TCS_NAME,
                        help='Translation Contact Server IP Address.')
    parser.add_argument('-p', dest='tcs_port', type=int, default=settings.DEFAULT_TCS_PORT,
                        help='Translation Contact Server Port Address.')
    args = parser.parse_args()  # validate them
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
            _request()
        elif input_data == 'exit':
            # exit - exit user application
            log.debug("exit - Exiting user application.")
            break
        elif input_data == 'help':
            # help - show list of possible commands
            commands = map(lambda x: '\t> {}'.format(x), [
                'list: Requesting list of possible translations from TCS server.',
                'request: Requesting translation for given arguments.\n\t\t> request n t N W1 W2 … WN\n\t\t> request n f filename',
                'exit: Exit current user application.',
            ])
            log.info("""List of possible commands:\n{}""".format(
                "\n".join(commands)))
        else:
            # validate corner cases
            if input_data.strip() != '':
                log.warning("\"{}\" command does not exist.".format(input_data))



def _list():
    """Method that handles the list functionality"""
    pass


def _request():
    """Method that handles the request functionality"""
    pass
