from dao.dao import DAO
from model.huesped import Huesped

class HuespedDAO(DAO):
    """
    Data Access Object para la entidad Huesped.
    Implementa el CRUD completo con consultas 100% parametrizadas.
    """
    def crear_tabla(self):
        """
        Crea la tabla huesped si no existe.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS huesped (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rut TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                telefono TEXT,
                email TEXT
            )
        """)
        self.conexion.commit()

    def insertar(self, huesped: Huesped) -> Huesped:
        """
        Inserta un nuevo huésped en la base de datos de manera parametrizada.
        """
        query = "INSERT INTO huesped (rut, nombre, telefono, email) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (huesped.rut, huesped.nombre, huesped.telefono, huesped.email))
        self.conexion.commit()
        huesped.id = self.cursor.lastrowid
        return huesped

    def listar(self) -> list:
        """
        Retorna la lista de todos los huéspedes registrados.
        """
        query = "SELECT id, rut, nombre, telefono, email FROM huesped ORDER BY id ASC"
        self.cursor.execute(query)
        filas = self.cursor.fetchall()
        huespedes = []
        for f in filas:
            h = Huesped(
                rut=f[1],
                nombre=f[2],
                telefono=f[3] or "",
                email=f[4] or "",
                id_huesped=f[0]
            )
            huespedes.append(h)
        return huespedes

    def buscar_por_id(self, id_huesped: int):
        """
        Busca un huésped por su identificador primario.
        """
        query = "SELECT id, rut, nombre, telefono, email FROM huesped WHERE id = ?"
        self.cursor.execute(query, (id_huesped,))
        fila = self.cursor.fetchone()
        if fila:
            return Huesped(
                rut=fila[1],
                nombre=fila[2],
                telefono=fila[3] or "",
                email=fila[4] or "",
                id_huesped=fila[0]
            )
        return None

    def buscar_por_rut(self, rut: str):
        """
        Busca un huésped por su RUT o pasaporte.
        """
        query = "SELECT id, rut, nombre, telefono, email FROM huesped WHERE rut = ?"
        self.cursor.execute(query, (rut.strip(),))
        fila = self.cursor.fetchone()
        if fila:
            return Huesped(
                rut=fila[1],
                nombre=fila[2],
                telefono=fila[3] or "",
                email=fila[4] or "",
                id_huesped=fila[0]
            )
        return None

    def actualizar(self, huesped: Huesped) -> bool:
        """
        Actualiza el nombre, teléfono y email de un huésped existente.
        """
        query = "UPDATE huesped SET nombre = ?, telefono = ?, email = ? WHERE id = ?"
        self.cursor.execute(query, (huesped.nombre, huesped.telefono, huesped.email, huesped.id))
        self.conexion.commit()
        return self.cursor.rowcount > 0

    def eliminar(self, id_huesped: int) -> bool:
        """
        Elimina un huésped por su ID.
        """
        query = "DELETE FROM huesped WHERE id = ?"
        self.cursor.execute(query, (id_huesped,))
        self.conexion.commit()
        return self.cursor.rowcount > 0
