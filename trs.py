#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from utils import Logger
log = Logger(debug=settings.DEBUG)

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
    log.debug("Using Language = {}, TRS Port = {}, TCS Name = {}, TCS Port = {}.".format(args.language, args.trs_port, args.tcs_name, args.tcs_port))
