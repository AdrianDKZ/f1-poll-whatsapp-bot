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
        telephone TEXT NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        points INTEGER DEFAULT 0 NOT NULL,
        strikes INTEGER DEFAULT 0 NOT NULL
    );
""")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS teams (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        user1 TEXT,
        user2 TEXT,
        FOREIGN KEY (user1) REFERENCES usuarios(id),
        FOREIGN KEY (user2) REFERENCES usuarios(id)
    );
''')

# Crea la tabla predicciones
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY,
        session_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        prediction TEXT NOT NULL,
        points INTEGER,
        FOREIGN KEY (session_id) REFERENCES sessions(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
""")

conn.commit()
