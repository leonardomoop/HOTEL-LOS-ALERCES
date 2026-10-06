# Sistema de Gestión - Hotel Boutique Los Alerces

**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Sección:** 114-2A-F2  
**Docente:** Michael Arjel  
**Institución:** INACAP Sede Puente Alto  
**Semestre:** Primavera 2026  

### Integrantes del Equipo
* **Cindy Carrasco**
* **Leonardo Mora**

---

## 1. Descripción del Negocio
El **Hotel Boutique Los Alerces** requiere un sistema centralizado para gestionar las estadías de sus huéspedes, controlando el registro de clientes, reservas por fechas, aseo de dependencias, facturación consolidada y catálogo de consumos adicionales (minibar, room service, spa).

El sistema aplica los requerimientos críticos del negocio:
1. **Polimorfismo en Habitaciones:** Diferenciación de tarifas y capacidades según el subtipo de habitación (`HabitacionIndividual`, `HabitacionDoble`, `Suite`).
2. **Consumo de API Externa:** Conversión de tarifas en dólares a pesos chilenos según el valor oficial diario obtenido en tiempo real desde la API pública `https://mindicador.cl/api/dolar`.
3. **Persistencia Transaccional con Detalle:** Registro de reservas cabecera asociadas a múltiples líneas de detalle de consumos extras en base de datos SQLite.
4. **Reglas Críticas del Negocio (Excepciones Propias):**
   * **Regla 1 (`HabitacionOcupadaError`):** No permite reservar una habitación si ya existe una reserva solapada en ese rango de fechas.
   * **Regla 2 (`AnticipoInsuficienteError`):** Bloquea el check-in si el cliente no ha pagado al menos el 50% de anticipo del hospedaje.
5. **Validación de Entradas:** Validación estricta del formato de documentos de identidad chilenos (RUT mediante algoritmo Módulo 11) y sanitización de todas las entradas del usuario.

---

## 2. Requisitos e Instalación

### Requisitos Previos
* Python 3.10 o superior instalado en el equipo.
* Conexión a internet (para sincronización del valor del dólar en tiempo real).

### Instalación de Dependencias
Clone o descargue el repositorio y, dentro de la carpeta del proyecto, ejecute en la terminal:

```bash
pip install -r requirements.txt
```

*(Dependencia principal: `requests` para el consumo de la API REST).*

---

## 3. Instrucciones de Ejecución

Para iniciar el sistema de gestión por consola, ejecute:

```bash
python main.py
```

El programa inicializará automáticamente el archivo de base de datos local `hotel.db`, creará las tablas necesarias si no existen e insertará las habitaciones y consumos iniciales para operar de inmediato.

---

## 4. Decisiones de Seguridad Implementadas

En cumplimiento con los aprendizajes esperados de **Programación Orientada a Objeto Seguro**, se aplicaron las siguientes decisiones de diseño y arquitectura de software:

### 4.1. Prevención de Inyección SQL (SQL Injection)
* **Separación de Capas (Patrón DAO):** Ninguna clase del modelo (`model/`) contiene instrucciones SQL. Todas las operaciones de base de datos están aisladas en la capa `dao/`.
* **Consultas 100% Parametrizadas:** Se utiliza exclusivamente el mecanismo de reemplazo por marcadores de posición (`?`) provisto por la librería oficial `sqlite3`. En ninguna parte del código se realiza concatenación o interpolación de strings (`f-strings`) dentro de las consultas SQL, neutralizando cualquier intento de inyección de comandos maliciosos.
* **Integridad Referencial:** Se habilita explícitamente `PRAGMA foreign_keys = ON;` al conectar, garantizando la consistencia de las relaciones entre huéspedes, habitaciones, reservas y líneas de consumo.

### 4.2. Encapsulamiento y Validación en el Modelo
* **Atributos Privados:** Todos los atributos del modelo están protegidos mediante convención de doble guion bajo (`__atributo`).
* **Propiedades con Validación en Setters:** El acceso y modificación de los datos se realiza a través de decoradores `@property` y `@setter`. Los setters aplican validaciones de tipo, longitud y formato antes de asignar el valor a la variable privada, previniendo estados inconsistentes en los objetos de memoria.

### 4.3. Validación Robusta de Entradas y Estabilidad
* **Validación de RUT con Algoritmo Módulo 11:** Se implementó una función matemática que descompone el cuerpo numérico y calcula el dígito verificador exacto (incluyendo el caso especial `'K'`). Si el usuario ingresa un RUT incorrecto (como `12.345.678-9`), el sistema lo rechaza con un mensaje claro sin abortar el programa.
* **Control de Tipos Numéricos:** Todas las lecturas por teclado están envueltas en funciones auxiliares (`leer_entero`, `leer_flotante`, `leer_fecha`) con bloques `try / except (ValueError)`. Si el usuario ingresa texto (`"abc"`) en campos numéricos o selecciona opciones fuera de rango (`99`), el sistema notifica el error y solicita nuevamente el dato sin caerse.

### 4.4. Resiliencia en Servicios Externos (API REST)
* **Tiempos de Espera (Timeout):** Las solicitudes HTTP a `mindicador.cl` tienen un timeout máximo configurado de 5 segundos, impidiendo que el hilo de ejecución quede congelado ante problemas de red.
* **Manejo de Contingencia y Alta Disponibilidad:** Se capturan específicamente las excepciones `Timeout`, `ConnectionError` y `RequestException`. Si el equipo no cuenta con conexión a internet o la API se encuentra fuera de servicio, el sistema advierte al operador y utiliza una tasa de cambio de contingencia preestablecida, asegurando la continuidad del negocio.

