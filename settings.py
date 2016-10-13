# !/usr/bin/python
# -*- coding: utf-8 -*-
"""All project settings are defined here"""
import os
import socket
# Group Number
GN = 1

# Set loggin as debug level
DEBUG = True

# Translation Contact Server default configuration
DEFAULT_TCS_NAME = socket.gethostbyname(socket.gethostname())  # 'localhost'
DEFAULT_TCS_PORT = 58000 + GN

# Translation Server default configurations
DEFAULT_TRS_NAME = socket.gethostbyname(socket.gethostname())  # 'localhost'
DEFAULT_TRS_PORT = 59000

# Size for buffer to hold all messages send between client and server (1024bytes*4*1024 = 4mb)
BUFFERSIZE = 4096 * 1024

# Timeout delay that we accept between connections, in seconds
TIMEOUT_DELAY = 5

# Translated properties
TRANSLATE_WORD_MAX_CHARS = 30
TRANSLATE_MAX_LIMIT = 10
TRANSLATE_TEXT_FILENAME = os.getcwd() + "/{}/text_translation.txt"
TRANSLATE_FILE_FILENAME = os.getcwd() + "/file_translation.txt"
F_IMAGE_FILENAME = "pyrion{}.png"
ACCEPTED_LANGUAGES = ['Inglês', 'Françês', 'Espanhol', 'Alemão', 'Italiano']

# "Local Database" path
DB_PATH = os.getcwd() + "/local_db.txt"
DB_LANGUAGE_MAX_CHARS = 20
DB_LANGUAGE_MAX_LIMIT = 99
