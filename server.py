import socket
import time
import logging
import json


names = []
name_to_connection = {}


def parse_json(client_message, connection_name, connection):
    loaded_json = json.loads(client_message.decode())
    
    if loaded_json["code"] == "hello":
        names.append(client_message["name"])
        name_to_connection[client_message["name"]] = connection
        return json.dumps({"code":"welcome"}) , loaded_json["name"]

    if loaded_json["code"] == "who":
        return json.dumps({"code":"users", "users":names}, connection_name

    if loaded_json["code"] == "outgoing":
        return json.dumps({"code":"incoming", "from":connection_name, "content":loaded_json["content"]}), loaded_json["to"]

    if loaded_json["code"] == "outgoing_broadcast":
        return json.dumps({"code":"incoming_broadcast", "from":connection_name, "content":loaded_json["content"]}), names, connection_name

    if loaded_json["code"] == "quit":
        connection.close()
        names.remove(connection_name)
        names_to_connection.pop(connection_name)


def send(client_message, connection_name, connection):
    route = parse_json(client_meesage, connection_name, connection)
    encoded_message = route[0].encode()
    if type(route[1]) == str:
        connection = name_to_connection[connection_name]
        connection.send(encoded_message)
    else:
        for name in route[1]:
            if name != route[2]:
                connection = name_to_connection[name]
                connection.send(encoded_message)


def serve():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('', 3333))
    server.listen(5)  
    nicknames = []

    while True:
        try:
            connection, peer_address = server.accept()
            data = connection.recv(1024)
            route = parse_json(data.decode())
            send(data, temp, connection)
        except:
            for name in names:
                connection = name_to_connection[name]
                try:
                    data = connection.recv(1024)
                    route = parse_json(data.decode())
                    send(data, name, connection)
                except:
                    pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    serve()