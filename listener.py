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
from _thread import start_new_thread

# running on a separate thread will listen on a port and act on data that it recieves
class Listener():
    def __init__(self):
        self.port = 1984
    
    # loop to constantly listen for socket and perform actions accordingly
    # should add threading
    def listen(self, swarm, settings):
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.port))
            s.listen(10)
            print("Listening")
            conn, addr = s.accept()
            if str(addr[0]) != '192.168.0.1':
                print("New connection from " + str(addr))
                data_type, data_content = receive(conn)
                self.data_translate(data_type, data_content, addr, conn, swarm, settings)
            s.close()

    # responds with swarm list in pickle form
    def new_bee_join_swarm(self, conn, swarm, settings, ip_address, public_key):
        swarm.add_bee(ip_address, data_content, swarm[-1].hash())
        swarm.generate_active_swarm()
        swarm.send_swarm(conn)
        swarm.send_active_swarm(conn)
        data = receive(conn)
        data_type, data_content = data[0:8], data[24:]
        swarm.set_hash(ip_address, data_content)
        swarm.update_all_swarm(settings)
    
    # response to the latest swarm being recieved
    def updating_swarm(self, swarm, raw_swarm, addr, conn, settings):
        swarm.consolidate(swarm.eval_swarm(raw_swarm), addr)
        data_type, data_content = receive(conn)
        swarm.active_swarm = swarm.eval_swarm(data_content)
        swarm.generate_active_swarm()
        swarm_hash = swarm.set_hash(settings.ip_address, swarm.active_swarm_hash())
        buffer = str(swarm_hash)
        send(conn, "SWRMHASH", buffer)
        swarm.print_swarm()
        swarm.update_all_swarm(settings)

    # interprets the type of data recieved and acts on it
    def data_translate(self, data_type, data_content, addr, conn, swarm, settings):
        if data_type == "REQUSWRM":
            self.new_bee_join_swarm(conn, swarm, settings, addr[0], data_content)
        elif data_type == "LTSTSWRM":
            self.updating_swarm(swarm, data_content, addr, conn, settings)
        conn.close()
        print("Closed connection from " + str(addr))
            

# uses public key to encrypt byte data
def encrypt(public_key, data):
    pub_key_obj = RSA.importKey(public_key)
    return pub_key_obj.encrypt(data, "x")[0]

# uses private key to decrypt byte data
def decrypt(private_key, data):
    priv_key_obj = RSA.importKey(private_key)
    return priv_key_obj.decrypt(data)

def make_16_bytes(tmp):
    tmp = str(tmp)
    while len(tmp) < 16:
        tmp = '0' + tmp
    return tmp

def receive(conn):
    data = ""
    t_bytes = -1
    while len(data) != t_bytes:
        if len(data) >= 24:
            t_bytes = int(data[8:24])
        if len(data) != t_bytes:
            data = data + conn.recv(1).decode("utf-8")
    return data[0:8], data[24:]

def send(conn, data_type, buffer):
    data = data_type + make_16_bytes(str(24 + len(buffer))) + buffer
    conn.send(bytes(data, "utf-8"))
