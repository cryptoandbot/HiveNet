#!/usr/bin/python3

"""
hiveNet.py

created by coffeeandscripts
v 0.1

description: runs main loop
"""
from settings import Settings
from listener import Listener, encrypt, decrypt
from swarm import Swarm, Bee
import sys
from _thread import start_new_thread

# generates all relevant objects and values for start of system
def setup():
    listener = None
    if len(sys.argv) == 2:
        settings = Settings()
        settings.setup()
        listener = Listener()
        swarm = Swarm()
        swarm.join_swarm(sys.argv[1], settings)
    else:
        print("Failed")
        sys.exit()
    return listener, swarm, settings

if __name__ == "__main__":
    listener, swarm, settings = setup()
    listener.listen(swarm, settings)

