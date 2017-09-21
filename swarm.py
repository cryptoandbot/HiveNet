#!/usr/bin/python3

"""
swarm.py

created by coffeeandscripts
v 0.1

description: swarm/node classes and relevant functions
"""
import hashlib
import socket
import pickle
from datetime import datetime
from time import sleep
from random import randint
from listener import encrypt, decrypt, receive, send, make_16_bytes

# object that has a collection of Bees within the network
# has functions to manipulate the current swarm blockchain and transfer it
class Swarm():
    def __init__(self):
        self.swarm = []
        self.active_swarm = []
        self.hash = None

    def print_swarm(self):
        print("Swarm:")
        for b in self.swarm:
            b.print_bee()
        print("Active_swarm:")
        for b in self.active_swarm:
            b.print_bee()

    # joins a current swarm and updates itself or starts a new one
    def join_swarm(self, hostname, settings):
        if hostname == "queen":
            self.add_to_swarm(settings.ip_address, settings.public_key, 0)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.connect((hostname, settings.port))
            self.request_swarm(s, settings.public_key)
            self.swarm = self.eval_swarm(self.receive_swarm(s))
            self.active_swarm = self.eval_swarm(self.receive_active_swarm(s))
            swarm_hash = self.set_hash(settings.ip_address, self.active_swarm_hash())
            self.send_active_swarm_hash(s, swarm_hash)
            s.close()
            self.print_swarm()
            self.update_all_swarm(settings)

    # interprets the byte stream for requested swarm and returns an array of Bees
    def eval_swarm(self, raw_swarm):
        return pickle.loads(eval(raw_swarm))

    # asks the queen bee (or given ip) for the latest swarm blockchain
    def request_swarm(self, conn, public_key):
        buffer = str(public_key)      
        send(conn, "REQUSWRM", buffer)

    def receive_swarm(self, conn):
        data_type, data_content = receive(conn)
        return data_content

    def receive_active_swarm(conn):
        data_type, data_content = receive(self, conn)
        return data_content

    # generates a hash for the current active swarm from individual hashes
    def active_swarm_hash(self):
        tmp = ""
        for b in self.active_swarm:
            tmp = tmp + b.hash()
        return str(hashlib.sha256(tmp.encode("utf-8")).hexdigest())


    # sets the hash within the active swarm based on public key
    def set_hash(self, ip_address, swarm_hash):
        for b in self.active_swarm:
            if b.ip_address == ip_address:
                b.swarm_hash = swarm_hash
                break
        return swarm_hash

    def send_active_swarm_hash(self, conn, swarm_hash):
        buffer = str(swarm_hash)
        send(conn, "SWRMHASH", buffer)
    
    def send_swarm(self, conn):
        buffer = str(pickle.dumps(self.swarm))
        send(conn, "LTSTSWRM", buffer)

    def send_active_swarm(self, conn):
        buffer = str(pickle.dumps(self.active_swarm))
        send(conn, "ACTVSWRM", buffer)

    # sends current swarm to a random bee that doesn't have a matching swarm hash
    def update_all_swarm(self, settings):
        self.generate_active_swarm()
        swarm_hash = self.set_hash(settings.ip_address, self.active_swarm_hash())
        if self.total_unmatched(swarm_hash) > 0:
            conn, ip_address = self.random_connection(swarm_hash, self.total_unmatched(swarm_hash))
            self.send_swarm(conn)
            self.send_active_swarm(conn)
            data_type, data_content = receive(conn)
            self.set_hash(ip_address, data_content)
            self.print_swarm()
            conn.close()

    # adds an ip address and public key to the swarm as active
    def add_bee(self, ip_address, public_key, prev_hash):
        self.swarm.append(Bee(ip_address, public_key, prev_hash, 1, datetime.now()))

    # goes through the blockchain to figure out active bees
    def generate_active_swarm(self):
        tmp_swarm = self.active_swarm
        self.active_swarm = []
        prev_hash = 0
        for b in self.swarm:
            if b.state == 1:
                self.active_swarm.append(Bee(b.ip_address, b.public_key, prev_hash, b.state, b.created_at))
                prev_hash = self.active_swarm[-1].hash()
        for b in tmp_swarm:
            for bb in self.active_swarm:
                if b.ip_address == bb.ip_address:
                    bb.swarm_hash = b.swarm_hash
 
    # returns int for the total number of bees in the swarm that don't match the active swarm hash of self
    # used to randomly find one to send swarm blockchain to
    def total_unmatched(self, swarm_hash):
        n = 0
        for b in self.active_swarm:
            if b.swarm_hash != swarm_hash:
                n += 1
        return n

    def random_connection(self, swarm_hash, total_unmatched):
        rdm = randint(1, total_unmatched)
        n = 1
        s = None
        for b in self.active_swarm:
            if n == rdm and b.swarm_hash != swarm_hash:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.connect((str(b.ip_address), 1984))
            elif b.swarm_hash != swarm_hash:
                n += 1
        return s

    # synchronises two swarm blockchains
    def consolidate(self, data, addr):
        self.swarm = data

# object that defines a single node on the network
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
    
    # generates an SHA256 hash based on its own contents and previous hash
    def hash(self):
        tmp = str(self.ip_address) + str(self.public_key) + str(self.prev_hash) + str(self.state) + str(self.created_at)
        return str(hashlib.sha256(tmp.encode("utf-8")).hexdigest())

    def print_bee(self):
        print("Bee:")
        print("    ip_address: " + str(self.ip_address))
        print("    public_key: " + str(self.public_key))
        print("    state: " + str(self.state))
        print("    swarm_hash: " + str(self.swarm_hash))
        print("    created_at: " + str(self.created_at))
        print("    updated_at: " + str(self.updated_at))
