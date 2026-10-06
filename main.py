import sys
from conectar import crear_conexion
from dao.huesped_dao import HuespedDAO
from dao.habitacion_dao import HabitacionDAO
from dao.consumo_dao import ConsumoDAO
from dao.reserva_dao import ReservaDAO
from model.huesped import Huesped
from model.linea_consumo import LineaConsumo
from model.reserva import Reserva
from model.excepciones import HabitacionOcupadaError, AnticipoInsuficienteError
from servicios.mi_indicador import MiIndicador
from utils.validador import (
    validar_rut,
    formatear_rut,
    leer_entero,
    leer_flotante,
    leer_fecha
)

def mostrar_menu_principal():
    print("\n" + "=" * 65)
    print("      🏨 SISTEMA DE GESTIÓN HOTEL BOUTIQUE LOS ALERCES 🏨      ")
    print("         Programación Orientada a Objeto Seguro - INACAP        ")
    print("=" * 65)
    print("  1. Gestión de Huéspedes (CRUD completo y validación RUT)")
    print("  2. Tipos de Habitación y Cálculo de Tarifas (Polimorfismo)")
    print("  3. Registrar Estadía con Consumos (Transacción con detalle)")
    print("  4. Consultar Detalle Completo de Estadía / Reserva")
    print("  5. Probar Regla de Negocio 1: Habitación Ocupada en Fechas")
    print("  6. Probar Regla de Negocio 2: Check-in con < 50% de Anticipo")
    print("  7. Consultar Dólar Oficial en Línea (mindicador.cl / Offline)")
    print("  8. Salir del Sistema")
    print("=" * 65)
    return input("👉 Seleccione una opción [1-8]: ").strip()


# =========================================================================
# 1. GESTIÓN DE HUÉSPEDES (P02, P03, P04, P05, P06, P07, P08)
# =========================================================================
def submenu_huespedes(huesped_dao: HuespedDAO):
    while True:
        print("\n" + "-" * 50)
        print("         👤 GESTIÓN DE HUÉSPEDES (CRUD)          ")
        print("-" * 50)
        print("  1. Registrar Nuevo Huésped (con validación de RUT)")
        print("  2. Listar Todos los Huéspedes")
        print("  3. Modificar Teléfono de un Huésped")
        print("  4. Eliminar un Huésped por ID")
        print("  5. Probar Validación de RUT (Módulo 11)")
        print("  6. Volver al Menú Principal")
        print("-" * 50)
        op = input("👉 Seleccione una opción [1-6]: ").strip()

        if op == "1":
            print("\n--- REGISTRAR HUÉSPED ---")
            rut_in = input("Ingrese RUT o documento de identidad: ").strip()
            if not validar_rut(rut_in):
                print(f"❌ Error de validación: El RUT '{rut_in}' no es válido según el algoritmo Módulo 11.")
                print("ℹ️  El programa continúa funcionando con total normalidad.")
                continue

            nombre = input("Ingrese Nombre completo: ").strip()
            if not nombre:
                print("❌ El nombre no puede estar vacío.")
                continue

            telefono = input("Ingrese Teléfono: ").strip()
            email = input("Ingrese Email: ").strip()

            try:
                nuevo = Huesped(rut=rut_in, nombre=nombre, telefono=telefono, email=email)
                huesped_dao.insertar(nuevo)
                print(f"✅ Huésped guardado con éxito en la base de datos con ID #{nuevo.id}.")
            except Exception as e:
                print(f"❌ Error al guardar huésped: {e}")

        elif op == "2":
            print("\n--- LISTADO DE HUÉSPEDES REGISTRADOS ---")
            lista = huesped_dao.listar()
            if not lista:
                print("ℹ️  No hay huéspedes registrados en el sistema.")
            else:
                print(f"{'ID':<5} | {'RUT/DOC':<15} | {'NOMBRE':<25} | {'TELÉFONO':<15} | {'EMAIL'}")
                print("-" * 75)
                for h in lista:
                    print(f"{h.id:<5} | {h.rut:<15} | {h.nombre:<25} | {h.telefono:<15} | {h.email}")

        elif op == "3":
            print("\n--- MODIFICAR TELÉFONO DE HUÉSPED ---")
            id_h = leer_entero("Ingrese el ID del huésped a modificar: ", minimo=1)
            huesped = huesped_dao.buscar_por_id(id_h)
            if not huesped:
                print(f"❌ No se encontró ningún huésped con ID {id_h}.")
                continue

            print(f"Huésped seleccionado: {huesped.nombre} (Teléfono actual: {huesped.telefono})")
            nuevo_tel = input("Ingrese el nuevo número de teléfono: ").strip()
            huesped.telefono = nuevo_tel
            if huesped_dao.actualizar(huesped):
                print(f"✅ Teléfono actualizado correctamente a '{nuevo_tel}'.")
            else:
                print("❌ No se pudo actualizar el registro.")

        elif op == "4":
            print("\n--- ELIMINAR HUÉSPED ---")
            id_h = leer_entero("Ingrese el ID del huésped a eliminar: ", minimo=1)
            huesped = huesped_dao.buscar_por_id(id_h)
            if not huesped:
                print(f"❌ No se encontró ningún huésped con ID {id_h}.")
                continue

            confirm = input(f"¿Confirma eliminar al huésped '{huesped.nombre}'? (S/N): ").strip().upper()
            if confirm == "S":
                try:
                    if huesped_dao.eliminar(id_h):
                        print(f"✅ Huésped con ID {id_h} eliminado correctamente.")
                    else:
                        print("❌ No se pudo eliminar el huésped.")
                except Exception as e:
                    print(f"❌ No se puede eliminar el huésped porque tiene reservas asociadas ({e}).")
            else:
                print("ℹ️  Operación cancelada.")

        elif op == "5":
            print("\n--- PRUEBA DE VALIDACIÓN DE RUT (MÓDULO 11) ---")
            rut_prueba = input("Ingrese el RUT a comprobar (ej. 12.345.678-5 o 12.345.678-9): ").strip()
            if validar_rut(rut_prueba):
                print(f"✅ El RUT '{formatear_rut(rut_prueba)}' es VÁLIDO.")
            else:
                print(f"❌ El RUT '{rut_prueba}' es INVÁLIDO (Dígito verificador no coincide con Módulo 11).")
                print("ℹ️  El dato fue rechazado y el sistema permanece estable.")

        elif op == "6":
            break
        else:
            print("❌ Opción inválida. Ingrese una opción del 1 al 6.")


