# !/usr/bin/python
# -*- coding: utf-8 -*-
"""All project settings are defined here"""
import os
# Group Number
GN = 1

# Set loggin as debug level
DEBUG = True

# Translation Contact Server default configuration
DEFAULT_TCS_NAME = 'localhost'
DEFAULT_TCS_PORT = 58000 + GN

# Translation Server default configurations
DEFAULT_TRS_PORT = 59000

# Size for buffer to hold all messages send between client and server (1024bytes*4*1024 = 4mb)
BUFFERSIZE = 4096 * 1024

# Timeout delay that we accept between connections, in seconds
TIMEOUT_DELAY = 2

