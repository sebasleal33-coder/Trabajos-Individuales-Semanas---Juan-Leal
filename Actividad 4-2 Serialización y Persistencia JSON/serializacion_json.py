"""
serializacion_json.py
Semana 4 - Actividad 2: Serialización y persistencia (JSON).

EL PROBLEMA QUE RESOLVEMOS
--------------------------
Los objetos viven en la MEMORIA de Python: existen mientras el programa corre y
desaparecen cuando termina. Para guardarlos en un disco, meterlos en una base de
datos o enviarlos por internet, hay que convertirlos a un formato de texto que
cualquier sistema entienda. Ese formato universal es JSON.

LA ANALOGÍA DEL VIAJE
---------------------
Serializar es EMPACAR: no puedes enviar tu casa por correo, así que metes su
contenido en una caja plana y etiquetada. El objeto se vuelve texto, y el texto
sí cabe en un archivo o en una petición HTTP.
Deserializar es DESEMPACAR al llegar: tomas la caja y vuelves a armar el objeto.

EL VIAJE COMPLETO, EN DOS ESCALAS
---------------------------------
    Objeto Python  ->  Diccionario  ->  Texto JSON      (serializar)
    Texto JSON     ->  Diccionario  ->  Objeto Python   (deserializar)

La escala del medio, el DICCIONARIO, no es opcional: el módulo json no sabe
traducir un objeto de una clase que nosotros inventamos, pero sí sabe traducir
un diccionario. Por eso primero pasamos por ahí.

Qué se pierde al serializar: los MÉTODOS. El JSON guarda solo los DATOS
(transaccion_id, tipo, monto). Al deserializar, los métodos vuelven porque se
los devuelve la clase cuando llamamos al constructor.

Cómo se conecta con las semanas anteriores:
    - Semana 3: reutilizamos las clases robustas (TransaccionCredito,
      TransaccionDebito) de diseno_pilares_poo.py, sin modificarlas (SRP:
      aquí solo agregamos el trabajo de convertir a/desde JSON).
    - Semana 4 (Act. 1): usamos try-except para que un dato dañado no
      tumbe el programa.

Para ejecutar:  python serializacion_json.py
(Este archivo, diseno_pilares_poo.py y Transacciones.txt deben estar en la
misma carpeta.)
"""

import json
from pathlib import Path

from diseno_pilares_poo import crear_transaccion, leer_y_almacenar_datos

# ---------------------------------------------------------------------------
# Rutas de los archivos (siempre junto a este .py, sin importar desde dónde
# se ejecute el programa)
# ---------------------------------------------------------------------------
CARPETA = Path(__file__).parent
ARCHIVO_ENTRADA = CARPETA / "Transacciones.txt"          # datos de la semana 3
ARCHIVO_JSON = CARPETA / "transacciones.json"            # archivo que vamos a crear
ARCHIVO_DANADO = CARPETA / "transacciones_danadas.json"  # prueba de datos dañados

# Claves que TODO diccionario debe traer para poder reconstruir el objeto.
CLAVES_OBLIGATORIAS = ("transaccion_id", "tipo", "monto")


# ---------------------------------------------------------------------------
# SERIALIZACIÓN:  Objeto -> Diccionario -> Texto JSON
# ---------------------------------------------------------------------------
def objeto_a_diccionario(transaccion):
    """Escala 1: convierte el objeto en un diccionario simple.

    Leemos los atributos del objeto y los copiamos como pares clave-valor.
    Aquí es donde se "pierden" los métodos: solo copiamos DATOS.

    Args:
        transaccion (TransaccionBase): Objeto a convertir.

    Returns:
        dict: Diccionario con transaccion_id, tipo y monto.
    """
    return {
        "transaccion_id": transaccion.transaccion_id,
        "tipo": transaccion.tipo,
        "monto": transaccion.monto,
    }