# =========================================================================
# 2. TIPOS DE HABITACIÓN Y CÁLCULO POLIMÓRFICO (P09, P10, P11)
# =========================================================================
def mostrar_tarifas_habitaciones(habitacion_dao: HabitacionDAO, servicio_api: MiIndicador):
    print("\n" + "=" * 60)
    print("      🛏️ POLIMORFISMO: TIPOS DE HABITACIÓN Y TARIFAS      ")
    print("=" * 60)
    habitaciones = habitacion_dao.listar()
    if not habitaciones:
        print("ℹ️  No hay habitaciones configuradas.")
        return

    # Obtener el dólar del día desde la API
    valor_dolar, msg_api, en_linea = servicio_api.obtener_dolar()
    print(f"📡 Estado API Dólar: {msg_api}")
    print(f"💵 Tipo de Cambio Utilizado: ${valor_dolar:,.2f} CLP/USD\n")

    noches = leer_entero("Ingrese la cantidad de noches a cotizar: ", minimo=1)

    print("\n" + "-" * 75)
    print(f"{'HAB':<6} | {'TIPO':<12} | {'CAPACIDAD':<11} | {'BASE USD/N':<12} | {'TOTAL ESTADÍA (CLP)'}")
    print("-" * 75)

    for hab in habitaciones:
        # Invocación polimórfica: cada subtipo calcula su tarifa aplicando su propia regla
        total_clp = hab.calcular_tarifa(noches, valor_dolar)
        print(
            f"{hab.numero:<6} | "
            f"{hab.tipo_nombre():<12} | "
            f"{hab.capacidad():<2} persona(s) | "
            f"${hab.precio_base_usd:<11.2f} | "
            f"${total_clp:,.0f} CLP"
        )
    print("-" * 75)
    print("📌 Reglas polimórficas aplicadas:")
    print("   • Individual : Tarifa base estándar por noche (Capacidad: 1 persona).")
    print("   • Doble      : Tarifa base + 10% por desayuno buffet incluido (Capacidad: 2 personas).")
    print("   • Suite      : Tarifa base + 15% por amenities de lujo y salón VIP (Capacidad: 4 personas).")


