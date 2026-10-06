from model.habitacion import Habitacion

class Suite(Habitacion):
    """
    Subtipo de habitación de lujo (Suite) para hasta 4 huéspedes.
    Hereda de Habitacion usando super().__init__().
    """
    def __init__(self, numero: int, piso: int, precio_base_usd: float = 160.0, limpia: bool = True):
        super().__init__(numero, piso, precio_base_usd, limpia)

    def capacidad(self) -> int:
        return 4

    def tipo_nombre(self) -> str:
        return "Suite"

    def calcular_tarifa(self, noches: int, valor_dolar: float = 1.0) -> int:
        """
        Cálculo de tarifa para Suite:
        Es la categoría de mayor valor. Aplica tarifa base superior y un cargo de servicio
        exclusivo por amenities premium y acceso a sala VIP (15% adicional).
        """
        if noches <= 0:
            raise ValueError("La cantidad de noches debe ser mayor a 0.")
        recargo_lujo = 1.15
        costo_usd = (self.precio_base_usd * noches) * recargo_lujo
        return round(costo_usd * valor_dolar)
