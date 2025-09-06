import requests
import json
import argparse
from cryptography.fernet import Fernet
import os

parser = argparse.ArgumentParser(description="Chat client")
group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("--read", metavar="CHAT", type=str, help="Read messages from a chat")
group.add_argument("--send", nargs=2, metavar=("CHAT", "MESSAGE"), help="Send a message to a chat")
group.add_argument("--genkey", metavar="CHAT", type=str, help="Generate a new encryption key.")

args = parser.parse_args()

with open("config.json", "r", encoding="utf-8") as config:
    configData = json.load(config)
host = configData["host"]
if not host.endswith("/"):
    host += "/"
username = configData["username"]

def checkServer(host):
    try:
        r = requests.get(host)
        t = r.json()
    except:
        print("Can't connect to server.")
        exit()
    print("Connected to server.")

def encrypt(text, key):
    cipher = Fernet(key)
    return cipher.encrypt(text.encode())

def decrypt(text, key):
    cipher = Fernet(key)
    return cipher.decrypt(text).decode()

def formatter(data, key):
    text = """"""
    for message in data["messages"]:
        content = decrypt(message["content"].encode(), key)
        if message["user"] == username:
            text = text + f"""\n\x1b[41m{message["user"]}\x1b[0m\n{content}\n"""
        else:
            text = text + f"""\n\x1b[46m{message["user"]}\x1b[0m\n{content}\n"""
    return text

def send(message, chat):
    checkServer(host)
    key_path = f"keys/{chat}.key"
    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except:
        print(f"No key found. Generate one with python3 main.py --genkey {chat}")
        exit()
    message = encrypt(message, key)
    r = requests.get(f"{host}chat/{chat}/send", params={"username": username, "message": message.decode()})
    if r.json()["status"] == "error":
        if r.json()["message"] == "User is not whitelisted":
            print("You are not whitelisted.")
            exit()
    print("Message sent.")

def read(chat):
    checkServer(host)                                                        
    key_path = f"keys/{chat}.key"
    try:
        with open(key_path, "rb") as f:
            key = f.read()
    except:
        print(f"No key found. Generate one with python3 main.py --genkey {chat}")
        exit()
    r = requests.get(f"{host}chat/{chat}/receive", params={"username": username})
    if r.json()["status"] == "error":
        if r.json()["message"] == "User is not whitelisted":
            print("You are not whitelisted.")
            exit()
    print(formatter(r.json(), key))

def checkFolder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
        existance = False
    else:
        existance = True
    return existance

if args.genkey:
    checkFolder("keys")
    print("Generating key...")
    chat = args.genkey
    key = Fernet.generate_key()
    with open(f"keys/{chat}.key", "wb") as f:
        f.write(key)
    print("Key generated.")                                                          
elif args.send:
    chat, message = args.send
    send(message, chat)
elif args.read:
    chat = args.read
    read(chat)
