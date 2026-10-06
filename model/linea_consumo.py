from model.consumo import Consumo

class LineaConsumo:
    """
    Representa una línea de detalle de consumo adicional asociada a una reserva.
    Composición con Reserva: si la reserva se elimina, sus líneas se destruyen lógicamente.
    """
    def __init__(self, consumo: Consumo, cantidad: int, precio_unitario: int = None, id_linea: int = None, reserva_id: int = None):
        self.__id = id_linea
        self.__reserva_id = reserva_id
        self.__consumo = consumo
        self.__cantidad = None
        self.__precio_unitario = None

        self.cantidad = cantidad
        self.precio_unitario = precio_unitario if precio_unitario is not None else consumo.precio_unitario

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, valor: int):
        self.__id = valor

    @property
    def reserva_id(self) -> int:
        return self.__reserva_id

    @reserva_id.setter
    def reserva_id(self, valor: int):
        self.__reserva_id = valor

    @property
    def consumo(self) -> Consumo:
        return self.__consumo

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("La cantidad debe ser un entero positivo mayor a 0.")
        self.__cantidad = valor

    @property
    def precio_unitario(self) -> int:
        return self.__precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor: int):
        if valor < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        self.__precio_unitario = int(valor)

    def subtotal(self) -> int:
        """
        Retorna el subtotal de la línea de detalle: cantidad * precio unitario.
        """
        return self.__cantidad * self.__precio_unitario

    def __str__(self) -> str:
        return (
            f"  - {self.__consumo.nombre}: {self.__cantidad} unid. x ${self.__precio_unitario:,.0f} CLP "
            f"= ${self.subtotal():,.0f} CLP"
        )
