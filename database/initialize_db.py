import sqlite3

# Conecta a la base de datos
conn = sqlite3.connect('database/Porra2024.sqlite3')
cursor = conn.cursor()

# Crea la tabla gp
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gp (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        date_start DATE NOT NULL,
        date_finish DATE NOT NULL
    );
""")

# Crea la tabla sesiones
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        gp_id INTEGER NOT NULL,
        datetime DATETIME NOT NULL,
        type TEXT NOT NULL CHECK (type IN ('libres', 'sprint', 'squaly', 'qualy', 'carrera')),
        result TEXT,
        FOREIGN KEY (gp_id) REFERENCES gp(id)
    );
""")
## Necesitamos una columna mas con los resultados de la sesion

# Crea la tabla usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        telephone TEXT NOT NULL,
        points INTEGER DEFAULT 0 NOT NULL,
        strikes INTEGER DEFAULT 0 NOT NULL
    );
""")

# Crea la tabla predicciones
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY,
        session_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        prediction TEXT NOT NULL,
        points INTEGER DEFAULT 0,
        stored INTEGER DEFAULT 0 CHECK(stored IN (0, 1)),
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
""")
## stored: boolean type. to be used only with 0 or 1

# Inserta un nuevo GP
cursor.execute("INSERT INTO gp (name, date_start, date_finish) VALUES ('Gran Premio de Pasadolandia', '2024-04-12', '2024-04-14')")
cursor.execute("INSERT INTO gp (name, date_start, date_finish) VALUES ('Gran Premio de Presentelandia', '2024-10-01', '2024-11-30')")


# Inserta una nueva sesión
cursor.execute("INSERT INTO sessions (gp_id, datetime, type) VALUES (2, '2024-04-12 10:30:00', 'libres')")
cursor.execute("INSERT INTO sessions (gp_id, datetime, type) VALUES (2, '2024-04-12 10:30:00', 'squaly')")
cursor.execute("INSERT INTO sessions (gp_id, datetime, type) VALUES (2, '2024-04-12 10:30:00', 'sprint')")
cursor.execute("INSERT INTO sessions (gp_id, datetime, type) VALUES (2, '2024-04-12 10:30:00', 'qualy')")
cursor.execute("INSERT INTO sessions (gp_id, datetime, type) VALUES (2, '2024-11-08 10:30:00', 'carrera')")

conn.commit()


# # Inserta un nuevo usuario
# cursor.execute("INSERT INTO usuarios (nombre) VALUES ('Juan')")

# # Inserta