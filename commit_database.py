import sqlite3, json, datetime

# Conecta a la base de datos
conn = sqlite3.connect('database/Porra2024.sqlite3')
cursor = conn.cursor()

def current_gp():
    today = datetime.date.today()
    cursor.execute("SELECT * FROM gp WHERE fecha_inicio <= ? AND fecha_fin >= ?", (today, today))
    gp = cursor.fetchone()
    return gp[0] if gp else False

def current_session(gp_id, session_type):
    cursor.execute("SELECT * FROM sesiones WHERE gp_id = ? AND tipo = ?", (gp_id, session_type))
    session = cursor.fetchone()
    return session[0] if session else False


def store_poll(prediction, session, user):
    ## Identify user in DB and insert it if not exists
    cursor.execute("SELECT * FROM usuarios WHERE telefono = ?", (user,))
    user_id = cursor.fetchone()
    if not user_id:
        cursor.execute("INSERT INTO usuarios (telefono) VALUES (?)", (user,))
    user_id = cursor.lastrowid if not user_id else user_id[0]

    cursor.execute("INSERT INTO predicciones (sesion, usuario_id, prediccion) VALUES (?, ?, ?)",
               (session, user, json.dumps(prediction)))
    conn.commit()


x = current_gp()
current_session(x, "qualy")