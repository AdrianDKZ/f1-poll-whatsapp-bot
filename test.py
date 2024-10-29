from neonize.client import NewClient
from neonize.events import ConnectedEv, MessageEv, PairStatusEv, event
from neonize.types import MessageServerID
from datetime import timedelta

from commands import INDEXER

client = NewClient("database.sqlite3")

@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    print("⚡ Connected")

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    handler(client, message)

# Define your custom message handler function
def handler(client: NewClient, message: MessageEv):
    print(message)
    message_source = message.Info.MessageSource
    ## Secure we are in a group and its ID is the correct one
    if message_source.IsGroup and message_source.Chat.User == "120363349774885451": #120363021965478012
        ## Retrieve messahe
        text = message.Message.conversation or message.Message.extendedTextMessage.text
        ## Commands will start by #
        if text[0] == "#":
            ## Get sender ID
            user = message_source.Sender.User
            ## Split text in lines and remove empty ones
            text = list(filter(lambda x: x != "", text.lower().split("\n")))
            print(text)
            comando = text[0].split(" ")[0]
            if comando not in INDEXER.keys():
                comando = "#ayuda"
            client.reply_message(INDEXER[comando](text, user), message)
            


    # # print(message.Info.MessageSource.Sender.User)
    # chat = message.Info.MessageSource.Chat

    # # Example scenarios
    # if text == "ping":
    #     client.reply_message("pong", message)
    # elif text == "_sticker":
    #     client.send_sticker("sticker_url_here")

# Add more scenarios as needed...

# Connect to WhatsApp
client.connect()
