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
    cursor.execute("SELECT * FROM sessions WHERE gp_id = ? AND type = ? AND datetime > ?", 
                   (gp_id, session_type, now.strftime('%Y-%m-%d %H:%M:%S')))
    return cursor.fetchone()

def all_sessions(gp_id):
    cursor.execute("SELECT * FROM sessions WHERE gp_id = ?", (gp_id,))
    return cursor.fetchall()

def store_results(prediction, session_id):
    cursor.execute("UPDATE sessions SET result = ? WHERE id = ?", (json.dumps(prediction), session_id))
    conn.commit()

def obtain_user(user):
    ## Identify user in DB and insert it if not exists
    cursor.execute("SELECT * FROM users WHERE telephone = ?", (user,))
    user_id = cursor.fetchone()
    if not user_id:
        cursor.execute("INSERT INTO users (telephone) VALUES (?)", (user,))
        conn.commit()
    return cursor.lastrowid if not user_id else user_id[0]

def common_checks(session, get_session):
    connect_sql()
    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return "!No se ha encontrado ningun GP activo a fecha de hoy"
    session_id = get_session(gp_id[0], session)
    if not session_id:
        return "!La sesión indicada no se encuentra"
    return session_id[0]

def store_poll(prediction, session, user):
    session_id = common_checks(session, current_session)
    if isinstance(session_id, str):
        return session_id
    
    user_id = obtain_user(user)

    ## Check if entry for user and session exists
    cursor.execute("SELECT * FROM predictions WHERE session_id = ? AND user_id = ?", (session_id, user_id))
    db_entry = cursor.fetchone()
    if not db_entry:
        cursor.execute("INSERT INTO predictions (session_id, user_id, prediction) VALUES (?, ?, ?)",
                (session_id, user_id, json.dumps(prediction)))
    else:
        cursor.execute("UPDATE predictions SET prediction = ? WHERE id = ?", (json.dumps(prediction), db_entry[0]))
    conn.commit()
    return "!Predicción actualizada" if db_entry else "!Prediccion guardada"

def prediction_points(results, session):
    session_id = common_checks(session, gp_session)
    if isinstance(session_id, str):
        return session_id   
    ## Store session results
    store_results(results, session_id)
    ## Obtain all predictions made for session
    cursor.execute("SELECT * FROM predictions WHERE session_id = ?", (session_id, ))
    resultados = "*Puntos obtenidos*"
    for prediction in cursor.fetchall():
        ## Obtain user points and strikes
        points, strike = get_points(prediction[3], results, session)
        ## Get previous points if result had already been indicated
        prev_points = 0 if prediction[4] == None else prediction[4]
        prev_strike = 1 if prev_points >= 5 else 0
        ## Update prediction points
        cursor.execute("UPDATE predictions SET points = ? WHERE id = ?", (points, prediction[0]))
        ## Obtain historical points and strikes
        cursor.execute("SELECT * FROM users WHERE id = ?", (prediction[2],))
        user_info = cursor.fetchone()
        ## Update total points and strikes. Obtained points + Total points - Previous session points (normally this will be 0)
        cursor.execute("UPDATE users SET points = ?, strikes = ? WHERE id = ?", (points+user_info[2]-prev_points, strike+user_info[3]-prev_strike, prediction[2]))
        resultados += f"\n@{user_info[1]}: {points} pts."
    conn.commit()
    return resultados      

def poll_points():
    connect_sql()
    cursor.execute("SELECT * FROM users")
    users_lst = sorted(cursor.fetchall(), key=lambda x: (-x[2], -x[3]))
    return "*Porra Individual*\n" + "\n".join(f"@{user[1]} - {user[2]} puntos ({user[3]})" for user in users_lst)

def obtain_times():
    connect_sql()
    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return constants.ERRORS["GP"]
    sessions = all_sessions(gp_id[0])

    format_datetime = lambda date: datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%A %d, %H:%M').capitalize()

    ## GP_Name + [session_name: session_date session_time]
    return (f"*{gp_id[1]}*\n" + 
            "\n".join(f"{session[3].capitalize()}: _{format_datetime(session[2])}_" for session in sessions))   

def get_points(prediction, results, session):
    ## Strike is a boolean int, so it can be added outside the function
    points, strike = 0, 1
    prediction = json.loads(prediction)
    for position, pilot in results.items():
        ## Add point if hit
        if prediction[position] == pilot:
            points += 1
        ## Strike to false if fail at a numeric position or not a race
        elif position != "ALO" or session != "carrera":
            strike = 0
    ## Two extra points if strike
    points += 2 if strike else 0
    return points, strike
