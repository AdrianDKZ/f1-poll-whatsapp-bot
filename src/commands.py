import re

from neonize.client import NewClient
from neonize.events import MessageEv

import constants, commit_database, utils

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

    def send(self, message):
        self.client.send_message(utils.build_msg(), message)

def show_help(msg: MessageObj):
    msg.reply("!Comandos _whatsapp-milf-bot_:" 
            + "\n\t*#Ayuda* - Comandos del bot"
            + "\n\t*#Tips* - Funcionamiento del bot"
            + "\n\t*#Horario* - Horarios del GP actual"
            + "\n\t*#Clasificacion* - Clasificación de la porra"
            + "\n\t*#SQualy* - Indica tus predicciones para la clasificación sprint"
            + "\n\t*#Sprint* - Indica tus predicciones para la carrera sprint"
            + "\n\t*#Qualy*  - Indica tus predicciones para la clasificación"
            + "\n\t*#Carrera* - Indica tus predicciones para la carrera"
            + f"\n\t*#Resultado _{constants.SESSIONS_STR}_* - Guarda los resultados de la sesión indicada"
            + f"\n\t*#Plantilla _{constants.SESSIONS_STR}_* - Obtiene la plantilla de la sesión indicada"
            + f"\n\t*#Porra _{constants.SESSIONS_STR}_* - Muestra las predicciones de la sesión indicada")
    
def show_tips(msg: MessageObj):
    msg.reply("!Funcionamiento de _whatsapp-milf-bot_:"
            + "\n\t - El bot *solo* detecta los mensajes que empiezan por *#*"
            + "\n\t - Las plantillas se envían con una *!* delante. *Hay que borrarla*."
            + "\n\t - El bot responde a *todos* los mensajes. *Comprueba la #*."
            + "\n\t - Las semanas de GP comienzan el *martes* y terminan el *lunes* (incluidos)."
            + "\n\t - Los martes a las 9.30h se envían automáticamente los horarios del GP."
            + "\n\t - Al comienzo de la sesión ya no se admiten más predicciones."
            + "\n\t - Al comienzo de cada sesión se envían automáticamente todas las predicciones hechas."
            + "\n\t - El bot detecta qué persona ha mandado la predicción."
            + "\n\t - Para los comandos _#resultado_ y _#plantilla_ se necesita indicar la sesión."
            + "\n\t - Las sesiones se indentifican como _squaly_, _sprint_, _qualy_ y _carrera_.")

def show_times(msg: MessageObj):
    times_info = commit_database.obtain_times()
    if utils.isError(times_info):
        msg.reply(times_info)
    else:
        msg.reply(format_times(times_info))   

def show_class(msg: MessageObj):
    msg.reply(commit_database.poll_points())
    msg.reply(commit_database.team_points())

def show_template(msg: MessageObj):
    if msg.subcommand in constants.TEMPLATE.keys():
        template = f"!#{msg.subcommand.capitalize()}\n{constants.TEMPLATE[msg.subcommand]}"
    else:
        template = f"!Indica *#Plantilla {constants.SESSIONS_STR}* para obtener la plantilla de la sesión deseada"
    msg.reply(template)

def show_preds(msg: MessageObj):
    if msg.subcommand not in constants.SESSIONS:
        msg.reply(constants.ERRORS["subcmd"])
    msg.reply(commit_database.obtain_polls(msg.subcommand))

def set_poll(msg: MessageObj):
    ## Check if results command is properly executed
    if msg.command == "resultado" and msg.subcommand not in constants.SESSIONS:
        msg.reply(constants.ERRORS["subcmd"] + f"\nEjecuta *#Plantilla {constants.SESSIONS_STR}* para obtener la plantilla de la sesión deseada.")
        return
    
    ## Parse prediction and finish if error
    session = msg.subcommand if msg.command == "resultado" else msg.command
    prediction = parse_prediction(msg.input, session)
    if utils.isError(prediction):
        msg.reply(prediction)
        if "formato" in prediction:
            subcommand = "" if msg.subcommand == None else session
            msg.send(f"!#{msg.command.capitalize()} {subcommand}\n{constants.TEMPLATE[session]}")
        return
    
    if msg.command == "resultado":
        msg.reply(commit_database.prediction_points(prediction, session))
        msg.send(commit_database.poll_points())
        msg.send(commit_database.team_points())
    else:
        msg.reply(commit_database.store_poll(prediction, session, msg.user))

def format_times(times_info):
    ## GP_Name + [session_name: session_date session_time]
    return (f"*!{times_info[0]}*\n" + 
                "\n".join(f"{session[3].capitalize()}: _{utils.dt_to_msg(session[2])}_" for session in times_info[1]))

def parse_prediction(msg: list, session: str):
    ## Parse lines to obtain prediction
    prediction = {}
    for line in msg:
        try:
            ## Split lines by hyphon to obtain POSITION - PILOT or ALO - POSITION
            line_info = line.replace(" ", "").split("-")
            ## Process ALO position deleting possible strings
            if "alo" in line_info[0]:
                prediction["ALO"] = re.sub("[a-zA-Z]+", "", line_info[1])
            else:
                ## Loop pilots till find the indicated
                isPilot = False
                for pilot_id, pilot_names in constants.PILOTS.items():
                    if line_info[1] in pilot_names:
                        isPilot = True
                        break
                ## If pilot not found, display pilot error
                if not isPilot:
                    return f"!Piloto *_{line_info[1]}_* no encontrado"
                prediction[line_info[0]] = pilot_id
        ## If any other error, display processing error
        except Exception as e:
            return f"!Error procesando la predicción. Usa el siguiente formato:"
    ## Check the obtained elements are equals to the indicated on the session template    
    session_template = constants.TEMPLATE[session].replace("- ", "").split("\n")
    if sorted(session_template) != sorted(prediction.keys()):
        return f"!Plantilla incorrecta. Usa el siguiente formato:"
    ## Return parsed prediction
    return prediction

INDEXER = {
    "ayuda": show_help,
    "tips": show_tips,
    "horario": show_times,
    "qualy": set_poll,
    "carrera": set_poll,
    "sprint": set_poll,
    "squaly": set_poll,
    "resultado": set_poll,
    "plantilla": show_template,
    "porra": show_preds,
    "clasificacion": show_class
}