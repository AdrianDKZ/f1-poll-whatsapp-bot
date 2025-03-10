CHAT_ID = "120363021965478012" ### GRUPO
## ID Grupo: "120363021965478012" ### GRUPO
## ID Pruebas: "120363349774885451" ### PRUEBAS
    
PILOTS = {
    ## RedBull
    "VER": ["max", "verstappen", "ver", "mierdstappen"],
    "LAW": ["liam", "lawson", "law"],
    ## Mclaren
    "NOR": ["lando", "norris", "nor"],
    "PIA": ["oscar", "piastri", "pia"],
    ## Ferrari
    "HAM": ["lewis", "hamilton", "ham"],
    "LEC": ["charles", "leclerc", "lec"],
    ## Mercedes
    "RUS": ["george", "russell", "rus"],
    "ANT": ["kimi", "antonelli", "ant"],
    ## Aston Martin
    "ALO": ["fernando", "alonso", "alo", "nano", "magic"],
    "STR": ["lance", "stroll", "str"],
    ## Alpine
    "GAS": ["pierre", "gasly", "gas"],
    "DOO": ["jack", "doohan", "doo"],
    "COL": ["franco", "colapinto", "col"],
    ## Williams
    "SAI": ["carlos", "sainz", "sai"],
    "ALB": ["alexander", "albon", "alb"],
    ## Haas
    "OCO": ["esteban", "ocon", "oco"],
    "BEA": ["oliver", "bearman", "bea"],
    ## Sauber    
    "HUL": ["nico", "hulkenberg", "hul"],
    "BOR": ["gabriel", "bortoleto", "bor"],
    ## Racing Bulls
    "TSU": ["yuki", "tsunoda", "tsu"],
    "HAD": ["isack", "hadjar", "had"],
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