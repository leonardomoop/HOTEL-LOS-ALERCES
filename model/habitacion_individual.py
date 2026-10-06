from model.habitacion import Habitacion

class HabitacionIndividual(Habitacion):
    """
    Subtipo de habitación para un único huésped.
    Hereda de Habitacion usando super().__init__().
    """
    def __init__(self, numero: int, piso: int, precio_base_usd: float = 50.0, limpia: bool = True):
        super().__init__(numero, piso, precio_base_usd, limpia)

    def capacidad(self) -> int:
        return 1

    def tipo_nombre(self) -> str:
        return "Individual"

    def calcular_tarifa(self, noches: int, valor_dolar: float = 1.0) -> int:
        """
        Cálculo de tarifa para Habitación Individual:
        Tarifa estándar directa por noche según valor dólar.
        """
        if noches <= 0:
            raise ValueError("La cantidad de noches debe ser mayor a 0.")
        costo_usd = self.precio_base_usd * noches
        return round(costo_usd * valor_dolar)