# =========================================================================
# 3. REGISTRAR ESTADÍA CON CONSUMOS (P12, P13)
# =========================================================================
def registrar_estadia_con_consumos(
    huesped_dao: HuespedDAO,
    habitacion_dao: HabitacionDAO,
    consumo_dao: ConsumoDAO,
    reserva_dao: ReservaDAO,
    servicio_api: MiIndicador
):
    print("\n" + "=" * 60)
    print("        🛎️ REGISTRAR ESTADÍA CON LÍNEAS DE CONSUMO        ")
    print("=" * 60)

    # 1. Seleccionar o crear Huésped
    huespedes = huesped_dao.listar()
    if not huespedes:
        print("⚠️  No hay huéspedes registrados. Creando huésped de prueba...")
        huesped = Huesped(rut="12.345.678-5", nombre="Ana Rojas", telefono="+56911223344", email="ana.rojas@gmail.com")
        huesped_dao.insertar(huesped)
        print(f"✅ Creado huésped: {huesped.nombre} ({huesped.rut})")
    else:
        print("\nHuéspedes disponibles:")
        for h in huespedes[:5]:
            print(f"  [ID: {h.id}] {h.nombre} ({h.rut})")
        id_h = leer_entero("\nIngrese ID del Huésped: ", minimo=1)
        huesped = huesped_dao.buscar_por_id(id_h)
        if not huesped:
            print(f"❌ Huésped #{id_h} no existe.")
            return

    # 2. Seleccionar Habitación
    habitaciones = habitacion_dao.listar()
    print("\nHabitaciones disponibles:")
    for hab in habitaciones:
        print(f"  Habitación N° {hab.numero} ({hab.tipo_nombre()}) - ${hab.precio_base_usd:.2f} USD/noche")
    num_hab = leer_entero("\nIngrese Número de Habitación: ", minimo=1)
    habitacion = habitacion_dao.buscar_por_numero(num_hab)
    if not habitacion:
        print(f"❌ Habitación {num_hab} no existe.")
        return

    # 3. Fechas de estadía
    print("\nIngrese fechas de estadía (formato AAAA-MM-DD):")
    f_inicio = leer_fecha("  Fecha de Check-in  (ej. 2026-10-10): ")
    while True:
        f_fin = leer_fecha("  Fecha de Check-out (ej. 2026-10-13): ")
        if f_fin > f_inicio:
            break
        print("❌ La fecha de salida debe ser posterior a la fecha de inicio.")

    # 4. Obtener Dólar del día
    valor_dolar, msg_api, _ = servicio_api.obtener_dolar()
    print(f"\n📡 {msg_api}")

    # 5. Instanciar la Reserva
    try:
        reserva = Reserva(
            huesped=huesped,
            habitacion=habitacion,
            fecha_inicio=f_inicio,
            fecha_fin=f_fin,
            valor_dolar=valor_dolar,
            anticipo_pagado=0
        )
    except Exception as e:
        print(f"❌ Error al inicializar reserva: {e}")
        return

    # 6. Agregar Líneas de Consumo (Minibar, Room Service, Spa requeridos por P12)
    print("\n--- AGREGAR CONSUMOS ADICIONALES (MINIBAR, ROOM SERVICE, SPA) ---")
    catalogo = consumo_dao.listar()
    for item in catalogo:
        cant = leer_entero(f"¿Desea agregar '{item.nombre}' (${item.precio_unitario:,.0f} CLP)? Ingrese cantidad (0 para omitir): ", minimo=0)
        if cant > 0:
            linea = LineaConsumo(consumo=item, cantidad=cant)
            reserva.agregar_linea_consumo(linea)

    # 7. Anticipo de pago
    print("\n--- RESUMEN DE COBRO ESTIMADO ---")
    print(f"Noches de estadía : {reserva.calcular_noches()}")
    print(f"Total Hospedaje   : ${reserva.total_hospedaje():,.0f} CLP")
    print(f"Total Consumos    : ${reserva.total_consumos():,.0f} CLP")
    print(f"TOTAL CONSOLIDADO : ${reserva.total():,.0f} CLP")
    print(f"Anticipo 50% min. : ${reserva.anticipo_minimo_requerido():,.0f} CLP")

    anticipo = leer_entero("\nIngrese monto abonado como anticipo en CLP: ", minimo=0)
    reserva.anticipo_pagado = anticipo

    # 8. Guardar en Base de Datos aplicando transaccionalidad y Regla 1
    try:
        reserva_dao.insertar(reserva)
        print(f"\n🎉 ¡ESTADÍA Y RESERVA GUARDADA CON ÉXITO! ID ASIGNADO: #{reserva.id}")
        print(f"Se registraron {len(reserva.lineas_detalle)} líneas de consumo asociadas.")
    except HabitacionOcupadaError as e:
        print(f"\n❌ {e}")
        print("ℹ️  La reserva fue rechazada para evitar sobreventa.")
    except Exception as e:
        print(f"\n❌ Error al guardar la transacción: {e}")