def serializar(transaccion):
    """Escala 1 + 2: Objeto -> Diccionario -> cadena de texto JSON.

    OJO: json.dumps NO devuelve un diccionario, devuelve un str (texto).

    Args:
        transaccion (TransaccionBase): Objeto a serializar.

    Returns:
        str: Texto en formato JSON.
    """
    como_dict = objeto_a_diccionario(transaccion)
    return json.dumps(como_dict)


# ---------------------------------------------------------------------------
# DESERIALIZACIÓN:  Texto JSON -> Diccionario -> Objeto
# ---------------------------------------------------------------------------
def diccionario_a_objeto(como_dict):
    """Escala final: usa las claves del diccionario para LLAMAR AL CONSTRUCTOR.

    Este paso es manual: json.loads solo llega hasta el diccionario, porque no
    conoce nuestras clases. Además valida que el diccionario venga completo y
    que los datos sean aceptados por los setters de la clase (semana 3).

    Args:
        como_dict (dict): Diccionario con transaccion_id, tipo y monto.

    Returns:
        TransaccionBase: Objeto TransaccionCredito o TransaccionDebito nuevo.

    Raises:
        ValueError: Si no es un diccionario, faltan claves o los datos son
            inválidos (tipo desconocido, monto negativo o no numérico, etc.).
    """
    if not isinstance(como_dict, dict):
        raise ValueError("El JSON no contiene un objeto (diccionario) de transacción.")

    faltantes = [clave for clave in CLAVES_OBLIGATORIAS if clave not in como_dict]
    if faltantes:
        raise ValueError(f"Faltan claves obligatorias: {faltantes}.")

    try:
        return crear_transaccion(
            como_dict["transaccion_id"], como_dict["tipo"], como_dict["monto"]
        )
    except (AttributeError, TypeError):
        # Ocurre cuando un dato tiene el tipo equivocado (ej. tipo = 123).
        raise ValueError(f"Algún dato tiene un tipo incorrecto: {como_dict}.")


def deserializar(texto_json):
    """Texto JSON -> Diccionario -> Objeto, con manejo de errores.

    Args:
        texto_json (str): Cadena de texto en formato JSON.

    Returns:
        TransaccionBase: Objeto reconstruido.

    Raises:
        ValueError: Si el texto no es JSON válido o los datos no sirven.
    """
    try:
        # Escala 1: la cadena JSON vuelve a ser un diccionario.
        como_dict = json.loads(texto_json)
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON mal formado: {error.msg} (posición {error.pos}).")
    # Escala 2: el diccionario vuelve a ser un objeto.
    return diccionario_a_objeto(como_dict)


# ---------------------------------------------------------------------------
# PERSISTENCIA: guardar y leer una LISTA de transacciones en un archivo .json
# ---------------------------------------------------------------------------
def guardar_en_archivo(transacciones, ruta):
    """Guarda una lista de objetos en un archivo JSON (persistencia).

    Args:
        transacciones (list[TransaccionBase]): Objetos a guardar.
        ruta (Path | str): Archivo donde se escribirá el JSON.
    """
    lista_de_dicts = [objeto_a_diccionario(t) for t in transacciones]
    with open(ruta, "w", encoding="utf-8") as archivo:
        # indent=4 deja el archivo ordenado y fácil de leer para una persona.
        json.dump(lista_de_dicts, archivo, indent=4, ensure_ascii=False)


def cargar_desde_archivo(ruta):
    """Lee un archivo JSON y reconstruye los objetos, aislando los errores.

    Si un registro está dañado, se anota como rechazado y se continúa con el
    siguiente (la misma idea de recuperación de la Actividad 4-1).

    Args:
        ruta (Path | str): Archivo JSON a leer.

    Returns:
        tuple[list[TransaccionBase], list[tuple]]: Objetos reconstruidos y
        rechazos con el formato ``(numero_registro, motivo)``.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo no es JSON válido o no contiene una lista.
    """
    with open(ruta, "r", encoding="utf-8") as archivo:
        try:
            contenido = json.load(archivo)
        except json.JSONDecodeError as error:
            raise ValueError(f"El archivo está dañado: {error.msg} (línea {error.lineno}).")

    if not isinstance(contenido, list):
        raise ValueError("El archivo debe contener una lista de transacciones.")

    objetos = []
    rechazos = []
    for numero, registro in enumerate(contenido, start=1):
        try:
            objetos.append(diccionario_a_objeto(registro))
        except ValueError as error:
            rechazos.append((numero, str(error)))
    return objetos, rechazos


