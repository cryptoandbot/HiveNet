#!/usr/bin/python3

"""
settings.py

created by coffeeandscripts
v 0.1

description: settings class and relevant functions
"""
from requests import get
from Crypto.PublicKey import RSA

class Settings():
    def __init__(self):
        self.ip_address = None
        self.port = 1984
        self.public_key = None
        self.private_key = None

    def setup(self):
        self.set_ip_address()
        self.set_key_pair()

    def set_ip_address(self):
        self.ip_address = get('https://api.ipify.org').text


    def set_key_pair(self):
        key = RSA.generate(2048)
        self.private_key = key.exportKey('DER')
        self.public_key = key.publickey().exportKey('DER')
