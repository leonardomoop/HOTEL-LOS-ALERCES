from model.empleado import Empleado

class Camarero(Empleado):
    """
    Representa al personal de limpieza de housekeeping.
    Su interacción con el sistema se limita al mantenimiento y aseo de dependencias.
    """
    def __init__(self, rut: str, nombre: str, turno: str = "Mañana", telefono: str = "", email: str = ""):
        super().__init__(rut, nombre, rol="Camarero", telefono=telefono, email=email)
        self.__turno = turno

    @property
    def turno(self) -> str:
        return self.__turno

    @turno.setter
    def turno(self, valor: str):
        self.__turno = valor

    def marcar_limpieza(self, habitacion) -> None:
        """
        Marca una habitación como limpia y lista para su uso.
        """
        habitacion.limpia = True
