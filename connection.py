#!/usr/bin/python3

"""
connection.py
description: classes and functions for connections
"""

# IMPORTS
import socket
from security import Encryptor

# FUNCTIONS
def make_socket_listener(s, port, load):
	s.bind(('', port))
	s.listen(load)

def open_socket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	return s

def connect_to_host(conn, host, port):
	conn.connect((host, port))

def receive(conn, encryptor):
	data = ""
	t_bytes = -1
	while len(data) != t_bytes:
		if len(data) >= 24:
			t_bytes = int(data[8:24])
		if len(data) != t_bytes:
			data = data + conn.recv(1).decode("utf-8")
	return data[0:8], data[24:]

def send(data_type, data_content, conn, encryptor):
	data = data_type + make_16_bytes(str(24 + len(str(data_content)))) + str(data_content)
	conn.send(bytes(data, "utf-8"))

def make_16_bytes(tmp):
	tmp = str(tmp)
	while len(tmp) < 16:
		tmp = '0' + tmp
	return tmp