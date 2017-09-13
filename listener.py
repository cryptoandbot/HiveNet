#!/usr/bin/python3

"""
listener.py

created by coffeeandscripts
v 0.1

description: listener class and relevant functions
"""
from Crypto.PublicKey import RSA
import socket
import pickle

# running on a separate thread will listen on a port and act on data that it recieves
class Listener():
    def __init__(self):
        self.port = 1984
    
    # loop to constantly listen for socket and perform actions accordingly
    # should add threading
    def listen(self, swarm, settings):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.bind(('', self.port))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.listen(10)
            conn, addr = s.accept()
            data = conn.recv(4069).decode("utf-8")
            self.data_translate(data, addr, conn, swarm, settings)
            conn.close()
            s.close()

    # responds with swarm list in pickle form
    def requswrm(self, swarm, settings):
        data = "LTSTSWRM" + pickle.dumps(swarm)
        conn.send(data).encode("utf-8")
    
    # response to the latest swarm being recieved
    def ltstswrm(self, swarm, data, addr, conn):
        swarm = swarm.consolidate(pickle.loads(data), addr)
        data = "SWRMHASH" + swarm.active_swarm_hash()
        conn.send(data).encode("utf-8")
        swarm.update_all_swarm()

    # interprets the type of data recieved and acts on it
    def data_translate(self, data, addr, conn, swarm, settings):
        data_type, data_content = data[0:8], data[8:]
        if data_type == "REQUSWRM":
            self.requswrm(swarm, settings)
        elif data_type == "LTSTSWRM":
            self.ltstswrm(swarm, data, addr)
            

# uses public key to encrypt byte data
def encrypt(public_key, data):
    pub_key_obj = RSA.importKey(public_key)
    return pub_key_obj.encrypt(data, "x")[0]

# uses private key to decrypt byte data
def decrypt(private_key, data):
    priv_key_obj = RSA.importKey(private_key)
    return priv_key_obj.decrypt(data)
