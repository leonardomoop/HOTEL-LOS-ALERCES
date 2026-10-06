from utils.validador import validar_documento, formatear_rut

class Persona:
    """
    Clase base que representa a un individuo (cliente o trabajador) en el sistema.
    Centraliza datos comunes como identificación, nombres y datos de contacto,
    y aloja la validación de formato del documento (RUT o pasaporte).
    """
    def __init__(self, rut: str, nombre: str, telefono: str = "", email: str = ""):
        self.__rut = None
        self.__nombre = None
        self.__telefono = None
        self.__email = None

        # Uso de setters para asegurar validación inicial
        self.rut = rut
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    @property
    def rut(self) -> str:
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        if not valor or not validar_documento(valor):
            raise ValueError(f"El RUT o pasaporte '{valor}' no tiene un formato válido.")
        self.__rut = formatear_rut(valor) if "-" in valor or valor.replace(".", "").isdigit() else valor.strip()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        self.__telefono = valor.strip() if valor else ""

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        self.__email = valor.strip() if valor else ""

    def __str__(self) -> str:
        return f"{self.__nombre} (Doc: {self.__rut}, Tel: {self.__telefono})"
