from dao.dao import DAO
from model.reserva import Reserva
from model.linea_consumo import LineaConsumo
from model.excepciones import HabitacionOcupadaError
from dao.huesped_dao import HuespedDAO
from dao.habitacion_dao import HabitacionDAO
from dao.consumo_dao import ConsumoDAO

class ReservaDAO(DAO):
    """
    Data Access Object para la gestión de Reservas y sus Líneas de Consumo.
    Gestiona transacciones compuestas (cabecera y detalle) y valida la disponibilidad.
    """
    def __init__(self, conexion):
        super().__init__(conexion)
        self.huesped_dao = HuespedDAO(conexion)
        self.habitacion_dao = HabitacionDAO(conexion)
        self.consumo_dao = ConsumoDAO(conexion)

    def crear_tablas(self):
        """
        Crea las tablas 'reserva' y 'linea_consumo' con soporte de claves foráneas.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reserva (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                huesped_id INTEGER NOT NULL,
                habitacion_numero INTEGER NOT NULL,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NOT NULL,
                valor_dolar REAL NOT NULL,
                anticipo_pagado INTEGER NOT NULL DEFAULT 0,
                check_in_realizado INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (huesped_id) REFERENCES huesped(id),
                FOREIGN KEY (habitacion_numero) REFERENCES habitacion(numero)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS linea_consumo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reserva_id INTEGER NOT NULL,
                consumo_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario INTEGER NOT NULL,
                FOREIGN KEY (reserva_id) REFERENCES reserva(id) ON DELETE CASCADE,
                FOREIGN KEY (consumo_id) REFERENCES consumo(id)
            )
        """)
        self.conexion.commit()

    def habitacion_disponible(self, habitacion_numero: int, fecha_inicio: str, fecha_fin: str, excluir_id: int = None) -> bool:
        """
        Comprueba si la habitación está libre en el rango de fechas solicitado.
        Condición de solapamiento: fecha_inicio < r.fecha_fin AND fecha_fin > r.fecha_inicio.
        """
        query = """
            SELECT COUNT(*) FROM reserva
            WHERE habitacion_numero = ?
              AND fecha_inicio < ?
              AND fecha_fin > ?
        """
        params = [habitacion_numero, fecha_fin, fecha_inicio]
        if excluir_id is not None:
            query += " AND id != ?"
            params.append(excluir_id)

        self.cursor.execute(query, tuple(params))
        conflictos = self.cursor.fetchone()[0]
        return conflictos == 0

    def insertar(self, reserva: Reserva) -> Reserva:
        """
        Registra una nueva reserva con sus líneas de detalle de forma transaccional.
        Aplica la Regla de Negocio 1: lanza HabitacionOcupadaError si las fechas se solapan.
        """
        if not self.habitacion_disponible(reserva.habitacion.numero, reserva.fecha_inicio, reserva.fecha_fin):
            raise HabitacionOcupadaError(
                numero_habitacion=reserva.habitacion.numero,
                fecha_inicio=reserva.fecha_inicio,
                fecha_fin=reserva.fecha_fin
            )

        try:
            # 1. Insertar cabecera de la reserva
            query_reserva = """
                INSERT INTO reserva (
                    huesped_id, habitacion_numero, fecha_inicio, fecha_fin,
                    valor_dolar, anticipo_pagado, check_in_realizado
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params_reserva = (
                reserva.huesped.id,
                reserva.habitacion.numero,
                reserva.fecha_inicio,
                reserva.fecha_fin,
                reserva.valor_dolar,
                reserva.anticipo_pagado,
                1 if reserva.check_in_realizado else 0
            )
            self.cursor.execute(query_reserva, params_reserva)
            reserva_id = self.cursor.lastrowid
            reserva.id = reserva_id

            # 2. Insertar cada línea de consumo de detalle
            for linea in reserva.lineas_detalle:
                query_linea = """
                    INSERT INTO linea_consumo (reserva_id, consumo_id, cantidad, precio_unitario)
                    VALUES (?, ?, ?, ?)
                """
                self.cursor.execute(query_linea, (
                    reserva_id,
                    linea.consumo.id,
                    linea.cantidad,
                    linea.precio_unitario
                ))
                linea.id = self.cursor.lastrowid
                linea.reserva_id = reserva_id

            self.conexion.commit()
            return reserva

        except Exception as e:
            self.conexion.rollback()
            raise e

    def buscar_por_id(self, id_reserva: int):
        """
        Carga una reserva completa junto con su Huésped, Habitación y todas sus Líneas de Consumo.
        """
        query = """
            SELECT id, huesped_id, habitacion_numero, fecha_inicio, fecha_fin,
                   valor_dolar, anticipo_pagado, check_in_realizado
            FROM reserva
            WHERE id = ?
        """
        self.cursor.execute(query, (id_reserva,))
        fila = self.cursor.fetchone()
        if not fila:
            return None

        huesped = self.huesped_dao.buscar_por_id(fila[1])
        habitacion = self.habitacion_dao.buscar_por_numero(fila[2])

        reserva = Reserva(
            huesped=huesped,
            habitacion=habitacion,
            fecha_inicio=fila[3],
            fecha_fin=fila[4],
            valor_dolar=fila[5],
            anticipo_pagado=fila[6],
            check_in_realizado=bool(fila[7]),
            id_reserva=fila[0]
        )

        # Cargar líneas de detalle
        query_lineas = """
            SELECT id, consumo_id, cantidad, precio_unitario
            FROM linea_consumo
            WHERE reserva_id = ?
            ORDER BY id ASC
        """
        self.cursor.execute(query_lineas, (id_reserva,))
        filas_lineas = self.cursor.fetchall()
        for fl in filas_lineas:
            consumo = self.consumo_dao.buscar_por_id(fl[1])
            if consumo:
                linea = LineaConsumo(
                    consumo=consumo,
                    cantidad=fl[2],
                    precio_unitario=fl[3],
                    id_linea=fl[0],
                    reserva_id=id_reserva
                )
                reserva.agregar_linea_consumo(linea)

        return reserva

    def listar(self) -> list:
        """
        Retorna la lista de todas las reservas registradas.
        """
        self.cursor.execute("SELECT id FROM reserva ORDER BY id ASC")
        ids = [row[0] for row in self.cursor.fetchall()]
        return [self.buscar_por_id(r_id) for r_id in ids]

    def actualizar_anticipo(self, id_reserva: int, nuevo_anticipo: int) -> bool:
        query = "UPDATE reserva SET anticipo_pagado = ? WHERE id = ?"
        self.cursor.execute(query, (nuevo_anticipo, id_reserva))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def actualizar_check_in(self, id_reserva: int, realizado: bool = True) -> bool:
        query = "UPDATE reserva SET check_in_realizado = ? WHERE id = ?"
        self.cursor.execute(query, (1 if realizado else 0, id_reserva))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, id_reserva: int) -> bool:
        """
        Elimina una reserva y sus líneas de consumo asociadas por su ID.
        """
        self.cursor.execute("DELETE FROM linea_consumo WHERE reserva_id = ?", (id_reserva,))
        self.cursor.execute("DELETE FROM reserva WHERE id = ?", (id_reserva,))
        self.conexion.commit()
        return self.cursor.rowcount > 0
