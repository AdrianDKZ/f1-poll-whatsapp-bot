import re

from info import PILOTS

def show_help(msg: list, user: str):
    return ("!Comandos whatsapp-milf-bot:" 
            + "\n\t#Ayuda \n\t#Horario \n\t#Qualy \n\t#SQualy \n\t#Carrera "
            + "\n\t#Sprint \n\t#Resultado \n\t#Plantilla [qualy, carrera, sprint, squaly]")

def show_times(msg: list, user: str):
    pass

def show_template(msg: list, user: str):
    if "qualy" in msg[0]:
        return "!#Qualy \nPole- \nALO-"
    elif "carrera" in msg[0]:
        return "!#Carrera \n1- \n2- \n3- \nALO-"
    elif "sprint" in msg[0]:
        return "!#Sprint \n1-"
    elif "squaly" in msg[0]:
        return "!#SQualy \n1-"
    else:
        return "!Indica *#Plantilla [qualy, carrera, sprint, squaly]* para obtener la plantilla de la sesión deseada"

def set_poll(msg: list, user: str):
    session = msg[0].replace("#","")

    pred_dict = {}
    for prediction in msg[1:]:
        try:
            pred_info = prediction.split("-")
            if "alo" in pred_info[0]:
                pred_dict["ALO"] = int(re.sub("[a-zA-Z]+", "", pred_info[1]))
            else:
                pred_dict[pred_info[0]] = next((pilot_id for pilot_id, pilot_names in PILOTS.items() if pred_info[1].replace(" ", "") in pilot_names))
        except (StopIteration, ValueError):
            return f"!Error en el procesamiento de _{prediction}_"
    ## TBD: procesamiento y guardado de los datos
    return "!Predicción guardada"#: \n" + '\n'.join(f"{key}- {pred_dict[key]}" for key in sorted(pred_dict.keys())) futuro formato para imprimir predicciones

def set_results(msg: list, user: str):
    pass

INDEXER = {
    "#ayuda": show_help,
    "#horario": show_times,
    "#qualy": set_poll,
    "#carrera": set_poll,
    "#sprint": set_poll,
    "#squaly": set_poll,
    "#resultado": set_results,
    "#plantilla": show_template
}