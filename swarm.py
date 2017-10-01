#!/usr/bin/python3

"""
swarm.py

created by coffeeandscripts
v 0.1

description: swarm/node classes and relevant functions
"""

# IMPORTS
import hashlib
import socket
import pickle
from datetime import datetime
from time import sleep
from random import randint

# CLASSES

class Swarm():
	def __init__(self):
		self.swarm = []
		self.active_swarm = []
		self.hash = None

	def print_swarm(self):
		pass

	def request_swarm(self, conn, public_key):
		send("JOINSWRM", public_key, conn)

	def add_to_swarm(self, ip_address, public_key, prev_hash):
		self.swarm.append(Bee(ip_address, public_key, prev_hash, 1, datetime.now()))

	def generate_active_swarm(self):
		tmp_active_swarm = self.active_swarm
		tmp_bees = []
		for b in self.swarm:
			already_in_swarm = False
			if b.state = 1:
				for bb in tmp_bees:
					if b.public_key == bb.public_key:
						already_in_swarm = True
				if alread_in_swarm == False:
					tmp_bees.append(b)
			else:
				for bb in tmp_bees:
					if b.public_key == bb.public_key:
						tmp_bees.remove(bb)
		self.active_swarm = []
		prev_hash = 0
		for b in tmp_bees:
			self.active_swarm.append(Bee(b.ip_address, b.public_key, prev_hash))
			prev_hash = self.active_swarm[-1].hash()
		for b in tmp_active_swarm:
			for bb in self.active_swarm:
				if b.public_key == bb.public_key:
					bb.swarm_hash = b.swarm_hash

	def active_swarm_hash(self):
		tmp = ""
        for b in self.active_swarm:
            tmp = tmp + b.hash()
        return str(hashlib.sha256(tmp.encode("utf-8")).hexdigest())

	def add_hash(self, ip_address, swarm_hash):
		for b in self.active_swarm:
			if b.ip_address == ip_address:
				b.swarm_hash = swarm_hash

	def send_latest_swarm(self, conn, encryptor):
		data_content = str(pickle.dumps(self.swarm))
		send("LTSTSWRM", data_content, conn)

	def send_active_swarm(self, conn, encryptor):
		data_content = str(pickle.dumps(self.active_swarm))
		send("ACTVSWRM", data_content, conn)

	def receive_active_swarm_hash(self, conn, encryptor):
		data_type, data_content = receive(conn, encryptor)
		if data_type == "SWRMHASH":
			pass
		else:
			pass
		return data_content

	def send_active_swarm_hash(self, conn, swarm_hash, encryptor):
		send("SWRMHASH", swarm_hash, conn)

	def total_unmatched(self):
		pass

	def update_bee(self):
		pass

	def remove_bee(self):
		pass

	def remove_self(self):
		pass

	def request_reconnect(self):
		pass

	def accept_connection(self):
		pass

	def health_check(self):
		pass

	def health_check_bee(self):
		pass

	def receive_swarm(self, conn, encryptor):
		data_type, data_content = receive(conn, encryptor)
		if data_type == "LTSTSWRM":
			pass
		else:
			pass
		return data_content
	def receive_active_swarm(self, conn, encryptor):
		data_type, data_content = receive(conn, encryptor)
		if data_type == "ACTVSWRM":
			pass
		else:
			pass
		return data_content

	def eval_swarm(self, raw_swarm):
        return pickle.loads(eval(raw_swarm))

	def join_swarm(self, host, self_ip_address, encryptor):
		if host == "queen":
			self.add_to_swarm(self_ip_address, encryptor.public_key, 0)
		else:
			conn = open_socket()
			conn = connect_to_host(conn, host, 1984)
			self.request_swarm(conn, encryptor.public_key)
			self.swarm = self.eval_swarm(self.receive_swarm(conn, encryptor))
			self.active_swarm = self.eval_swarm(self.receive_active_swarm(conn, encryptor))
			actv_swrm_hash = self.active_swarm_hash()
			self.add_hash(self_ip_address, actv_swrm_hash)
			self.send_active_swarm_hash(conn, actv_swrm_hash, encryptor)
			self.update_swarm

	def update_swarm(self):
		pass

class Bee():
	def __init__(self, ip_address, public_key, prev_hash, state, created_at):
        self.ip_address = ip_address
        self.public_key = public_key
        self.prev_hash = prev_hash
        self.state = state
        self.swarm_hash = None
        self.healthcheck_at = None
        self.created_at = created_at
        self.updated_at = datetime.now()

	def hash(self):
		tmp = str(self.ip_address) + str(self.public_key) + str(self.prev_hash) + str(self.state) + str(self.created_at)
        return str(hashlib.sha256(tmp.encode("utf-8")).hexdigest())

	def print_bee(self):
		pass