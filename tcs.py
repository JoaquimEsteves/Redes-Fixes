#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from protocols import UDP
from utils import Logger
log = Logger(debug=settings.DEBUG)


class TCSHandler(object):
    """Class to wrap all Endpoints for TCS messages."""
    def __init__(self, host=settings.DEFAULT_TCS_NAME, port=settings.DEFAULT_TCS_PORT):
        """inits udp instance (TCS SERVER)"""
        self.UDP = UDP(host, port)

    def dispatch(self, data):
        """this method parses and checks for with feature is the "data" requesting
        this works as a central hub, "switch", where it redirects to the correct
        method. as input is the data from the outside world, output is the
        handled data"""
        # removes \n from string
        data = self.UDP._remove_new_line(data)
        # split data into chunks
        data = data.split(" ")
        # get protocol and rest of the data
        protocol = data[0]
        data = data[1:]
        # dispatch to correct method
        if protocol == "ULQ":
            data = self._ULQ(data)
        elif protocol == "ULR":
            data = self._ULR(data)
        elif protocol == "UNQ":
            data = self._UNQ(data)
        elif protocol == "UNR":
            data = self._UNR(data)
        else:
            data = "ERR"
        # put back the \n
        data += "\n"
        return data

    def _ULQ(self, data):
        """"""
        log.debug("[ULQ] with data=\"{}\"".format(data))
        return ""

    def _ULR(self, data):
        """"""
        log.debug("[ULR] with data=\"{}\"".format(data))
        return ""

    def _UNQ(self, data):
        """"""
        log.debug("[UNQ] with data=\"{}\"".format(data))
        return ""

    def _UNR(self, data):
        """"""
        log.debug("[ULR] with data=\"{}\"".format(data))
        return ""


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
    udp = UDP(settings.DEFAULT_TCS_NAME, args.tcs_port)
    udp.run(handler=TCSHandler())
