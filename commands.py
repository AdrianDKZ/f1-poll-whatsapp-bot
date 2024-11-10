import re

from neonize.client import NewClient
from neonize.events import MessageEv

import constants
import commit_database

class MessageObj():
    def __init__(self, client: NewClient, message: MessageEv, chat, user, text):
        self.client = client
        self.user = user
        self.message = message
        self.chat = chat

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

    def send(self, message):
        self.client.send_message(self.chat, message)

def show_help(msg: MessageObj):
    msg.reply("!Comandos whatsapp-milf-bot:" 
            + "\n\t*#Ayuda* - Comandos del bot"
            + "\n\t*#Horario* - Horarios del GP actual"
            + "\n\t*#Porra* - Clasificación de la porra"
            + "\n\t*#SQualy* - Indica tus predicciones para la clasificación sprint"
            + "\n\t*#Sprint* - Indica tus predicciones para la carrera sprint"
            + "\n\t*#Qualy*  - Indica tus predicciones para la clasificación"
            + "\n\t*#Carrera* - Indica tus predicciones para la carrera"
            + f"\n\t*#Resultado _{constants.SESSIONS_STR}_* - Guarda los resultados de la sesión indicada"
            + f"\n\t*#Plantilla _{constants.SESSIONS_STR}_* - Obtiene la plantilla de la sesión indicada")

def show_times(msg: MessageObj):
    msg.reply(commit_database.obtain_times())

def show_poll(msg: MessageObj):
    msg.reply(commit_database.poll_points())
    msg.reply(commit_database.team_points())

def show_template(msg: MessageObj):
    if msg.subcommand in constants.TEMPLATE.keys():
        template = f"!#{msg.subcommand.capitalize()}\n{constants.TEMPLATE[msg.subcommand]}"
    else:
        template = f"!Indica *#Plantilla {constants.SESSIONS_STR}* para obtener la plantilla de la sesión deseada"
    msg.reply(template)

def set_poll(msg: MessageObj):
    ## Check if results command is properly executed
    if msg.command == "resultado" and msg.subcommand not in constants.SESSIONS:
        msg.reply(f"!Recuerda indicar la sesión deseada de la siguiente forma: *#Resultado {constants.SESSIONS_STR}*"
                  + f"\nEjecuta *#Plantilla {constants.SESSIONS_STR}* para obtener la plantilla de la sesión deseada.")
        return
    
    ## Parse prediction and finish if error
    session = msg.subcommand if msg.command == "resultado" else msg.command
    prediction = parse_prediction(msg.input, session)
    if isinstance(prediction, str):
        msg.reply(prediction)
        if prediction.startswith("!Plantilla"):
            msg.send(f"!#{msg.command.capitalize()}\n{constants.TEMPLATE[msg.command]}")
        return
    
    if msg.command == "resultado":
        msg.reply(commit_database.prediction_points(prediction, session))
        msg.send(commit_database.poll_points())
        msg.send(commit_database.team_points())
    else:
        msg.reply(commit_database.store_poll(prediction, session, msg.user))

def parse_prediction(msg: list, session: str):
    ## Parse lines to obtain prediction
    prediction = {}
    for line in msg:
        try:
            line_info = line.split("-")
            if "alo" in line_info[0]:
                prediction["ALO"] = re.sub("[a-zA-Z]+", "", line_info[1]).replace(" ", "")
            else:
                prediction[line_info[0]] = next((pilot_id for pilot_id, pilot_names in constants.PILOTS.items() if line_info[1].replace(" ", "") in pilot_names))
        except (StopIteration, ValueError):
            return f"!Error en el procesamiento de _{line}_"
    ## Check the obtained elements are equals to the indicated on the session template    
    session_template = constants.TEMPLATE[session].replace("- ", "").split("\n")
    if sorted(session_template) != sorted(prediction.keys()):
        return f"!Plantilla incorrecta. Usa el siguiente formato:"
    ## Return parsed prediction
    return prediction

INDEXER = {
    "ayuda": show_help,
    "horario": show_times,
    "qualy": set_poll,
    "carrera": set_poll,
    "sprint": set_poll,
    "squaly": set_poll,
    "resultado": set_poll,
    "plantilla": show_template,
    "porra": show_poll
}