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
from random import randint
from listener import encrypt, decrypt

# object that has a collection of Bees within the network
# has functions to manipulate the current swarm blockchain and transfer it
class Swarm():
    def __init__(self):
        self.swarm = []
        self.active_swarm = []
        self.hash = None

    # joins a current swarm and updates itself or starts a new one
    def join_swarm(self, hostname, settings):
        if hostname == "queen":
            self.add_to_swarm(settings.ip_address, settings.public_key, 0)
        else:
            self.swarm = self.eval_swarm(self.request_swarm(hostname, settings.public_key, settings.port))
            self.add_to_swarm(settings.ip_address, settings.public_key, self.swarm[-1].hash())
            self.generate_active_swarm()
            self.update_all_swarm(settings)

    # interprets the byte stream for requested swarm and returns an array of Bees
    def eval_swarm(self, raw_swarm):
        return eval(raw_swarm)

    # asks the queen bee (or given ip) for the latest swarm blockchain
    def request_swarm(self, hostname, public_key, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        data = 'REQUSWRM' + public_key
        s.send(data.encode('utf-8'))
        data = s.recv(4096).decode('utf-8')
        s.close()
        return data

    def remove_bee(self, public_key):
        n = 0
        for b in self.active_swarm:
            if b.public_key == public_key:
                del self.active_swarm[n]
            else:
                n += 1

    # goes through the blockchain to figure out active bees
    def generate_active_swarm(self):
        prev_hash = 0
        for b in self.swarm:
            if b.state == 1:
                self.active_swarm.append(Bee(b.ip_address, b.public_key, prev_hash, b.state, b.created_at))
                prev_hash = self.active_swarm[-1].hash()
            else:
                self.remove_bee(b.public_key)

    # generates a hash for the current active swarm from individual hashes
    def active_swarm_hash(self):
        tmp = ""
        for b in self.active_swarm:
            tmp.append(b.hash())
        return str(hashlib.sha256(tmp.encode('utf-8')).hexdigest())

    # sets the hash within the active swarm based on public key
    def set_hash(self, public_key, swarm_hash):
        for b in self.active_swarm:
            if b.public_key == public_key:
                b.swarm_hash = swarm_hash
                break
        return swarm_hash

    # returns int for the total number of bees in the swarm that don't match the active swarm hash of self
    # used to randomly find one to send swarm blockchain to
    def total_unmatched(self, swarm_hash):
        n = 0
        for b in self.active_swarm:
            if b.swarm_hash != swarm_hash:
                n += 1
        return n

    # pickles and sends the whole swarm blockchain randomly
    # waits for a reply that is the active swarm hash from the recipient
    def send_swarm(self, swarm_hash, unmatched):
        rdm = randint(1, unmatched)
        n = 0
        for b in self.active_swarm:
            if n == rdm:
                data = "LTSTSWRM" + pickle.dumps(self.swarm)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((b.ip_address, 1984))
                s.send(data.encode('utf-8'))
                data = s.recv(4096).decode('utf-8')
                data_type, data_content = data[0:8], data[8:]
                if data_type == "SWRMHASH":
                    b.swarm_hash = data_content
                s.close()
                break
            else:
                n += 1

    # synchronises two swarm blockchains
    def consolidate(self, data, addr):
        tmp_swarm = data.generate_active_swarm()
        prev_swarm_hash = tmp_swarm.active_swarm_hash()
        for b in self.swarm:
            for bb in tmp_swarm:
                pass
                ## COMBINE THE TWO SWARMS
        # GENERATE NEW ACTIVE SWARM FOR SELF
        # ADD PREV_SWARM_HASH TO ACTIVE SWARM FOR THE SENDER

    # 
    def update_all_swarm(self):
        swarm_hash = self.set_hash(settings.public_key, self.active_swarm_hash())
        if self.total_unmatched(swarm_hash) > 0:
            self.send_swarm(swarm_hash, self.total_unmatched(swarm_hash))


    # adds an ip address and public key to the swarm as active
    def add_to_swarm(self, ip_address, public_key, prev_hash):
        self.swarm.append(Bee(ip_address, public_key, prev_hash))

# object that defines a single node on the network
class Bee():
    def __init__(self, ip_address, public_key, prev_hash, state, created_at):
        self.ip_address = ip_address
        self.public_key = public_key
        self.prev_hash = prev_hash
        self.state = state
        self.swarm_hash = None
        self.created_at = created_at
        self.updated_at = datetime.now()
    
    # generates an SHA256 hash based on its own contents and previous hash
    def hash(self):
        tmp = self.ip_address + self.public_key + self.prev_hash + str(self.state) + str(self.created_at)
        return str(hashlib.sha256(tmp.encode('utf-8')).hexdigest())
