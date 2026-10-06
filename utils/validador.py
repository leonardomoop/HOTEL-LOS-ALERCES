from datetime import datetime
import re

def validar_rut(rut: str) -> bool:
    """
    Valida un RUT chileno aplicando el algoritmo Módulo 11.
    Acepta formatos con puntos y guion (12.345.678-5) o limpios (12345678-5).
    Retorna True si el RUT es válido, False en caso contrario.
    """
    if not rut or not isinstance(rut, str):
        return False

    # Limpiar puntos, espacios y guiones
    rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()

    if len(rut_limpio) < 2:
        return False

    cuerpo = rut_limpio[:-1]
    dv_ingresado = rut_limpio[-1]

    if not cuerpo.isdigit():
        return False

    # Algoritmo Módulo 11
    suma = 0
    multiplicador = 2

    for c in reversed(cuerpo):
        suma += int(c) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    dv_calculado = 11 - resto

    if dv_calculado == 11:
        dv_esperado = "0"
    elif dv_calculado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_calculado)

    return dv_ingresado == dv_esperado

def formatear_rut(rut: str) -> str:
    """
    Formatea un RUT a la estructura estándar: XX.XXX.XXX-X
    """
    rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()
    if len(rut_limpio) < 2:
        return rut
    cuerpo = rut_limpio[:-1]
    dv = rut_limpio[-1]
    # Formatear cuerpo con puntos
    cuerpo_con_puntos = f"{int(cuerpo):,}".replace(",", ".")
    return f"{cuerpo_con_puntos}-{dv}"

def validar_documento(doc: str) -> bool:
    """
    Valida si el documento es un RUT chileno válido o un pasaporte extranjero
    (mínimo 6 caracteres alfanuméricos).
    """
    if not doc or not isinstance(doc, str):
        return False
    doc = doc.strip()
    if validar_rut(doc):
        return True
    # Pasaporte internacional: 6 a 12 caracteres alfanuméricos
    return bool(re.match(r"^[A-Za-z0-9]{6,12}$", doc))

def leer_entero(mensaje: str, minimo: int = None, maximo: int = None) -> int:
    """
    Lee un número entero por consola de forma segura, evitando que el programa se caiga
    si el usuario ingresa letras o caracteres inválidos.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            valor = int(entrada)
            if minimo is not None and valor < minimo:
                print(f"❌ Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"❌ Error: El valor debe ser menor o igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("❌ Error: Debe ingresar un número entero válido (no se permiten letras ni símbolos).")

def leer_flotante(mensaje: str, minimo: float = None) -> float:
    """
    Lee un número decimal por consola de forma segura.
    """
    while True:
        entrada = input(mensaje).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if minimo is not None and valor < minimo:
                print(f"❌ Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("❌ Error: Debe ingresar un valor numérico válido.")

def leer_fecha(mensaje: str) -> str:
    """
    Lee una fecha en formato YYYY-MM-DD y valida su formato y coherencia.
    """
    while True:
        entrada = input(mensaje).strip()
        try:
            fecha = datetime.strptime(entrada, "%Y-%m-%d").date()
            return fecha.strftime("%Y-%m-%d")
        except ValueError:
            print("❌ Formato de fecha inválido. Debe usar el formato AAAA-MM-DD (ejemplo: 2026-10-10).")
