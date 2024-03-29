import socket
import argparse
import select
import logging
import safe_connection

def handle_reads(read_ready, messages):
    for connection in read_ready:
        logging.info(f'Connection ready to read: {connection}')
        message = connection.recv(1024).decode()
        logging.info(f'Received message: {message} {len(message)}')
        messages[connection] = message

def handle_writes(write_ready, messages):
    for connection in write_ready:
        if connection not in messages:
            continue
        message = messages[connection]
        logging.info(f'Connection ready to write: {connection}: {message}')
        connection.send(f'Echo: {message}'.encode())
        del messages[connection]

def accept_connection(server, connections):
    connection, peer_address = server.accept()
    connection = safe_connection.SafeConnection(connection)
    logging.info(f'Connection from {peer_address}')
    connections.append(connection)
    return connection

def serve(port):
    server = socket.socket()
    server.bind(('', port))
    server.listen(5)

    connections = []
    messages = {}

    while True:
        read_ready, write_ready, errors = select.select(connections + [server], connections, [])
        logging.info(f'Ready to read: {len(read_ready)} Ready to write: {len(write_ready)}')
        logging.info(f'errors: {len(errors)}')
        if server in read_ready:
            connection = accept_connection(server, connections)
            read_ready.remove(server)

        handle_reads(read_ready, messages)
        handle_writes(write_ready, messages)
        connections = [connection for connection in connections if not connection.done()]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('port', type=int)
    arguments = parser.parse_args()
    serve(arguments.port)
