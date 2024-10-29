import sqlite3

# Conecta a la base de datos
conn = sqlite3.connect('Porra2024.db')
cursor = conn.cursor()

# Crea la tabla gp
cursor.execute("""
    CREATE TABLE IF NOT EXISTS gp (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE NOT NULL
    );
""")

# Crea la tabla sesiones
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sesiones (
        id INTEGER PRIMARY KEY,
        gp_id INTEGER NOT NULL,
        fecha DATE NOT NULL,
        hora TIME NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('Sprint', 'Sprint Qaly', 'Qaly', 'Carrera')),
        FOREIGN KEY (gp_id) REFERENCES gp(id)
    );
""")

# Crea la tabla usuarios
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        telefono TEXT NOT NULL
    );
""")

# Crea la tabla predicciones
cursor.execute("""
    CREATE TABLE IF NOT EXISTS predicciones (
        id INTEGER PRIMARY KEY,
        sesion_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        resultado TEXT NOT NULL,
        FOREIGN KEY (sesion_id) REFERENCES sesiones(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
""")

# Crea la tabla resultados
cursor.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY,
        sesion_id INTEGER NOT NULL,
        usuario_id INTEGER NOT NULL,
        puntuacion INTEGER NOT NULL,
        FOREIGN KEY (sesion_id) REFERENCES sesiones(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
""")

# Crea la tabla puntuaciones_totales
cursor.execute("""
    CREATE TABLE IF NOT EXISTS puntuaciones_totales (
        usuario_id INTEGER NOT NULL,
        gp_id INTEGER NOT NULL,
        puntuacion INTEGER NOT NULL,
        PRIMARY KEY (usuario_id, gp_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
        FOREIGN KEY (gp_id) REFERENCES gp(id)
    );
""")

# # Inserta un nuevo GP
# cursor.execute("INSERT INTO gp (nombre, fecha_inicio, fecha_fin) VALUES ('Gran Premio de España', '2024-04-12', '2024-04-14')")

# # Inserta una nueva sesión
# cursor.execute("INSERT INTO sesiones (gp_id, fecha, hora, tipo) VALUES (1, '2024-04-12', '10:30:00', 'Sprint')")

# # Inserta un nuevo usuario
# cursor.execute("INSERT INTO usuarios (nombre) VALUES ('Juan')")

# # Inserta