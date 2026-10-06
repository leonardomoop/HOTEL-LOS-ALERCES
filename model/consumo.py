class Consumo:
    """
    Representa un producto o servicio adicional del catálogo maestro del hotel
    (ej. Minibar, Room Service, Spa).
    """
    def __init__(self, codigo: str, nombre: str, precio_unitario: int, id_consumo: int = None):
        self.__id = id_consumo
        self.__codigo = None
        self.__nombre = None
        self.__precio_unitario = None

        self.codigo = codigo
        self.nombre = nombre
        self.precio_unitario = precio_unitario

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, valor: int):
        self.__id = valor

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El código de consumo no puede estar vacío.")
        self.__codigo = valor.strip()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ValueError("El nombre del consumo no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def precio_unitario(self) -> int:
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor: int):
        if valor < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        self.__precio_unitario = int(valor)

    def __str__(self) -> str:
        return f"{self.__nombre} (Cod: {self.__codigo}) - ${self.__precio_unitario:,.0f} CLP"
