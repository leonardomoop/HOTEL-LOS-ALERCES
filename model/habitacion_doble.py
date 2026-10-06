from model.habitacion import Habitacion

class HabitacionDoble(Habitacion):
    """
    Subtipo de habitación para dos huéspedes.
    Hereda de Habitacion usando super().__init__().
    """
    def __init__(self, numero: int, piso: int, precio_base_usd: float = 85.0, limpia: bool = True):
        super().__init__(numero, piso, precio_base_usd, limpia)

    def capacidad(self) -> int:
        return 2

    def tipo_nombre(self) -> str:
        return "Doble"

    def calcular_tarifa(self, noches: int, valor_dolar: float = 1.0) -> int:
        """
        Cálculo de tarifa para Habitación Doble:
        Incluye tarifa por noche con recargo por servicio de desayuno buffet para 2 personas (10% adicional).
        """
        if noches <= 0:
            raise ValueError("La cantidad de noches debe ser mayor a 0.")
        recargo_desayuno = 1.10
        costo_usd = (self.precio_base_usd * noches) * recargo_desayuno
        return round(costo_usd * valor_dolar)
