import re

from neonize.client import NewClient
from neonize.events import MessageEv

import constants
import commit_database

class MessageObj():
    def __init__(self, client: NewClient, message: MessageEv, user, text):
        self.client = client
        self.user = user
        self.message = message

        ## Convert text to lowercase, split by line and delete empty ones
        text = list(filter(lambda x: x != "", text.lower().split("\n")))
        ## Rest of the text as important part of message
        self.input = text[1:]
        ## Obtain command and subcommand if exists. If not correct, invoke help function
        full_command = text[0].split(" ")
        self.command = full_command[0][1:] if full_command[0][1:] in INDEXER.keys() else "ayuda"
        self.subcommand = full_command[1] if len(full_command) > 1 else None

    def reply(self, response):
        self.client.reply_message(response, self.message)


def show_help(msg: MessageObj):
    msg.reply("!Comandos whatsapp-milf-bot:" 
            + "\n\t#Ayuda \n\t#Horario \n\t#Qualy \n\t#SQualy \n\t#Carrera \n\t#Sprint"
            + f"\n\t#Resultado {constants.SESSIONS_STR} \n\t#Plantilla {constants.SESSIONS_STR}")

def show_times(msg: MessageObj):
    msg.reply(commit_database.obtain_times())

def show_template(msg: MessageObj):
    if "qualy" in msg.subcommand:
        template = "!#Qualy \nPole- \nALO-"
    elif "carrera" in msg.subcommand:
        template = "!#Carrera \n1- \n2- \n3- \nALO-"
    elif "sprint" in msg.subcommand:
        template = "!#Sprint \n1-"
    elif "squaly" in msg.subcommand:
        template = "!#SQualy \n1-"
    else:
        template = f"!Indica *#Plantilla {constants.SESSIONS_STR}* para obtener la plantilla de la sesión deseada"
    msg.reply(template)

def set_poll(msg: MessageObj):
    ## Check if results command is properly executed
    if msg.command == "resultados" and msg.subcommand not in constants.SESSIONS:
        msg.reply(f"!Recuerda indicar la sesión deseada de la siguiente forma: *#Resultado {constants.SESSIONS_STR}*"
                  + f"\nEjecuta *#Plantilla {constants.SESSIONS_STR}* para obtener la plantilla de la sesión deseada.")
        return
    
    ## Parse prediction and finish if error
    prediction = parse_prediction(msg.input)
    if isinstance(prediction, str):
        msg.reply(prediction)
        return
    
    if msg.command == "resultado":
        msg.reply(commit_database.store_results(prediction, msg.subcommand))
        ## Necesitamos otro comando con el que emviar un mensaje con los resultados de la prediccion
        ## Ademas, otro mas con los resultados actualizados de la clasificacion general
    else:
        msg.reply(commit_database.store_poll(prediction, msg.command, msg.user))

#: \n" + '\n'.join(f"{key}- {pred_dict[key]}" for key in sorted(pred_dict.keys())) futuro formato para imprimir predicciones

def parse_prediction(msg: list):
    pred_dict = {}
    for prediction in msg:
        try:
            pred_info = prediction.split("-")
            if "alo" in pred_info[0]:
                pred_dict["ALO"] = int(re.sub("[a-zA-Z]+", "", pred_info[1]))
            else:
                pred_dict[pred_info[0]] = next((pilot_id for pilot_id, pilot_names in constants.PILOTS.items() if pred_info[1].replace(" ", "") in pilot_names))
        except (StopIteration, ValueError):
            return f"!Error en el procesamiento de _{prediction}_"
    return pred_dict

INDEXER = {
    "ayuda": show_help,
    "horario": show_times,
    "qualy": set_poll,
    "carrera": set_poll,
    "sprint": set_poll,
    "squaly": set_poll,
    "resultado": set_poll,
    "plantilla": show_template
}