# =========================================================================
# 4. CONSULTAR DETALLE DE RESERVA / ESTADÍA (P13)
# =========================================================================
def consultar_detalle_reserva(reserva_dao: ReservaDAO):
    print("\n" + "=" * 60)
    print("      📋 CONSULTAR DETALLE DE ESTADÍA / RESERVA      ")
    print("=" * 60)
    reservas = reserva_dao.listar()
    if not reservas:
        print("ℹ️  No hay reservas registradas en el sistema.")
        return

    print("Reservas registradas:")
    for r in reservas:
        print(f"  [ID #{r.id}] Huésped: {r.huesped.nombre} | Habitación {r.habitacion.numero} ({r.fecha_inicio} al {r.fecha_fin})")

    id_r = leer_entero("\nIngrese el ID de la reserva a detallar: ", minimo=1)
    reserva = reserva_dao.buscar_por_id(id_r)
    if not reserva:
        print(f"❌ No se encontró ninguna reserva con ID #{id_r}.")
        return

    print("\n" + "=" * 65)
    print(f"                 DETALLE DE RESERVA #{reserva.id}")
    print("=" * 65)
    print(f"Huésped          : {reserva.huesped.nombre} (RUT: {reserva.huesped.rut})")
    print(f"Contacto         : Tel {reserva.huesped.telefono} | {reserva.huesped.email}")
    print(f"Habitación       : N° {reserva.habitacion.numero} - {reserva.habitacion.tipo_nombre()} (Piso {reserva.habitacion.piso})")
    print(f"Capacidad Máx.   : {reserva.habitacion.capacidad()} persona(s)")
    print(f"Período Estadía  : Desde {reserva.fecha_inicio} hasta {reserva.fecha_fin} ({reserva.calcular_noches()} noches)")
    print(f"Tipo Cambio USD  : ${reserva.valor_dolar:,.2f} CLP por dólar")
    print(f"Costo Hospedaje  : ${reserva.total_hospedaje():,.0f} CLP")
    print("-" * 65)
    print("LÍNEAS DE DETALLE DE CONSUMOS EXTRAS:")
    if not reserva.lineas_detalle:
        print("  (Sin consumos extras asociados)")
    else:
        for idx, linea in enumerate(reserva.lineas_detalle, 1):
            print(f"  {idx}. {linea.consumo.nombre} ({linea.consumo.codigo}): "
                  f"{linea.cantidad} unid. x ${linea.precio_unitario:,.0f} = ${linea.subtotal():,.0f} CLP")
    print("-" * 65)
    print(f"Subtotal Consumos: ${reserva.total_consumos():,.0f} CLP")
    print(f"TOTAL GENERAL    : ${reserva.total():,.0f} CLP")
    print(f"Anticipo Pagado  : ${reserva.anticipo_pagado:,.0f} CLP")
    print(f"Saldo Pendiente  : ${reserva.saldo_pendiente():,.0f} CLP")
    estado_checkin = "✅ SÍ (Completado)" if reserva.check_in_realizado else "⏳ NO (Pendiente)"
    print(f"Check-in         : {estado_checkin}")
    print("=" * 65)