# ---------------------------------------------------------------------------
# DEMOSTRACIONES (lo que se ve al ejecutar el programa)
# ---------------------------------------------------------------------------
def demo_viaje_completo():
    """Parte 1: el viaje de UN objeto, escala por escala."""
    print("=" * 70)
    print("PARTE 1: EL VIAJE COMPLETO DE UNA TRANSACCION")
    print("=" * 70)

    original = crear_transaccion("C002", "CREDITO", 700000)
    print("\n[SERIALIZAR]")
    print("1) Objeto original :", original.obtener_informacion())
    print("   Tipo de dato    :", type(original).__name__, "(vive en memoria, tiene métodos)")

    como_dict = objeto_a_diccionario(original)
    print("2) Diccionario     :", como_dict)
    print("   Tipo de dato    :", type(como_dict).__name__)

    texto = json.dumps(como_dict)
    print("3) Texto JSON      :", texto)
    print("   Tipo de dato    :", type(texto).__name__, "(es TEXTO: ya puede viajar o guardarse)")

    print("\n[DESERIALIZAR]")
    de_vuelta = json.loads(texto)
    print("4) Diccionario     :", de_vuelta)
    print("   Tipo de dato    :", type(de_vuelta).__name__, "(json.loads NO crea el objeto)")

    reconstruido = diccionario_a_objeto(de_vuelta)
    print("5) Objeto nuevo    :", reconstruido.obtener_informacion())
    print("   Tipo de dato    :", type(reconstruido).__name__, "(volvió a ser objeto, con sus métodos)")
    print("   Método recuperado -> calcular_impacto():", f"${reconstruido.calcular_impacto():,.2f}")


def demo_casos_de_error():
    """Parte 2: textos JSON dañados y cómo el programa los rechaza sin caerse."""
    print("\n" + "=" * 70)
    print("PARTE 2: MANEJO DE CASOS DE ERROR AL DESERIALIZAR")
    print("=" * 70)

    casos = [
        ("JSON válido (control)",
         '{"transaccion_id": "C020", "tipo": "CREDITO", "monto": 500000}'),
        ("JSON mal formado (falta cerrar la llave)",
         '{"transaccion_id": "C021", "tipo": "CREDITO", "monto": 500000'),
        ("Falta una clave obligatoria (monto)",
         '{"transaccion_id": "C022", "tipo": "DEBITO"}'),
        ("Tipo de transacción no registrado",
         '{"transaccion_id": "C023", "tipo": "EFECTIVO", "monto": 100000}'),
        ("Monto negativo",
         '{"transaccion_id": "C024", "tipo": "CREDITO", "monto": -5000000}'),
        ("Monto no numérico",
         '{"transaccion_id": "C025", "tipo": "DEBITO", "monto": "mucho"}'),
        ("Dato con tipo incorrecto (tipo = 123)",
         '{"transaccion_id": "C026", "tipo": 123, "monto": 1000}'),
        ("El JSON no es un diccionario",
         '[1, 2, 3]'),
    ]

    for numero, (descripcion, texto) in enumerate(casos, start=1):
        print(f"\nCaso {numero}: {descripcion}")
        print("  Texto recibido:", texto)
        try:
            objeto = deserializar(texto)
            print("  ACEPTADO ->", objeto.obtener_informacion())
        except ValueError as error:
            print("  RECHAZADO ->", error)


