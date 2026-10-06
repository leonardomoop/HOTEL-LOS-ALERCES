from dao.dao import DAO
from model.habitacion_individual import HabitacionIndividual
from model.habitacion_doble import HabitacionDoble
from model.suite import Suite

class HabitacionDAO(DAO):
    """
    Data Access Object para la persistencia de habitaciones.
    Mapea los registros hacia sus subtipos correspondientes (polimorfismo).
    """
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS habitacion (
                numero INTEGER PRIMARY KEY,
                piso INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                precio_base_usd REAL NOT NULL,
                limpia INTEGER NOT NULL DEFAULT 1
            )
        """)
        self.conexion.commit()
        self.insertar_predeterminadas()

    def insertar_predeterminadas(self):
        """
        Inserta las habitaciones iniciales para las pruebas del sistema si la tabla está vacía.
        """
        self.cursor.execute("SELECT COUNT(*) FROM habitacion")
        if self.cursor.fetchone()[0] == 0:
            habitaciones = [
                (101, 1, "Individual", 50.0, 1),
                (102, 1, "Doble", 85.0, 1),
                (201, 2, "Suite", 160.0, 1),
            ]
            self.cursor.executemany("""
                INSERT INTO habitacion (numero, piso, tipo, precio_base_usd, limpia)
                VALUES (?, ?, ?, ?, ?)
            """, habitaciones)
            self.conexion.commit()

    def _mapear_objeto(self, fila):
        if not fila:
            return None
        numero, piso, tipo, precio_base, limpia_int = fila
        es_limpia = bool(limpia_int)

        if tipo == "Individual":
            return HabitacionIndividual(numero, piso, precio_base, es_limpia)
        elif tipo == "Doble":
            return HabitacionDoble(numero, piso, precio_base, es_limpia)
        elif tipo == "Suite":
            return Suite(numero, piso, precio_base, es_limpia)
        else:
            return HabitacionIndividual(numero, piso, precio_base, es_limpia)

    def listar(self) -> list:
        query = "SELECT numero, piso, tipo, precio_base_usd, limpia FROM habitacion ORDER BY numero ASC"
        self.cursor.execute(query)
        filas = self.cursor.fetchall()
        return [self._mapear_objeto(f) for f in filas]

    def buscar_por_numero(self, numero: int):
        query = "SELECT numero, piso, tipo, precio_base_usd, limpia FROM habitacion WHERE numero = ?"
        self.cursor.execute(query, (numero,))
        fila = self.cursor.fetchone()
        return self._mapear_objeto(fila)

    def actualizar_limpieza(self, numero: int, limpia: bool) -> bool:
        query = "UPDATE habitacion SET limpia = ? WHERE numero = ?"
        self.cursor.execute(query, (1 if limpia else 0, numero))
        self.conexion.commit()
        return self.cursor.rowcount > 0
