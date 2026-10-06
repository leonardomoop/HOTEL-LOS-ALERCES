import sqlite3
import os

# Ruta de la base de datos en el mismo directorio del proyecto
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hotel.db")

def crear_conexion():
    """
    Crea y retorna una conexión a la base de datos SQLite 'hotel.db'.
    Habilita explícitamente el soporte de claves foráneas (Foreign Keys)
    para asegurar la integridad referencial de los datos.
    """
    conexion = sqlite3.connect(DB_PATH)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion
