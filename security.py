#!/usr/bin/python3

"""
security.py
description: classes and functions for security
"""

# IMPORTS
from Crypto.PublicKey import RSA

# CLASSES
class Encryptor():
	def __init__(self):
		self.public_key = None
		self.private_key = None

	def pub_priv_key_pair_gen(self):
		key = RSA.generate(2048)
        self.private_key = key.exportKey('PEM')
        self.public_key = key.publickey().exportKey('PEM')

	def encrypt(self, data):
	    pub_key_obj = RSA.importKey(self.public_key)
	    return pub_key_obj.encrypt(data, "x")[0]

	def decrypt(self, data):
	    priv_key_obj = RSA.importKey(self.private_key)
	    return priv_key_obj.decrypt(data)