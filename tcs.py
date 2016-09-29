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
        elif protocol == "UNQ":
            data = self._UNQ(data)
        elif protocol == "SRG":
            data = self._SRG(data)
        elif protocol == "SUN":
            data = self._SUN(data)
        else:
            data = "ERR"
        # put back the \n
        data += "\n"
        return data

    def _ULQ(self, data):
        """"""
        log.debug("[ULQ] with data=\"{}\"".format(data))
        return "ULR 2 Ingles Frances"

    def _UNQ(self, data):
        """"""
        log.debug("[UNQ] with data=\"{}\"".format(data))
        return "UNR IPaddress Port"

    def _SRG(self, data):
        """Register incoming request from TRS server to local database"""
        log.debug("[SRG] with data=\"{}\"".format(data))
        try:
            # get configuration of incoming TRS request
            language, ipaddress, ipport = data[:]
            # TODO: Validate arguments:
            #       - check if there are only 3 arguments
            #       - check if the three arguments make any sense (check if is valid IP ad Port)
            # save configurations into "db"
            with open(settings.DB_PATH, 'a') as db:
                db.write("{}\n".format("\t".join([language, ipaddress, ipport])))
            status = "OK"
        except Exception, e:
            log.error(e.message)
            status = "NOK"
        return "SRR {}".format(status)

    def _SUN(self, data):
        """Unregister incoming TRS server from local database"""
        log.debug("[SUN] with data=\"{}\"".format(data))
        try:
            # get configuration of incoming TRS request
            language, ipaddress, ipport = data[:]
            # TODO: Validate arguments:
            #       - check if there are only 3 arguments
            #       - check if the three arguments make any sense (check if is valid IP ad Port)
            # get all configurations from "db"
            with open(settings.DB_PATH, 'r') as db:
                db = db.readlines()
            # remove TRS config from db
            updated_db = list()
            for row in db:
                # clean row and slice it into array
                row = row.rstrip().split("\t")
                # check if current row is the one I want to delete
                if row[0] == language and row[1] == ipaddress and row[2] == ipport:
                    continue
                # if not, then just append it to "updated db" array
                updated_db.append(row)

            with open(settings.DB_PATH, 'w') as db:
                for row in updated_db:
                    db.write("{}\n".format("\t".join(row)))

            status = "OK"
        except Exception, e:
            log.error(e.message)
            status = "NOK"
        return "SUR {}".format(status)

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
