#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import settings
import argparse
from socket import inet_aton, error as SocketError
from protocols import UDP
from utils import Logger
log = Logger(debug=settings.DEBUG)

class DBWrapper(object):
    """Fake db manipulation. Collection of methods that manipulate
    the settings.DB_PATH txt file"""

    def __init__(self, db_path=settings.DB_PATH):
        """Set basic variables"""
        self.db_path = db_path
        # make sure file is only created when needed.
        self.close()
        # make sure file exist
        with open(settings.DB_PATH, 'w+') as db:
            db.write("")

    def close(self):
        """Remove self.db_path local file"""
        if os.path.isfile(self.db_path):
            os.remove(self.db_path)

    def get_rows(self):
        """Return list of rows from db_path "database" """
        with open(self.db_path, 'r+') as db:
            db = db.readlines()
        # clean row and slice it into array
        db = [row.rstrip().split("\t") for row in db]
        return db

    def get_row(self, language):
        """Return row for given language. Raise Exception if language is not found"""
        for row in self.get_rows():
            # get correct row
            if language == row[0]:
                return row
        raise Exception("Language \"{}\" not found in local db".format(language))

    def has_language(self, language):
        """Check if given language already exists in "database" """
        rows = self.get_rows()
        languages = map(lambda x: x[0], rows)
        return language in languages

    def add_trs_server(self, language=None, ipaddress=None, ipport=None):
        """adds line into db_path file. line contains given arguments separated by
        \t, with a \n in the end.
        Raises Exception if there are any missing arguments or invalid arguments"""
        # all arguments are required
        if language is None and ipaddress is None and ipport is None:
            raise Exception("All three arguments are required!")
        # check if language string is valid
        if len(language) > settings.DB_LANGUAGE_MAX_CHARS:
            raise Exception("Language \"{}\" is not valid! Max {} chars".format(
                language, settings.DB_LANGUAGE_MAX_CHARS))
        # check if ipaddress is in correct format
        try:
            # valid
            if ipaddress == 'localhost':
                ipaddress = '127.0.0.1'
            inet_aton(ipaddress)
        except SocketError, e:
            # invalid
            raise Exception("IpAddress \"{}\" is not valid!".format(ipaddress))
        # check if ipport is in correct format
        try:
            # check if can be converted into integer
            ipport = int(ipport)
        except Exception, e:
            raise Exception("IpPort \"{}\" is not valid!".format(ipport))
        if ipport > 65535 or ipport < 0:
            raise Exception("IpPort \"{}\" doesn't have a valid range!".format(ipport))
        # append line into file
        with open(self.db_path, 'a') as db:
            line = "\t".join(map(str, [language, ipaddress, ipport]))
            db.write(line + "\n")

    def remove_trs_server(self, language=None, ipaddress=None, ipport=None):
        """remove line from db_path file. if no line is found, nothing happens"""
        # read all db to memory (list)
        rows = self.get_rows()
        updated_db = list()
        for row in rows:
            # check if current row is the one I want to delete
            if row[0] == language:
                continue
            # if not, then just append it to "updated db" array
            updated_db.append(row)

        with open(settings.DB_PATH, 'w') as db:
            for row in updated_db:
                db.write("{}\n".format("\t".join(row)))


class TCSHandler(object):
    """Class to wrap all Endpoints for TCS messages."""
    def __init__(self, host=settings.DEFAULT_TCS_NAME, port=settings.DEFAULT_TCS_PORT):
        """inits udp instance (TCS SERVER)"""
        self.UDP = UDP(host, port)
        self.DB = DBWrapper()

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
        """Return information from database"""
        log.debug("[ULQ] with data=\"{}\"".format(data))
        rows = self.DB.get_rows()
        languages = map(lambda x: x[0], rows)
        num_languages = len(rows)
        if num_languages == 0:
            # no languages (TRS Servers) available
            return "ULR EOF"
        return "ULR {} {}".format(num_languages, " ".join(languages)).strip()

    def _UNQ(self, data):
        """Get IpAddress and IpPort from given language (TRS) server"""
        log.debug("[UNQ] with data=\"{}\"".format(data))
        try:
            language = data[0]
            row = self.DB.get_row(language)
            ipaddress, ipport = row[1], row[2]
        except IndexError, e:
            # Invalid request. Not well formated
            log.error(e)
            return "UNR ERR"
        except Exception, e:
            # Invalid request for inexisting language
            log.error(e)
            return "UNR EOF"
        return "UNR {} {}".format(ipaddress, ipport)

    def _SRG(self, data):
        """Register incoming request from TRS server to local database"""
        log.debug("[SRG] with data=\"{}\"".format(data))
        try:
            # get configuration of incoming TRS request
            language, ipaddress, ipport = data[:]
            # check if language already register
            language_exists = self.DB.has_language(language)
            # check if Language Limit was already exceded.
            max_db_limit = len(self.DB.get_rows()) > settings.DB_LANGUAGE_MAX_LIMIT
            # check if language is valid
            language_is_valid = language in settings.ACCEPTED_LANGUAGES
            if not language_exists and not max_db_limit and language_is_valid:
                self.DB.add_trs_server(language, ipaddress, ipport)
            else:
                raise Exception("Language \"{}\" already register or not valid. (DB row count = {})".format(
                    language, len(self.DB.get_rows())))
            status = "OK"
        except Exception, e:
            log.error(e)
            status = "NOK"
        return "SRR {}".format(status)

    def _SUN(self, data):
        """Unregister incoming TRS server from local database"""
        log.debug("[SUN] with data=\"{}\"".format(data))
        try:
            # get configuration of incoming TRS request
            language, ipaddress, ipport = data[:]
            self.DB.remove_trs_server(language, ipaddress, ipport)
            status = "OK"
        except Exception, e:
            log.error(e)
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

    handler = TCSHandler()
    try:
        # running server
        udp = UDP(settings.DEFAULT_TCS_NAME, args.tcs_port)
        udp.run(handler=handler)
    except KeyboardInterrupt, e:
        # if CTRL+C is pressed, then go for last step
        log.info("Exiting TCS Server...")
        pass
    finally:
        # remove db file
        handler.DB.close()

