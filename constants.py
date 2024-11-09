
PILOTS = {
    "HAM": ["lewis", "hamilton", "ham"],
    "RUS": ["george", "russell", "rus"],
    "VER": ["max", "verstappen", "ver"],
    "PER": ["sergio", "perez", "per"],
    "LEC": ["charles", "leclerc", "lec"],
    "SAI": ["carlos", "sainz", "sai"],
    "NOR": ["lando", "norris", "nor"],
    "PIA": ["oscar", "piastri", "pia"],
    "OCO": ["esteban", "ocon", "oco"],
    "GAS": ["pierre", "gasly", "gas"],
    "ALB": ["alexander", "albon", "alb"],
    "COL": ["franco", "colapinto", "col"],
    "TSU": ["yuki", "tsunoda", "tsu"],
    "LAW": ["liam", "lawson", "law"],
    "ZHO": ["guanyu", "zhou", "zho"],
    "BOT": ["valtteri", "bottas", "bot"],
    "ALO": ["fernando", "alonso", "alo", "nano", "magic"],
    "STR": ["lance", "stroll", "str"],
    "HUL": ["nico", "hulkenberg", "hul"],
    "MAG": ["kevin", "magunussen", "mag"]
}

ERRORS = {
    "GP404": "!No se ha encontrado ningun GP activo en la fecha de hoy",
    "SES404": "!La sesión indicada no se encuentra"
}

TEMPLATE = {
    "squaly":  "1- ",
    "sprint":  "1- ",
    "qualy":   "1- \nALO- ",
    "carrera": "1- \n2- \n3- \nALO- "    
}

SESSIONS = ["qualy", "carrera", "sprint", "squaly"]
SESSIONS_STR = '[' + ', '.join(SESSIONS) + ']'