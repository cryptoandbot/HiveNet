#!/usr/bin/python3

"""
listener.py
description: listener class and relevant functions
"""

# IMPORTS
import socket
from requests import get
from connection import *
from security import Encryptor
from _thread import start_new_thread

# CLASSES
class Listener():
	def __init__(self):
		self.ip_address = None
		self.port = None

	def set_port(self, port):
		self.port = port

	def set_ip_address(self):
		self.ip_address = get("https://api.ipify.org").text

	def listen(self, swarm, encryptor):
		while True:
			s = open_socket()
			make_socket_listener(s, 1984, 10)
			conn, addr = s.accept()
			start_new_thread(self.run_conn, (conn, addr, swarm, encryptor,))

	def run_conn(self, conn, addr, swarm, encryptor):
		data_type, data_content = receive(conn, encryptor)
		if data_type == "MSGERROR":
			pass
		elif data_type == "JOINSWRM":
			swarm.add_to_swarm(addr[0], data_content, swarm.swarm[-1].hash())
			swarm.generate_active_swarm()
			swarm.add_hash(self.ip_address, swarm.active_swarm_hash())
			swarm.send_latest_swarm(conn, encryptor)
			swarm.send_active_swarm(conn, encryptor)
			swarm.add_hash(addr[0], swarm.receive_active_swarm_hash(conn, encryptor))
			swarm.update_swarm(self.ip_address, encryptor)
			swarm.print_swarm()
		elif data_type == "LTSTSWRM":
			pass
			# consolidate latest swarm
			# receive active swarm
			# swarm hash
			# add hash to swarm
			# send hash
			# update swarm
