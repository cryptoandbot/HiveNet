#!/usr/bin/python3

"""
listener.py

created by coffeeandscripts
v 0.1

description: listener class and relevant functions
"""
from Crypto.PublicKey import RSA
import socket

# running on a separate thread will listen on a port and act on data that it recieves
class Listener():
    def __init__(self):
        self.port = 1984

    def listen(self, swarm, settings):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.bind(('', self.port))
            s.listen(10)
            conn, addr = s.accept()
            print("Connection from " + str(addr))
            conn.send(("Thanks for connecting").encode('utf-8'))
            conn.close()
            s.close()

# uses public key to encrypt byte data
def encrypt(public_key, data):
    pub_key_obj = RSA.importKey(public_key)
    return pub_key_obj.encrypt(data, 'x')[0]

# uses private key to decrypt byte data
def decrypt(private_key, data):
    priv_key_obj = RSA.importKey(private_key)
    return priv_key_obj.decrypt(data)
