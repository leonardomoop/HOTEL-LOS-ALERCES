from dao.dao import DAO
from model.consumo import Consumo

class ConsumoDAO(DAO):
    """
    Data Access Object para el catálogo maestro de consumos extras
    (Minibar, Room Service, Spa, etc.).
    """
    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                precio_unitario INTEGER NOT NULL
            )
        """)
        self.conexion.commit()
        self.insertar_predeterminados()

    def insertar_predeterminados(self):
        """
        Inserta los productos o servicios del catálogo requeridos para el guión de pruebas.
        """
        self.cursor.execute("SELECT COUNT(*) FROM consumo")
        if self.cursor.fetchone()[0] == 0:
            catalogo = [
                ("MIN-01", "Consumo Minibar", 5000),
                ("RMS-01", "Room Service Gastronómico", 12000),
                ("SPA-01", "Sesión de Spa & Relajación", 25000),
            ]
            self.cursor.executemany("""
                INSERT INTO consumo (codigo, nombre, precio_unitario)
                VALUES (?, ?, ?)
            """, catalogo)
            self.conexion.commit()

    def listar(self) -> list:
        query = "SELECT id, codigo, nombre, precio_unitario FROM consumo ORDER BY id ASC"
        self.cursor.execute(query)
        filas = self.cursor.fetchall()
        return [Consumo(codigo=f[1], nombre=f[2], precio_unitario=f[3], id_consumo=f[0]) for f in filas]

    def buscar_por_id(self, id_consumo: int):
        query = "SELECT id, codigo, nombre, precio_unitario FROM consumo WHERE id = ?"
        self.cursor.execute(query, (id_consumo,))
        fila = self.cursor.fetchone()
        if fila:
            return Consumo(codigo=fila[1], nombre=fila[2], precio_unitario=fila[3], id_consumo=fila[0])
        return None

    def buscar_por_codigo(self, codigo: str):
        query = "SELECT id, codigo, nombre, precio_unitario FROM consumo WHERE codigo = ?"
        self.cursor.execute(query, (codigo.strip().upper(),))
        fila = self.cursor.fetchone()
        if fila:
            return Consumo(codigo=fila[1], nombre=fila[2], precio_unitario=fila[3], id_consumo=fila[0])
        return None
