class Habitacion:
    """
    Clase base que representa una dependencia física del hotel.
    Define atributos comunes de habitación y el método polimórfico calcular_tarifa().
    """
    def __init__(self, numero: int, piso: int, precio_base_usd: float, limpia: bool = True):
        self.__numero = None
        self.__piso = None
        self.__precio_base_usd = None
        self.__limpia = limpia

        self.numero = numero
        self.piso = piso
        self.precio_base_usd = precio_base_usd

    @property
    def numero(self) -> int:
        return self.__numero

    @numero.setter
    def numero(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El número de habitación debe ser un entero positivo.")
        self.__numero = valor

    @property
    def piso(self) -> int:
        return self.__piso

    @piso.setter
    def piso(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("El piso debe ser un entero positivo.")
        self.__piso = valor

    @property
    def precio_base_usd(self) -> float:
        return self.__precio_base_usd

    @precio_base_usd.setter
    def precio_base_usd(self, valor: float):
        if valor < 0:
            raise ValueError("El precio base en USD no puede ser negativo.")
        self.__precio_base_usd = float(valor)

    @property
    def limpia(self) -> bool:
        return self.__limpia

    @limpia.setter
    def limpia(self, valor: bool):
        self.__limpia = bool(valor)

    def capacidad(self) -> int:
        """
        Retorna la capacidad máxima de personas. Sobrescribir en subtipos.
        """
        return 1

    def tipo_nombre(self) -> str:
        """
        Retorna el nombre del tipo de habitación. Sobrescribir en subtipos.
        """
        return "Habitación Base"

    def calcular_tarifa(self, noches: int, valor_dolar: float = 1.0) -> int:
        """
        Calcula la tarifa total en pesos chilenos (CLP) según las noches y el tipo de cambio.
        Método polimórfico a sobrescribir por cada subtipo de habitación.
        """
        if noches <= 0:
            raise ValueError("La cantidad de noches debe ser mayor a 0.")
        return round(self.__precio_base_usd * noches * valor_dolar)

    def __str__(self) -> str:
        estado_limp = "Limpia" if self.__limpia else "Sucia"
        return (
            f"Habitación {self.__numero} ({self.tipo_nombre()}) - Piso {self.__piso} | "
            f"Capacidad: {self.capacidad()} pers. | Tarifa Base: ${self.__precio_base_usd:.2f} USD/noche | "
            f"Estado: {estado_limp}"
        )
