CHAT_ID = "120363021965478012" ### GRUPO  
## ID Pruebas: "120363349774885451" 
## ID Grupo:"120363021965478012"

DB_PATH = 'database/Porra2024.sqlite3'
## Grupo: 'database/Porra2024.sqlite3'
## Pruebas: 'database/Porra2024_test.sqlite3'
    
PILOTS = {
    "HAM": ["lewis", "hamilton", "ham"],
    "RUS": ["george", "russell", "rus"],
    "VER": ["max", "verstappen", "ver", "mierdstapen"],
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

TEMPLATE = {
    "squaly":  "1- ",
    "sprint":  "1- ",
    "qualy":   "1- \nALO- ",
    "carrera": "1- \n2- \n3- \nALO- "    
}

SESSIONS = ["squaly", "sprint", "qualy", "carrera"]
SESSIONS_STR = '[' + ', '.join(SESSIONS) + ']'

ERRORS = {
    "NoGP": "!No se ha encontrado ningun GP activo en la fecha de hoy",
    "NoSession": "!La sesión indicada no se encuentra",
    "subcmd": f"!El comando indicado requiere indicar la sesión: _{SESSIONS_STR}_"
}