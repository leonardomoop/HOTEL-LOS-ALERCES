class DAO:
    """
    Clase base para todos los Data Access Objects (DAO).
    Mantiene la referencia a la conexión activa y al cursor de la base de datos.
    """
    def __init__(self, conexion):
        self.conexion = conexion
        self.cursor = conexion.cursor()
