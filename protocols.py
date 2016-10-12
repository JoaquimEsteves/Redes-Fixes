#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import settings
from socket import *
from utils import Logger
log = Logger(debug=settings.DEBUG)

class Protocol(object):

    def __init__(self, host, port, buffer_size=settings.BUFFERSIZE, max_connections=1):
        self.host = host
        self.port = int(port)
        self.buffer_size = buffer_size
        self.max_connections = max_connections

    def _remove_new_line(self, message):
        """if exists, removes \n from the end of the message"""
        if message.endswith('\n'):
            return message[:-1]
        return message


class UDP(Protocol):
    """Class to wrap all UDP interactions between client and server"""
    def __init__(self, host, port=settings.DEFAULT_TCS_PORT):
        super(UDP, self).__init__(host, port)

    def request(self, data):
        """makes udp socket connection to host and port machine
        returns the raw response from the host machine"""
        # Create a new socket using the given address family, socket type and protocol number
        sock = socket(AF_INET, SOCK_DGRAM)
        # Set the value of the given socket option (see the Unix manual page setsockopt(2)).
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        # define timout to settings.TIMEOUT_DELAY
        sock.settimeout(settings.TIMEOUT_DELAY)
        try:
            log.debug("[UDP] Sending request to {}:{} > \"{}\".".format(self.host, self.port, self._remove_new_line(data)))
            # Send data to the socket.
            sock.sendto(data, (self.host, self.port))
            # Receive data from the socket (max amount is the buffer size).
            data = sock.recv(self.buffer_size)
            log.debug("[UDP] Got back > \"{}\".".format(self._remove_new_line(data)))
        # in case of timeout
        except timeout, msg:
            # TODO: Maybe retry 3 times
            log.error("[UDP] Request Timeout. {}".format(msg))
            data = "ERR"
        # in case of error
        except error, msg:
            log.error("[UDP] Something happen when trying to connect to {}:{}. Error: {}".format(self.host, self.port, msg))
            data = "ERR"
        finally:
            # Close socket connection
            sock.close()
        data = self._remove_new_line(data)
        return data

    def run(self, handler=None):
        """UDP server. TCS runs this server"""
        try:
            # Create a new socket using the given address family, socket type and protocol number
            sock = socket(AF_INET, SOCK_DGRAM)
        except error, msg:
            log.error(msg)
            raise error
        try:
            # Bind socket to local host and port
            sock.bind((self.host, self.port))
        except error , msg:
            log.error(msg)
            raise error

        log.info("UDP Server is ready for connection on [{}:{}].".format(self.host, self.port))
        # now keep talking with the client
        while True:
            # Receive data from client (data, addr)
            data, addr = sock.recvfrom(self.buffer_size)
            # Get connection HostIP and HostPORT
            addr_ip, addr_port = addr
            if not data:
                break
            log.debug("Got request from {}:{} > \"{}\".".format(addr_ip, addr_port, self._remove_new_line(data)))

            if not handler:
                raise ValueError("Handler is required!")
            data = handler.dispatch(data)

            log.debug("Sending back > \"{}\".".format(self._remove_new_line(data)))
            # Send data to the socket.
            sock.sendto(data, addr)
        # Close socket connection
        sock.close()


class TCP(Protocol):
    """Class to wrap all TCP interactions between client and server"""
    def __init__(self, host, port=settings.DEFAULT_TRS_PORT):
        super(TCP, self).__init__(host, port)

    def request(self, data):
        """makes tcp socket connection to host and port machine
        returns the raw response from the host machine"""
        # Create a new socket using the given address family, socket type and protocol number
        sock = socket(AF_INET, SOCK_STREAM)
        # Set the value of the given socket option (see the Unix manual page setsockopt(2)).
        sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        try:
            # Connect to a remote socket at address.
            sock.connect((self.host, self.port))
            # define timout to settings.TIMEOUT_DELAY
            sock.settimeout(settings.TIMEOUT_DELAY)
            log.debug("[TCP] Sending request to {}:{} > \"{}\".".format(self.host, self.port, self._remove_new_line(data)[:64]))
            # Send data to the socket.
            sock.sendall(data)
            # Receive data from the socket (max amount is the buffer size).
            data = sock.recv(self.buffer_size)
            log.debug("[TCP] Got back > \"{}\".".format(self._remove_new_line(data)[:64]))
        # in case of timeout
        except timeout, msg:
            log.error("[TCP] Request Timeout. {}".format(msg))
            data = "ERR"
        # in case of error
        except error, msg:
            log.error("[TCP] Something happen when trying to connect to {}:{}. Error: {}".format(self.host, self.port, msg))
            data = "ERR"
        finally:
            # Close socket connection
            sock.close()
        data = self._remove_new_line(data)
        return data

    def run(self, handler=None):
        """TCP server. TRS runs this server"""
        try:
            # Create a new socket using the given address family, socket type and protocol number
            sock = socket(AF_INET, SOCK_STREAM)
        except error, msg:
            log.error(msg)
            raise error
        try:
            # Bind socket to local host and port
            sock.bind((self.host, self.port))
            # Listen for connections made to the socket.
            sock.listen(self.max_connections)
        except error , msg:
            log.error(msg)
            raise error

        log.info("TCP Server is ready for connection on [{}:{}].".format(self.host, self.port))

        while True:
            # Accept a connection.
            connection, client_address = sock.accept()
            # Get connection HostIP and HostPORT
            addr_ip, addr_port = client_address
            try:
                # Receive data from socket
                data = ""
                data_connection = connection.recv(self.buffer_size)
                while data_connection[-1] != "\n":
                    data += data_connection
                    log.debug("Received {} bytes".format(len(data)))
                    data_connection = connection.recv(self.buffer_size)
                data += data_connection

                log.debug("Got request from {}:{} > \"{}\".".format(addr_ip, addr_port, self._remove_new_line(data_connection)[:64]))

                if data:
                    if not handler:
                        raise ValueError("Handler is required!")
                    data = handler.dispatch(data)

                    log.debug("Sending back > \"{}\".".format(self._remove_new_line(data)[:64]))
                    # Send data to the socket.
                    connection.sendall(data)
                else:
                    break
            finally:
                # Close socket connection
                connection.close()
