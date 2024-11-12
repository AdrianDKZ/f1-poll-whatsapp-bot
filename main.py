from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv, event
from neonize.types import MessageServerID

from commands import INDEXER, MessageObj
from constants import CHAT_ID
from commit_database import store_user
from schedule import schedule_runner

import threading

client = NewClient("database.sqlite3")

@client.event(ConnectedEv)
def on_connected(newClient: NewClient, __: ConnectedEv):
    print("⚡ Connected")
    thread = threading.Thread(target=schedule_runner, args=(newClient,))
    thread.daemon = True
    thread.start()

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    print(message)
    message_source = message.Info.MessageSource
    ## Secure we are in a group and its ID is the correct one
    if message_source.IsGroup and message_source.Chat.User == CHAT_ID:
        ## Retrieve message
        text = message.Message.conversation or message.Message.extendedTextMessage.text
        ## Commands will start by #
        if text[0] == "#":
            ## Get sender ID
            user = message_source.Sender.User
            store_user(user, message.Info.Pushname)
            info = MessageObj(client, message, user, text)
            INDEXER[info.command](info)
            
client.connect()
    # # print(message.Info.MessageSource.Sender.User)
    # chat = message.Info.MessageSource.Chat

    # # Example scenarios
    # if text == "ping":
    #     client.reply_message("pong", message)
    # elif text == "_sticker":
    #     client.send_sticker("sticker_url_here")

# Add more scenarios as needed...

# Connect to WhatsApp

