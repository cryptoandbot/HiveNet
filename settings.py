#!/usr/bin/python3

"""
settings.py

created by coffeeandscripts
v 0.1

description: settings class and relevant functions
"""
from requests import get
from Crypto.PublicKey import RSA

# object that stores and manipulates general settings throughout
class Settings():
    def __init__(self):
        self.ip_address = None
        self.port = 1984
        self.public_key = None
        self.private_key = None

    # run at first creation to generate some variables
    def setup(self):
        self.set_ip_address()
        self.set_key_pair()

    # GET request to return ip address as a string (OPTIMIZE)
    def set_ip_address(self):
        self.ip_address = get('https://api.ipify.org').text

    # sets a private key and public key as readable bytes
    def set_key_pair(self):
        key = RSA.generate(2048)
        self.private_key = key.exportKey('PEM')
        self.public_key = key.publickey().exportKey('PEM')