---

## 5. Documentación de Uso de Herramientas de Inteligencia Artificial (Criterio 3.1.4)

Durante el desarrollo del proyecto se consultaron herramientas de Inteligencia Artificial como asistentes de programación en pares. A continuación, se detallan ejemplos concretos de código sugerido, explicando las decisiones técnicas de adopción, modificación o descarte:

### Ejemplo 1: Validación del Algoritmo Módulo 11 para RUT Chileno
* **Sugerencia Inicial de la IA:** La IA sugirió una expresión regular básica para validar el formato del RUT (`r"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$"`).
* **Decisión Técnica:** **Modificada y Ampliada.**
* **Justificación:** Una expresión regular solo verifica la forma del texto, pero no valida si el dígito verificador es matemáticamente correcto. Si un usuario ingresaba `12.345.678-9`, la expresión regular lo aceptaba como válido a pesar de que el dígito real es `5`. Se reemplazó la sugerencia por la implementación completa del algoritmo de ponderación Módulo 11 (factores del 2 al 7) para garantizar la autenticidad del documento de identidad del huésped.

### Ejemplo 2: Manejo de Excepciones en el Consumo de la API de Dólar
* **Sugerencia Inicial de la IA:** La IA propuso envolver la llamada `requests.get()` en un bloque genérico `except Exception: pass` que silenciaba el error y retornaba `0`.
* **Decisión Técnica:** **Descartada por Insegura.**
* **Justificación:** Silenciar excepciones (`pass`) impide la observabilidad del sistema y retornar `0` en la tasa de cambio provocaría que el costo de las habitaciones se calculara en `$0 CLP`, generando pérdidas críticas para el hotel. En su lugar, se implementó captura granular de `Timeout` y `ConnectionError`, emitiendo una alerta clara en consola y activando una tasa de contingencia segura.

### Ejemplo 3: Transaccionalidad al Guardar Reserva y Líneas de Consumo
* **Sugerencia Inicial de la IA:** La IA sugirió realizar `self.conexion.commit()` inmediatamente después de insertar la cabecera de la reserva y luego otro `commit()` por cada línea de detalle dentro de un bucle `for`.
* **Decisión Técnica:** **Modificada.**
* **Justificación:** Si ocurría un fallo o corte de energía a mitad del bucle de consumos, la cabecera y algunas líneas quedaban guardadas mientras otras se perdían, rompiendo la atomicidad. Se modificó agrupando la cabecera y todas las líneas dentro de un único bloque `try/except` con `commit()` al final y `rollback()` ante cualquier error, garantizando el principio ACID de persistencia.

---

## 6. Estructura del Proyecto

```text
sistema_hotel/
│
├── conectar.py              # Función para establecer conexión SQLite con claves foráneas
├── requirements.txt         # Librerías externas del proyecto (requests)
├── README.md                # Documentación del sistema, seguridad y uso de IA
├── main.py                  # Interfaz de consola interactiva con las 19 pruebas de evaluación
│
├── model/                   # Clases del modelo orientado a objetos (una por archivo)
│   ├── __init__.py
│   ├── excepciones.py       # Excepciones propias del negocio (HabitacionOcupadaError, etc.)
│   ├── persona.py           # Clase base de personas con validación de documentos
│   ├── huesped.py           # Subtipo cliente con historial de reservas
│   ├── empleado.py          # Clase base de personal del hotel
│   ├── recepcionista.py     # Subtipo administrativo
│   ├── camarero.py          # Subtipo operativo (housekeeping)
│   ├── habitacion.py        # Clase base habitacion con método polimórfico calcular_tarifa()
│   ├── habitacion_individual.py # Subtipo Individual (capacidad: 1)
│   ├── habitacion_doble.py  # Subtipo Doble (capacidad: 2, incluye desayuno buffet)
│   ├── suite.py             # Subtipo Suite (capacidad: 4, tarifa premium y servicios VIP)
│   ├── consumo.py           # Catálogo maestro de productos y servicios extras
│   ├── linea_consumo.py     # Línea de detalle con cálculo de subtotal
│   └── reserva.py           # Transacción central, control de anticipo y check-in
│
├── dao/                     # Capa de persistencia en SQLite (separada del modelo)
│   ├── __init__.py
│   ├── dao.py               # Clase base DAO
│   ├── huesped_dao.py       # CRUD completo parametrizado de Huéspedes
│   ├── habitacion_dao.py    # Persistencia y mapeo polimórfico de Habitaciones
│   ├── consumo_dao.py       # Persistencia del catálogo de consumos
│   └── reserva_dao.py       # Transacciones compuestas (cabecera + detalle) y validación de fechas
│
├── servicios/               # Consumo de APIs externas
│   ├── __init__.py
│   └── mi_indicador.py      # Cliente HTTP para mindicador.cl con timeout y modo offline
│
└── utils/                   # Módulos de apoyo y validaciones
    ├── __init__.py
    └── validador.py         # Módulo 11 para RUT chileno y entradas seguras por consola
```
