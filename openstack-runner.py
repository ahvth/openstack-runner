# TODO: implement return codes from server

import socket
import json
import webob 

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost', 8090))

# become a server socket, maximum 5 connections
serversocket.listen(5) 


def extract_json_objects(text, decoder=json.JSONDecoder()):
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(1024)
    if len(buf) > 0:
        u = buf.decode('utf-8')
        result = []
        for obj in extract_json_objects(u):
            data = obj
        print(data)
