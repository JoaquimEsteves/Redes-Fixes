# !/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import settings

class Logger(object):
    """Utils Logging has 4 variables that controls if the log goes to the output(screen)
    _error, _debug, _warning and _info default:  all loggers are enable except debug, which is False

    to enable debug log just add the following lines to your code
    from utils import Logger
    log = Logger(debug=True)
    log.info("Information message")
    """
    def __init__(self, debug=False, info=True, error=True, warning=True):
        self._error = error
        self._debug = debug
        self._warning = warning
        self._info = info

    def error(self, msg):
        if self._error:
            print("[ERROR]: {}".format(msg))

    def debug(self, msg):
        if self._debug:
            print("[DEBUG]: {}".format(msg))

    def info(self, msg):
        if self._info:
            print("[INFO]: {}".format(msg))

    def warning(self, msg):
        if self._warning:
            print("[WARNING]: {}".format(msg))


def create_translation_files():
    # create transltion files
    keywords = "ola mundo tudo bem como vai a vida espero que vá bem porreiro pah chiça penico fibra optica".split()
    for l in settings.ACCEPTED_LANGUAGES:
        filename = "trs_{}.txt".format(l)
        with open(filename, 'w+') as f:
            content = map(
                lambda x: "{}\t{}".format(x[0], x[1]),
                zip(keywords, ['<translation_required>'] * len(keywords))
            )
            f.write("\n".join(content))

