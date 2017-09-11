#!/usr/bin/python3

"""
swarm.py

created by coffeeandscripts
v 0.1

description: swarm/node classes and relevant functions
"""
import hashlib
import socket
from listener import encrypt, decrypt

# object that has a collection of Bees within the network
# has functions to manipulate the current swarm blockchain and transfer it
class Swarm():
    def __init__(self):
        self.swarm = []
        self.active_swarm = []

    # joins a current swarm and updates itself or starts a new one
    def join_swarm(self, hostname, settings):
        if hostname == "queen":
            self.add_to_swarm(settings.ip_address, settings.public_key, 0)
        else:
            self.request_swarm(hostname, settings.public_key, settings.port)
            # request hostname for latest swarm
            # add self to swarm
            # begin a swarm update

    # asks the queen bee (or given ip) for the latest swarm blockchain
    def request_swarm(self, hostname, public_key, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))
        data = '' + public_key
        s.send(data.encode('utf-8'))
        data = s.recv(2048).decode('utf-8')
        print(str(data))
        s.close()

    # goes through the blockchain to figure out active bees
    def generate_active_swarm(self):
        pass

    # adds an ip address and public key to the swarm as active
    def add_to_swarm(self, ip_address, public_key, prev_hash):
        self.swarm.append(Bee(ip_address, public_key, prev_hash))

# object that defines a single node on the network
class Bee():
    def __init__(self, ip_address, public_key, prev_hash):
        self.ip_address = ip_address
        self.public_key = public_key
        self.prev_hash = prev_hash
    
    # generates an SHA256 hash based on its own contents and previous hash
    def hash(self):
        tmp = ip_address + public_key + prev_hash
        return str(hashlib.sha256(tmp.encode('utf-8')).hexdigest())