def demo_persistencia():
    """Parte 3: problema concreto, guardar las transacciones y recuperarlas."""
    print("\n" + "=" * 70)
    print("PARTE 3: PERSISTENCIA - GUARDAR Y RECUPERAR TRANSACCIONES")
    print("=" * 70)

    # 1) Los objetos de la semana 3 (los registros inválidos ya vienen filtrados).
    originales, rechazadas = leer_y_almacenar_datos(ARCHIVO_ENTRADA)
    print(f"\nObjetos cargados desde Transacciones.txt: {len(originales)}")
    print(f"Líneas rechazadas por los setters (semana 3): {len(rechazadas)}")

    # 2) Serializar y guardar en disco.
    guardar_en_archivo(originales, ARCHIVO_JSON)
    print(f"\nArchivo creado: {ARCHIVO_JSON.name}")
    print("Primeras líneas del archivo:")
    with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
        for linea in archivo.readlines()[:12]:
            print("   ", linea.rstrip())
    print("    ...")

    # 3) Deserializar: los objetos vuelven a la memoria.
    reconstruidos, rechazos = cargar_desde_archivo(ARCHIVO_JSON)
    print(f"\nObjetos reconstruidos desde el archivo: {len(reconstruidos)}")

    # 4) Verificación: ¿llegó todo igual? ¿volvieron los métodos?
    iguales = all(
        objeto_a_diccionario(a) == objeto_a_diccionario(b)
        for a, b in zip(originales, reconstruidos)
    )
    impacto_original = sum(t.calcular_impacto() for t in originales)
    impacto_nuevo = sum(t.calcular_impacto() for t in reconstruidos)
    print("Datos idénticos tras ida y vuelta :", "SI" if iguales else "NO")
    print(f"Impacto total (objetos originales)  : ${impacto_original:,.2f}")
    print(f"Impacto total (objetos reconstruidos): ${impacto_nuevo:,.2f}")

    # 5) Archivo con registros dañados: se aíslan y el resto se recupera.
    print("\n--- Archivo con registros dañados ---")
    registros_danados = [
        {"transaccion_id": "C100", "tipo": "DEBITO", "monto": 250000},
        {"transaccion_id": "C101", "tipo": "CREDITO"},
        {"transaccion_id": "C102", "tipo": "EFECTIVO", "monto": 90000},
        {"transaccion_id": "C103", "tipo": "CREDITO", "monto": 800000},
        {"transaccion_id": "C104", "tipo": "DEBITO", "monto": -1},
    ]
    with open(ARCHIVO_DANADO, "w", encoding="utf-8") as archivo:
        json.dump(registros_danados, archivo, indent=4)

    recuperados, rechazos = cargar_desde_archivo(ARCHIVO_DANADO)
    print(f"Registros recuperados: {len(recuperados)} | rechazados: {len(rechazos)}")
    for t in recuperados:
        print("  OK       ->", t.obtener_informacion())
    for numero, motivo in rechazos:
        print(f"  Registro {numero} rechazado -> {motivo}")

    # 6) Errores de archivo: truncado y archivo inexistente.
    print("\n--- Errores a nivel de archivo ---")
    with open(ARCHIVO_DANADO, "w", encoding="utf-8") as archivo:
        archivo.write('[{"transaccion_id": "C200", "tipo": "DEBITO"')  # truncado
    for ruta in (ARCHIVO_DANADO, CARPETA / "no_existe.json"):
        try:
            cargar_desde_archivo(ruta)
        except FileNotFoundError:
            print(f"  {ruta.name}: el archivo no existe.")
        except ValueError as error:
            print(f"  {ruta.name}: {error}")


def ejecutar():
    """Ejecuta las tres demostraciones en orden."""
    demo_viaje_completo()
    demo_casos_de_error()
    demo_persistencia()
    print("\n--- FIN ---")


if __name__ == "__main__":
    ejecutar()