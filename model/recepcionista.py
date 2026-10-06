from model.empleado import Empleado

class Recepcionista(Empleado):
    """
    Representa al perfil administrativo del hotel.
    Encapsula operaciones transaccionales críticas como gestionar reservas y cobros.
    """
    def __init__(self, rut: str, nombre: str, telefono: str = "", email: str = ""):
        super().__init__(rut, nombre, rol="Recepcionista", telefono=telefono, email=email)

    def puede_administrar(self) -> bool:
        return True
