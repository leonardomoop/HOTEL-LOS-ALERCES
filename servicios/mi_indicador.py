import requests
from requests.exceptions import Timeout, ConnectionError, RequestException

class MiIndicador:
    """
    Servicio para el consumo de indicadores económicos oficiales desde la API REST mindicador.cl.
    Implementa tiempos de espera (timeout) y manejo exhaustivo de excepciones de red
    para asegurar la alta disponibilidad y continuidad operacional del sistema.
    """
    BASE_URL = "https://mindicador.cl/api/"
    VALOR_DOLAR_CONTINGENCIA = 950.0  # Valor de respaldo seguro ante pérdida de conectividad

    def __init__(self, timeout: int = 5):
        self.__timeout = timeout

    @property
    def timeout(self) -> int:
        return self.__timeout

    def obtener_dolar(self, fecha: str = None) -> tuple[float, str, bool]:
        """
        Consulta el valor del dólar observado en pesos chilenos (CLP).
        
        Retorna una tupla: (valor_dolar: float, mensaje_estado: str, es_en_linea: bool)
        - Si la conexión es exitosa: retorna el valor obtenido en tiempo real desde la API.
        - Si hay falla de red, timeout o desconexión (P17): captura la excepción,
          informa claramente al usuario del incidente y proporciona continuidad
          utilizando una tasa de contingencia sin detener la ejecución del programa.
        """
        url = self.BASE_URL + "dolar"
        if fecha:
            # Formato esperado por mindicador: DD-MM-YYYY
            partes = fecha.split("-")
            if len(partes) == 3 and len(partes[0]) == 4:
                fecha_api = f"{partes[2]}-{partes[1]}-{partes[0]}"
            else:
                fecha_api = fecha
            url += f"/{fecha_api}"

        try:
            respuesta = requests.get(url, timeout=self.__timeout)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                if datos.get("serie") and len(datos["serie"]) > 0:
                    valor = float(datos["serie"][0]["valor"])
                    fecha_obtenida = datos["serie"][0].get("fecha", "")[:10]
                    return valor, f"Valor obtenido en línea exitosamente ({fecha_obtenida}): ${valor:,.2f} CLP/USD", True
                else:
                    return self.VALOR_DOLAR_CONTINGENCIA, "La API no retornó series de datos para la fecha consultada. Se usa valor de respaldo.", False
            else:
                return self.VALOR_DOLAR_CONTINGENCIA, f"La API respondió con código de error HTTP {respuesta.status_code}. Se usa valor de respaldo.", False

        except Timeout:
            mensaje = "⚠️ Tiempo de espera agotado al conectar con mindicador.cl (Timeout). Se activa modo contingencia."
            return self.VALOR_DOLAR_CONTINGENCIA, mensaje, False

        except ConnectionError:
            mensaje = "⚠️ Sin conexión a internet o servidor de mindicador.cl no disponible (ConnectionError). Se activa modo contingencia."
            return self.VALOR_DOLAR_CONTINGENCIA, mensaje, False

        except RequestException as e:
            mensaje = f"⚠️ Incidencia de red al consultar servicio externo ({type(e).__name__}). Se activa modo contingencia."
            return self.VALOR_DOLAR_CONTINGENCIA, mensaje, False

        except Exception as e:
            mensaje = f"⚠️ Error inesperado al procesar la respuesta de la API ({e}). Se activa modo contingencia."
            return self.VALOR_DOLAR_CONTINGENCIA, mensaje, False
