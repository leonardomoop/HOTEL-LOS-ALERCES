class HabitacionOcupadaError(Exception):
    """
    Excepción de regla de negocio 1:
    Se lanza cuando se intenta reservar una habitación que ya se encuentra ocupada
    o reservada en el rango de fechas solicitado.
    """
    def __init__(self, numero_habitacion: int, fecha_inicio: str, fecha_fin: str, mensaje: str = None):
        if not mensaje:
            mensaje = (
                f"Regla de Negocio Incumplida: La habitación N° {numero_habitacion} "
                f"ya se encuentra ocupada/reservada entre el {fecha_inicio} y el {fecha_fin}."
            )
        super().__init__(mensaje)
        self.numero_habitacion = numero_habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


class AnticipoInsuficienteError(Exception):
    """
    Excepción de regla de negocio 2:
    Se lanza cuando se intenta realizar el check-in de una reserva sin haber
    completado al menos el 50% de pago por anticipado.
    """
    def __init__(self, anticipo_actual: int, minimo_requerido: int, mensaje: str = None):
        if not mensaje:
            mensaje = (
                f"Regla de Negocio Incumplida: No se puede realizar el Check-in. "
                f"Se requiere un anticipo mínimo del 50% (${minimo_requerido:,.0f} CLP) "
                f"y el monto abonado actual es de ${anticipo_actual:,.0f} CLP."
            )
        super().__init__(mensaje)
        self.anticipo_actual = anticipo_actual
        self.minimo_requerido = minimo_requerido


class DatoInvalidoError(Exception):
    """
    Excepción lanzada cuando los datos proporcionados no cumplen con el formato o rango exigido.
    """
    pass