# =========================================================================
# 5. DEMOSTRACIÓN REGLA 1: HABITACIÓN OCUPADA (P14)
# =========================================================================
def demo_regla_habitacion_ocupada(huesped_dao: HuespedDAO, habitacion_dao: HabitacionDAO, reserva_dao: ReservaDAO):
    print("\n" + "=" * 65)
    print("  🚨 DEMOSTRACIÓN REGLA 1: HABITACIÓN YA OCUPADA (PRUEBA P14)  ")
    print("=" * 65)
    print("Objetivo: Reservar la habitación 101 del 10 al 12 de octubre.")
    print("Luego intentar reservar la misma habitación del 11 al 13 de octubre.")
    print("Resultado esperado: La segunda reserva es bloqueada por HabitacionOcupadaError.")
    print("-" * 65)

    # 1. Asegurar huésped
    huesped = huesped_dao.buscar_por_rut("12.345.678-5")
    if not huesped:
        huesped = Huesped(rut="12.345.678-5", nombre="Ana Rojas", telefono="+56911223344", email="ana.rojas@gmail.com")
        huesped_dao.insertar(huesped)

    hab_101 = habitacion_dao.buscar_por_numero(101)

    print("\n▶ PASO 1: Intentando registrar Reserva 1 (Hab 101 del 2026-10-10 al 2026-10-12)...")
    try:
        r1 = Reserva(huesped, hab_101, "2026-10-10", "2026-10-12", valor_dolar=950.0, anticipo_pagado=50000)
        reserva_dao.insertar(r1)
        print(f"✅ Reserva 1 creada con éxito (ID #{r1.id}) para las fechas 2026-10-10 al 2026-10-12.")
    except HabitacionOcupadaError:
        print("ℹ️  La Reserva 1 ya se encontraba registrada previamente en la base de datos.")

    print("\n▶ PASO 2: Intentando registrar Reserva 2 (Misma Hab 101 del 2026-10-11 al 2026-10-13)...")
    try:
        r2 = Reserva(huesped, hab_101, "2026-10-11", "2026-10-13", valor_dolar=950.0, anticipo_pagado=50000)
        reserva_dao.insertar(r2)
        print("❌ Error: El sistema permitió la reserva cuando debió haberla impedido.")
    except HabitacionOcupadaError as e:
        print("\n🛡️ ¡EXCEPCIÓN PROPIA CAPTURADA CORRECTAMENTE (try/except)!")
        print(f"Tipo de Excepción: {type(e).__name__}")
        print(f"Mensaje de Error : {e}")
        print("✅ Resultado: La segunda reserva fue bloqueada con éxito y el sistema sigue operativo.")


