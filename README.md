# FiChat
Private encrypted chat software for personal use.

Feel free to fork and add your own features. This is an extremley bare-bones version of whats possible.

Features:
- Multi-chat Compatibility
- End-To-End Encryption
- Chat Whitelisting
(If you want more, feel free to make them yourself!)

1st step: move the `server` folder to your server, and configure the port in `config.json` and make chats in `chats.json`. Now is about the right time to install the dependancies:
- fastapi
- uvicorn
Now when yyou first run `main.py`, it will generate a folder called `chats`, here you can find all the chats you make. Each chat has a `config.json` and a `messages.json`. In the `config.json`, you can find a whitelist where you can add whitelisted usernames for all the chats (please note anyone can chose whatever username they want, so if they know someone who is whitelisted, they still can obtain access). It is recommended to set up a domain for the chat. Next is the client-side of things. First get the `client` folder and change the `config.json` so that the host matches that of the server, and the username the one that is wwhitelisted. Now you should install the dependancies:
- requests
- cryptography
One person for every chat will run the command `python3 main.py --genkey <chat-name>` with `<chat-name>` being the actual name of the chat. The key will then be located in the keys folder, the person that generated it will then give it to the other members of the chat, and they will need to place it in their keys folder.

Usage:
To start server: `python3 server/main.py`
To generate key: `python3 client/main.py --genkey <chat-name>`
To send message: `python3 client/main.py --send <chat-name> <message>`
To read a chat: `python3 cient/main.py --read <chat-name>`

We can't wait to see what YOU can come up with,
Fizz Org. Dev. Team
