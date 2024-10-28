from database import process_poll

def show_help(msg: list, user: str):
    return ("Comandos whatsapp-milf-bot:" 
            + "\n\t#Ayuda \n\t#Horario \n\t#Qualy \n\t#SQualy \n\t#Carrera \n\t#Sprint \n\t#Resultado"
            + "\nPara obtener la plantilla de los comandos qualy, squaly, carrera o sprint escribe #sesion plantilla")

def show_times(msg: list, user: str):
    pass

def set_qualy(msg: list, user: str):
    if "plantilla" in msg[0]:
        return "!#Qualy \nPole- \nALO-"
    process_poll(msg[1:], "qualy", user)

def set_race(msg: list, user: str):
    if "plantilla" in msg[0]:
        return "!#Carrera \n1- \n2- \n3- \nALO-"
    process_poll(msg[1:], "race", user)

def set_sprint(msg: list, user: str):
    if "plantilla" in msg[0]:
        return "!#Sprint \n1-"
    process_poll(msg[1:], "sprint", user)

def set_squaly(msg: list, user: str):
    if "plantilla" in msg[0]:
        return "!#SQualy \n1-"
    process_poll(msg[1:], "squaly", user)

def set_results(msg: list, user: str):
    pass

INDEXER = {
    "#ayuda": show_help,
    "#horario": show_times,
    "#qualy": set_qualy,
    "#carrera": set_race,
    "#sprint": set_sprint,
    "#squaly": set_squaly,
    "#resultado": set_results
}