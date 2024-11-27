import sqlite3, json, datetime
import locale

import constants

# Set the Spanish locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def connect_sql():
    global conn, cursor
    conn = sqlite3.connect(constants.DB_PATH)
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

def session_predictions(session_id):
    cursor.execute("SELECT * FROM predictions WHERE session_id = ?", (session_id, ))
    return cursor.fetchall()

def store_results(prediction, session_id):
    cursor.execute("UPDATE sessions SET result = ? WHERE id = ?", (json.dumps(prediction), session_id))
    conn.commit()

def store_user(telephone, user_name):
    connect_sql()
    if not obtain_user(telephone):
        user_name = f"@{telephone}" if user_name == "" else user_name.split(" ")[0]
        cursor.execute("INSERT INTO users (telephone, name) VALUES (?, ?)", (telephone, user_name))
        conn.commit()

def obtain_user(user):
    ## Identify user in DB and insert it if not exists
    cursor.execute("SELECT * FROM users WHERE telephone = ?", (user,))
    return cursor.fetchone()

def common_checks(session, get_session):
    connect_sql()
    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return constants.ERRORS["NoGP"]
    session_id = get_session(gp_id[0], session)
    if not session_id:
        return constants.ERRORS["NoSession"]
    return session_id[0]

def store_poll(prediction, session, user):
    session_id = common_checks(session, current_session)
    if isinstance(session_id, str):
        return session_id
    
    user_id = obtain_user(user)[0]

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

def obtain_polls(session):
    connect_sql()
    session_id = common_checks(session, current_session) if isinstance(session, str) else session
    ## Obtain session info
    cursor.execute("SELECT gp_id, type FROM sessions WHERE id = ?", (session_id,))
    gp_id, session_type = cursor.fetchone()
    cursor.execute("SELECT name FROM gp WHERE id = ?", (gp_id,))
    gp_name = cursor.fetchone()[0]
    preds_str = f"*!{gp_name}* \n _{session_type.capitalize()}_"
    for prediction in session_predictions(session_id):
        user = obtain_user(prediction[2])
        pred = json.loads(prediction[3])
        user_pred_str = "\n".join(f"{position}- {pilot}" for position, pilot in pred.items())
        preds_str += f"\n\n{user[1]}:\n{user_pred_str}"
    return preds_str

def prediction_points(results, session):
    session_id = common_checks(session, gp_session)
    if isinstance(session_id, str):
        return session_id   
    ## Store session results
    store_results(results, session_id)
    ## Obtain all predictions made for session
    resultados = "*Puntos obtenidos*"
    for prediction in session_predictions(session_id):
        ## Obtain user points and strikes
        points, strike = get_points(prediction[3], results, session)
        ## Get previous points if result had already been indicated
        prev_points = 0 if prediction[4] == None else prediction[4]
        prev_strike = 1 if prev_points >= 5 else 0
        ## Update prediction points
        cursor.execute("UPDATE predictions SET points = ? WHERE id = ?", (points, prediction[0]))
        ## Obtain historical points and strikes
        user_info = obtain_user(prediction[2])
        ## Update total points and strikes. Obtained points + Total points - Previous session points (normally this will be 0)
        cursor.execute("UPDATE users SET points = ?, strikes = ? WHERE telephone = ?", (points+user_info[2]-prev_points, strike+user_info[3]-prev_strike, prediction[2]))
        resultados += f"\n{user_info[1]}: {points} pts."
    conn.commit()
    return resultados      

def poll_points():
    connect_sql()
    cursor.execute("SELECT * FROM users")
    users_lst = sorted(cursor.fetchall(), key=lambda x: (-x[2], -x[3]))
    return "*Porra Individual*\n" + "\n".join(f"{user[1]} - {user[2]} puntos ({user[3]})" for user in users_lst)

def team_points():
    connect_sql()
    cursor.execute("SELECT * FROM teams")
    teams_info = []
    for team in cursor.fetchall():
        user1, user2 = obtain_user(team[2]), obtain_user(team[3])
        teams_info.append((team[1], user1[1], user2[1], user1[2]+user2[2], user1[3]+user2[3]))
    teams_info = sorted(teams_info, key=lambda x: (-x[3], -x[4]))
    return "*Porra por Equipos*\n" + "\n".join(f"{team[0]} ({team[1]} y {team[2]}) - {team[3]} puntos ({team[4]})" for team in teams_info)

def obtain_times():
    connect_sql()
    ## Get current Grand Prix and the GP Session
    gp_id = current_gp()
    if not gp_id:
        return constants.ERRORS["NoGP"]
    sessions = all_sessions(gp_id[0])
    return gp_id[1], sessions

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
