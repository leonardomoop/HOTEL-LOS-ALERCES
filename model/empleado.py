from model.persona import Persona

class Empleado(Persona):
    """
    Clase base para el personal del hotel.
    Hereda de Persona y define el rol del trabajador para control operativo.
    """
    def __init__(self, rut: str, nombre: str, rol: str, telefono: str = "", email: str = ""):
        super().__init__(rut, nombre, telefono, email)
        self.__rol = None
        self.rol = rol

    @property
    def rol(self) -> str:
        return self.__rol

    @rol.setter
    def rol(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El rol del empleado no puede estar vacío.")
        self.__rol = valor.strip()

    def obtener_rol(self) -> str:
        return self.__rol
