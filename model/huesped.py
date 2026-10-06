from model.persona import Persona

class Huesped(Persona):
    """
    Representa al cliente o huésped del Hotel Los Alerces.
    Hereda de Persona con super().__init__() y mantiene el historial de sus reservas.
    """
    def __init__(self, rut: str, nombre: str, telefono: str = "", email: str = "", id_huesped: int = None):
        super().__init__(rut, nombre, telefono, email)
        self.__id = id_huesped
        self.__reservas = []

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, valor: int):
        self.__id = valor

    def agregar_reserva(self, reserva):
        self.__reservas.append(reserva)

    def obtener_reservas(self) -> list:
        return list(self.__reservas)

    def __str__(self) -> str:
        id_str = f"[ID: {self.__id}] " if self.__id else ""
        return f"{id_str}{self.nombre} | RUT/Doc: {self.rut} | Tel: {self.telefono} | Email: {self.email}"
