from datetime import datetime
from model.huesped import Huesped
from model.habitacion import Habitacion
from model.linea_consumo import LineaConsumo
from model.excepciones import AnticipoInsuficienteError

class Reserva:
    """
    Clase central transaccional del negocio.
    Enlaza al huésped, la habitación, el rango de fechas de la estadía,
    el valor del dólar del día y sus líneas de detalle de consumos extras.
    Aplica la Regla de Negocio 2: no permite Check-in sin al menos el 50% de anticipo.
    """
    def __init__(
        self,
        huesped: Huesped,
        habitacion: Habitacion,
        fecha_inicio: str,
        fecha_fin: str,
        valor_dolar: float = 1.0,
        anticipo_pagado: int = 0,
        check_in_realizado: bool = False,
        id_reserva: int = None
    ):
        self.__id = id_reserva
        self.__huesped = huesped
        self.__habitacion = habitacion
        self.__fecha_inicio = None
        self.__fecha_fin = None
        self.__valor_dolar = None
        self.__anticipo_pagado = None
        self.__check_in_realizado = bool(check_in_realizado)
        self.__lineas_detalle = []

        # Validación y asignación mediante setters
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.valor_dolar = valor_dolar
        self.anticipo_pagado = anticipo_pagado

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, valor: int):
        self.__id = valor

    @property
    def huesped(self) -> Huesped:
        return self.__huesped

    @property
    def habitacion(self) -> Habitacion:
        return self.__habitacion

    @property
    def fecha_inicio(self) -> str:
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, valor: str):
        datetime.strptime(valor, "%Y-%m-%d")
        self.__fecha_inicio = valor

    @property
    def fecha_fin(self) -> str:
        return self.__fecha_fin

    @fecha_fin.setter
    def fecha_fin(self, valor: str):
        datetime.strptime(valor, "%Y-%m-%d")
        if self.__fecha_inicio and valor <= self.__fecha_inicio:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de inicio.")
        self.__fecha_fin = valor

    @property
    def valor_dolar(self) -> float:
        return self.__valor_dolar

    @valor_dolar.setter
    def valor_dolar(self, valor: float):
        if valor <= 0:
            raise ValueError("El valor del dólar debe ser mayor a 0.")
        self.__valor_dolar = float(valor)

    @property
    def anticipo_pagado(self) -> int:
        return self.__anticipo_pagado

    @anticipo_pagado.setter
    def anticipo_pagado(self, valor: int):
        if valor < 0:
            raise ValueError("El anticipo pagado no puede ser negativo.")
        self.__anticipo_pagado = int(valor)

    @property
    def check_in_realizado(self) -> bool:
        return self.__check_in_realizado

    @check_in_realizado.setter
    def check_in_realizado(self, valor: bool):
        self.__check_in_realizado = bool(valor)

    @property
    def lineas_detalle(self) -> list:
        return list(self.__lineas_detalle)

    def agregar_linea_consumo(self, linea: LineaConsumo) -> None:
        """
        Agrega una línea de consumo adicional a la reserva.
        """
        self.__lineas_detalle.append(linea)

    def calcular_noches(self) -> int:
        """
        Calcula la cantidad de noches entre fecha de inicio y salida.
        """
        f_ini = datetime.strptime(self.__fecha_inicio, "%Y-%m-%d").date()
        f_fin = datetime.strptime(self.__fecha_fin, "%Y-%m-%d").date()
        noches = (f_fin - f_ini).days
        return max(1, noches)

    def total_hospedaje(self) -> int:
        """
        Calcula el costo del hospedaje usando el método polimórfico de la habitación
        multiplicado por el valor del dólar del día.
        """
        noches = self.calcular_noches()
        return self.__habitacion.calcular_tarifa(noches, self.__valor_dolar)

    def total_consumos(self) -> int:
        """
        Suma el subtotal de todas las líneas de consumos extras.
        """
        return sum(linea.subtotal() for linea in self.__lineas_detalle)

    def total(self) -> int:
        """
        Calcula el monto total consolidado: Hospedaje + Consumos extras.
        """
        return self.total_hospedaje() + self.total_consumos()

    def anticipo_minimo_requerido(self) -> int:
        """
        Calcula el 50% mínimo requerido para autorizar el Check-in.
        """
        return round(self.total_hospedaje() * 0.50)

    def saldo_pendiente(self) -> int:
        """
        Retorna el saldo que falta por pagar.
        """
        return max(0, self.total() - self.__anticipo_pagado)

    def realizar_check_in(self) -> None:
        """
        Ejecuta el Check-in aplicando la Regla de Negocio 2:
        Bloquea el ingreso si no se ha pagado al menos el 50% de anticipo.
        Lanza AnticipoInsuficienteError si no cumple la regla.
        """
        minimo = self.anticipo_minimo_requerido()
        if self.__anticipo_pagado < minimo:
            raise AnticipoInsuficienteError(
                anticipo_actual=self.__anticipo_pagado,
                minimo_requerido=minimo
            )
        self.__check_in_realizado = True

    def __str__(self) -> str:
        id_str = f"Reserva #{self.__id} | " if self.__id else "Reserva Nueva | "
        check_str = "Check-in: REALIZADO" if self.__check_in_realizado else "Check-in: PENDIENTE"
        return (
            f"{id_str}Huésped: {self.__huesped.nombre} | Habitación: {self.__habitacion.numero} ({self.__habitacion.tipo_nombre()})\n"
            f"  Fechas: {self.__fecha_inicio} al {self.__fecha_fin} ({self.calcular_noches()} noches)\n"
            f"  Tarifa Dólar aplicada: ${self.__valor_dolar:,.2f} CLP/USD\n"
            f"  Hospedaje: ${self.total_hospedaje():,.0f} CLP | Consumos: ${self.total_consumos():,.0f} CLP\n"
            f"  Total: ${self.total():,.0f} CLP | Anticipo Pagado: ${self.__anticipo_pagado:,.0f} CLP | Saldo: ${self.saldo_pendiente():,.0f} CLP\n"
            f"  Estado: {check_str}"
        )
