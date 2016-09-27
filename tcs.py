#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from utils import Logger
log = Logger(debug=settings.DEBUG)

if __name__ == "__main__":
    log.info("Starting TCS server...")
    # format of command is ./tcs [-p TCSport],
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='tcs_port', type=int, default=settings.DEFAULT_TCS_PORT,
                        help='Translation Contact Server Port Address.')
    args = parser.parse_args()  # validate them
    # print information just to make sure
    log.debug("Using TCS Port = {}.".format(args.tcs_port))

    # running server
    # tcp = TCP(settings.DEFAULT_TESname, TESport)
    # tcp.run(handle_data=TESProtocols(ECPname, ECPport))
