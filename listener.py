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
                data = receive(conn)
                start_new_thread(self.data_translate, (data, addr, conn, swarm, settings, ))
            s.close()

    # responds with swarm list in pickle form
    def requswrm(self, conn, swarm, settings):
        buffer = str(pickle.dumps(swarm.swarm))
        data = "LTSTSWRM" + make_16_bytes(str(24 + len(buffer)))  + buffer
        conn.send(bytes(data, "utf-8"))
    
    # response to the latest swarm being recieved
    def ltstswrm(self, swarm, data, addr, conn, settings):
        swarm = swarm.consolidate(swarm.eval_swarm(data[24:]), addr)
        buffer = swarm.active_swarm_hash()
        swarm.set_hash(settings.ip_address, buffer)    
        data = "SWRMHASH" + make_16_bytes(str(24+ len(buffer))) + buffer
        conn.send(bytes(data, "utf-8"))
        data = receive(conn)
        data_type, data_content = data[0:8], data[24:]
        if data_type == "ACTVSWRM":
            swarm.active_swarm = swarm.eval_swarm(data_content)
        swarm.print_swarm()
        swarm.update_all_swarm(settings)

    # interprets the type of data recieved and acts on it
    def data_translate(self, data, addr, conn, swarm, settings):
        data_type, data_content = data[0:8], data[24:]
        if data_type == "REQUSWRM":
            self.requswrm(conn, swarm, settings)
        elif data_type == "LTSTSWRM":
            self.ltstswrm(swarm, data, addr, conn, settings)
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
            data = data + conn.recv(1024).decode("utf-8")
    return data
