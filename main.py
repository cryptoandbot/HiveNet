#!/usr/bin/python3

"""
main.py
description: runs main loop
"""

# IMPORTS
import sys
from _thread import start_new_thread
from listener import Listener
from security import Encryptor
from swarm import Swarm

# FUNCTIONS
def setup():
	if len(sys.argv) == 2:
		listener = Listener()
		listener.set_port(1984)
		listener.set_ip_address()
		encryptor = Encryptor()
		encryptor.pub_priv_key_pair_gen()
		swarm = Swarm()
		swarm.join_swarm(sys.argv[1], listener.ip_address, encryptor)
	else:
		print("Failed")
		sys.exit()
	return listener, encryptor, swarm

# MAIN LOOP
if __name__ == '__main__':
	listener, encryptor, swarm = setup()
	#start_new_thread(listener.listen, (encryptor,))
	listener.listen(swarm, encryptor)