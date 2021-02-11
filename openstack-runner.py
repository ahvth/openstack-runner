# test connection with `curl --header "Content-Type: application/json" --request POST --data '{"username":"xyz","password":"xyz"}' http://localhost:8090` 

import socket
import json

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('0.0.0.0', 8090))

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

def get_connections(serversocket):
    data = ''
    connection, address = serversocket.accept()
    buf = connection.recv(1024)
    if len(buf) > 0:
        u = buf.decode('utf-8')
        json_objects = []
        for obj in extract_json_objects(u):
            json_objects.append(obj)
        if len(json_objects) == 1:
            response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\nJSON data posted. Disconnecting.\n"
            print(json_objects[0])
            enc_response = response.encode('utf-8')
            connection.send(enc_response)
            connection.close()
            return data       
        elif len(json_objects) > 1:
            response = "HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\nMalformed request. Too many JSON arrays provided.\n"
            print("Got bad request.")
            enc_response = response.encode('utf-8')
            connection.send(enc_response)
            connection.close()
        else:
            response = "HTTP/1.1 400 Bad Request\nContent-Type: text/html\n\nMalformed request.\n"
            print("Got bad request.")
            enc_response = response.encode('utf-8')
            connection.send(enc_response)
            connection.close()

def process_data():
    pass

while True:
    get_connections(serversocket)