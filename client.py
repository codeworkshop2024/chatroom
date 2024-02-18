import socket
import json
import argparse
import threading


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('server_ip', type=str)
    parser.add_argument('server_port', type = str)
    parser.add_argument('my_nickname', type=str)
    arguments = parser.parse_args()

    socket = socket.socket()
    socket.connect((arguments[0], arguments[1]))
    print(f"connecting to server at {arguments[0]}, {argument[1]}")
    print("current users:")
    names = socket.send("who".encode())
    for name in names:
        print(name)
    

def get_input():
    global user_input
    user_input = input("enter your message>")



def parse_user_message(message, name):
    if message in ("who", "quit"):
        return json.dumps({"code":message})
    if '|' not in message:
        return error
    index| = message.index('|')
    to_send_user = message[0:index|]
    to_send_message = message[index|+1:len(message)]
    
    if to_send_user == "*":
        return json.dumps({"code": "outgoing_broadcast", "content": to_send_message}
    else:
        return json.dumps({"code": to_send_user, "from": user_name, "content": to_send_message})



def parse_server_message(message):
    loaded_json = json.loads(message.decode())

        if loaded_json["code"] == "welcome":
            return "Enter username: "

        if loaded_json["code"] == "users":
            return loaded_json["users"]

        if loaded_json["code"] == "incoming":
            return loaded_json["from"] + "|" + loaded_json["content"]

        if loaded_json["code"] == "incoming_broadcast":
            return "*" + loaded_json["from"] + "|" + loaded_json["content"]