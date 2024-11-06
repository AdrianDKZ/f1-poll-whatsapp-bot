import sqlite3, json, datetime
import locale

import constants

# Set the Spanish locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def connect_sql():
    global conn, cursor
    conn = sqlite3.connect('database/Porra2024.sqlite3')
    cursor = conn.cursor()

def current_gp():
    today = datetime.date.today()
    cursor.execute("SELECT * FROM gp WHERE date_start <= ? AND date_finish >= ?", (today, today))
    return cursor.fetchone()

def gp_session(gp_id, session_type):
    cursor.execute("SELECT * FROM sessions WHERE gp_id = ? AND type = ?", (gp_id, session_type))
    return cursor.fetchone()

def current_session(gp_id, session_type):
    now = datetime.datetime.now()
    cursor.execute("SELECT * FROM sessions WHERE gp_id = ? AND type = ? AND date <= ? AND time < ?", 
                   (gp_id, session_type, now.date(), now.time()))
    return cursor.fetchone()

def all_sessions(gp_id):
    cursor.execute("SELECT * FROM sessions WHERE gp_id = ?", (gp_id,))
    return cursor.fetchall()

def store_poll(prediction, session, user):
    connect_sql()
    ## Identify user in DB and insert it if not exists
    cursor.execute("SELECT * FROM users WHERE telephone = ?", (user,))
    user_id = cursor.fetchone()
    if not user_id:
        cursor.execute("INSERT INTO users (telephone) VALUES (?)", (user,))
        conn.commit()
    user_id = cursor.lastrowid if not user_id else user_id[0]

    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return constants.ERRORS["GP"]
    session_id = current_session(gp_id[0], session)
    if not session_id:
        return "!La sesión indicada no se ha encontrado o ha comenzado ya"
    
    ## Check if entry for user and session exists
    cursor.execute("SELECT * FROM predictions WHERE session_id = ? AND user_id = ?", (session_id[0], user_id))
    db_entry = cursor.fetchone()

    if not db_entry:
        cursor.execute("INSERT INTO predictions (session_id, user_id, prediction) VALUES (?, ?, ?)",
                (session_id[0], user_id, json.dumps(prediction)))
    else:
        cursor.execute("UPDATE predictions SET prediction = ? WHERE id = ?", (json.dumps(prediction), db_entry[0]))
    conn.commit()
    return "!Predicción actualizada" if db_entry else "!Prediccion guardada"
   
def store_results(prediction, session):
    connect_sql()

    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return constants.ERRORS["GP"]
    session_id = gp_session(gp_id[0], session)
    if not session_id:
        return "!La sesión indicada no se encuentra"
    
    cursor.execute("UPDATE sessions SET result = ? WHERE id = ?", (json.dumps(prediction), session_id[0]))
    conn.commit()

    return "!Resultados guardados"


def obtain_times():
    connect_sql()
    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return constants.ERRORS["GP"]
    sessions = all_sessions(gp_id[0])

    format_date = lambda date: datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A %d').capitalize()
    format_time = lambda time: datetime.datetime.strptime(time, '%H:%M:%S').strftime('%H:%M')

    ## GP_Name + [session_name: session_date session_time]
    return (f"{gp_id[1]}\n" + 
            "\n".join(f"*{session[4].capitalize()}*: _{format_date(session[2])} {format_time(session[3])}_" for session in sessions))   
