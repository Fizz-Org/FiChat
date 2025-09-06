from fastapi import FastAPI, Query
import uvicorn
import json
import os
from pathlib import Path

DEFAULT_CHAT_CONFIG = {"whitelist":["user1", "user2"]}

def checkConfig(path):
    with open(path) as config:
        configData = json.load(config)
    port = configData["port"]
    return port

def checkFolder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
        existance = False
    else:
        existance = True
    return existance

port = checkConfig("config.json")

with open("chats.json") as chats:
    chatsData = json.load(chats)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Server Online"}

checkFolder("chats")

def is_whitelisted(chat_name, username):
    config_path = Path("chats") / chatsData[chat_name]["folder"] / "config.json"
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            chat_config = json.load(f)
        return username in chat_config.get("whitelist", [])
    print("Config file not found:", config_path)
    return False

for chat in chatsData:
    chatData = chatsData[chat]
    if not checkFolder("chats/" + chatData["folder"]):
        with open("chats/" + chatData["folder"] + "/" + "config.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(DEFAULT_CHAT_CONFIG))
        with open("chats/" + chatData["folder"] + "/" + "messages.json", "w", encoding="utf-8") as file:
            json.dump([], file)
    
    async def chat_send(username: str = Query(...), message: str = Query(...), chat_name=chat):
        if not is_whitelisted(chat_name, username):
            return {"chat": chat_name, "status": "error", "message": "User is not whitelisted"}

        file_path = Path("chats") / chatsData[chat_name]["folder"] / "messages.json"
        with file_path.open("r", encoding="utf-8") as f:
            messages = json.load(f)

        messages.append({"user": username, "content": message})

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4)

        return {"chat": chat_name, "status": "sent", "user": username, "message": message}

    chat_send.__name__ = f"{chat}_send"
    app.add_api_route(f"/chat/{chat}/send", chat_send, methods=["GET"])

    async def chat_receive(username: str = Query(...), chat_name=chat):
        if not is_whitelisted(chat_name, username):
            return {"chat": chat_name, "status": "error", "message": "User is not whitelisted"}

        file_path = Path("chats") / chatsData[chat_name]["folder"] / "messages.json"
        with file_path.open("r", encoding="utf-8") as f:
            messages = json.load(f)

        user_messages = [m for m in messages]
        return {"chat": chat_name, "status": "received", "messages": user_messages}
    chat_receive.__name__ = f"{chat}_receive"
    app.add_api_route(f"/chat/{chat}/receive", chat_receive, methods=["GET"])

if __name__ == "__main__":
    uvicorn.run(app, port=port)