# =========================================================================
# 6. DEMOSTRACIÓN REGLA 2: CHECK-IN CON ANTICIPO INSUFICIENTE (P15)
# =========================================================================
def demo_regla_anticipo_checkin(huesped_dao: HuespedDAO, habitacion_dao: HabitacionDAO):
    print("\n" + "=" * 65)
    print("  🚨 DEMOSTRACIÓN REGLA 2: ANTICIPO INSUFICIENTE (< 50%) (PRUEBA P15)  ")
    print("=" * 65)
    print("Objetivo: Crear reserva con un pago del 40% del hospedaje e intentar Check-in.")
    print("Resultado esperado: El Check-in se bloquea lanzando AnticipoInsuficienteError.")
    print("-" * 65)

    huesped = huesped_dao.buscar_por_rut("12.345.678-5")
    if not huesped:
        huesped = Huesped(rut="12.345.678-5", nombre="Ana Rojas", telefono="+56911223344", email="ana.rojas@gmail.com")

    hab_102 = habitacion_dao.buscar_por_numero(102) # Doble
    reserva_prueba = Reserva(
        huesped=huesped,
        habitacion=hab_102,
        fecha_inicio="2026-11-01",
        fecha_fin="2026-11-04",
        valor_dolar=950.0
    )

    costo_hospedaje = reserva_prueba.total_hospedaje()
    minimo_50 = reserva_prueba.anticipo_minimo_requerido()
    pago_40 = round(costo_hospedaje * 0.40)
    reserva_prueba.anticipo_pagado = pago_40

    print(f"Habitación Reservada  : Hab N° {hab_102.numero} ({hab_102.tipo_nombre()})")
    print(f"Total Hospedaje       : ${costo_hospedaje:,.0f} CLP")
    print(f"Anticipo Requerido 50%: ${minimo_50:,.0f} CLP")
    print(f"Anticipo Abonado (40%): ${pago_40:,.0f} CLP")

    print("\n▶ Ejecutando: reserva.realizar_check_in()...")
    try:
        reserva_prueba.realizar_check_in()
        print("❌ Error: Se permitió el Check-in sin cumplir con el 50% de anticipo.")
    except AnticipoInsuficienteError as e:
        print("\n🛡️ ¡EXCEPCIÓN PROPIA CAPTURADA CORRECTAMENTE (try/except)!")
        print(f"Tipo de Excepción: {type(e).__name__}")
        print(f"Mensaje de Error : {e}")
        print("✅ Resultado: El Check-in fue bloqueado con éxito y el sistema sigue operativo.")


# =========================================================================
# 7. CONSULTAR DÓLAR OFICIAL EN LÍNEA (P16, P17)
# =========================================================================
def consultar_dolar_en_linea(servicio_api: MiIndicador):
    print("\n" + "=" * 60)
    print("      🌐 CONSULTA DE API EXTERNA: DÓLAR OBSERVADO      ")
    print("=" * 60)
    print("Consultando endpoint: https://mindicador.cl/api/dolar ...")

    valor, mensaje, en_linea = servicio_api.obtener_dolar()
    print(f"\n{mensaje}")
    if en_linea:
        print("🟢 Modo Conectado: Valor sincronizado en tiempo real con el Banco Central de Chile.")
    else:
        print("🟠 Modo Desconectado: El sistema notificó la incidencia y sigue funcionando de forma continua.")


# =========================================================================
# PROGRAMA PRINCIPAL
# =========================================================================
def main():
    try:
        conexion = crear_conexion()
        huesped_dao = HuespedDAO(conexion)
        habitacion_dao = HabitacionDAO(conexion)
        consumo_dao = ConsumoDAO(conexion)
        reserva_dao = ReservaDAO(conexion)

        # Crear tablas e inicializar datos maestros
        huesped_dao.crear_tabla()
        habitacion_dao.crear_tabla()
        consumo_dao.crear_tabla()
        reserva_dao.crear_tablas()

        servicio_api = MiIndicador(timeout=5)
    except Exception as e:
        print(f"❌ Error fatal al inicializar base de datos: {e}")
        sys.exit(1)

    while True:
        opcion = mostrar_menu_principal()

        if opcion == "1":
            submenu_huespedes(huesped_dao)
        elif opcion == "2":
            mostrar_tarifas_habitaciones(habitacion_dao, servicio_api)
        elif opcion == "3":
            registrar_estadia_con_consumos(huesped_dao, habitacion_dao, consumo_dao, reserva_dao, servicio_api)
        elif opcion == "4":
            consultar_detalle_reserva(reserva_dao)
        elif opcion == "5":
            demo_regla_habitacion_ocupada(huesped_dao, habitacion_dao, reserva_dao)
        elif opcion == "6":
            demo_regla_anticipo_checkin(huesped_dao, habitacion_dao)
        elif opcion == "7":
            consultar_dolar_en_linea(servicio_api)
        elif opcion == "8":
            print("\n👋 Cerrando sesión en Hotel Boutique Los Alerces. ¡Hasta pronto!")
            conexion.close()
            break
        else:
            # Prueba P18: Opción que no existe (ej. 99)
            print(f"\n❌ Opción '{opcion}' inválida. Por favor seleccione una opción del 1 al 8.")


if __name__ == "__main__":
    main()
