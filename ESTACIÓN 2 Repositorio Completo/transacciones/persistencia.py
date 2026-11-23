"""
persistencia.py
Serialización y deserialización de transacciones en formato JSON.

    Serializar   : Objeto -> Diccionario -> Texto JSON
    Deserializar : Texto JSON -> Diccionario -> Objeto

El módulo json no conoce nuestras clases, por eso el diccionario es la escala
intermedia obligatoria. Al serializar solo viajan los DATOS; los métodos
vuelven cuando el constructor reconstruye el objeto.
"""

import json
import logging

from .modelos import crear_transaccion

logger = logging.getLogger(__name__)

# Claves que todo diccionario debe traer para poder reconstruir el objeto.
CLAVES_OBLIGATORIAS = ("transaccion_id", "tipo", "monto")


# ---------------------------------------------------------------------------
# Serialización
# ---------------------------------------------------------------------------
def objeto_a_diccionario(transaccion):
    """Escala 1: convierte el objeto en un diccionario con solo sus datos."""
    return {
        "transaccion_id": transaccion.transaccion_id,
        "tipo": transaccion.tipo,
        "monto": transaccion.monto,
    }


def serializar(transaccion):
    """Objeto -> Diccionario -> cadena de texto JSON (devuelve un str)."""
    return json.dumps(objeto_a_diccionario(transaccion))


# ---------------------------------------------------------------------------
# Deserialización
# ---------------------------------------------------------------------------
def diccionario_a_objeto(como_dict):
    """Usa las claves del diccionario para llamar al constructor.

    Valida que venga completo y que los datos sean aceptados por los setters.

    Raises:
        ValueError: Si no es un diccionario, faltan claves o los datos son inválidos.
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
        raise ValueError(f"Algún dato tiene un tipo incorrecto: {como_dict}.")


def deserializar(texto_json):
    """Texto JSON -> Diccionario -> Objeto, con manejo de errores.

    Raises:
        ValueError: Si el texto no es JSON válido o los datos no sirven.
    """
    try:
        como_dict = json.loads(texto_json)
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON mal formado: {error.msg} (posición {error.pos}).")
    return diccionario_a_objeto(como_dict)


# ---------------------------------------------------------------------------
# Persistencia en archivo
# ---------------------------------------------------------------------------
def guardar_en_archivo(transacciones, ruta):
    """Guarda una lista de objetos en un archivo JSON (crea la carpeta si falta)."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    lista_de_dicts = [objeto_a_diccionario(t) for t in transacciones]
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(lista_de_dicts, archivo, indent=4, ensure_ascii=False)
    logger.info("Guardadas %d transacciones en '%s'.", len(lista_de_dicts), ruta)


def cargar_desde_archivo(ruta):
    """Lee un archivo JSON y reconstruye los objetos, aislando los errores.

    Si un registro está dañado se anota como rechazado y se continúa con el
    siguiente (misma idea de recuperación de la lectura del .txt).

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

    objetos, rechazos = [], []
    for numero, registro in enumerate(contenido, start=1):
        try:
            objetos.append(diccionario_a_objeto(registro))
        except ValueError as error:
            rechazos.append((numero, str(error)))
            logger.warning("Registro %d rechazado: %s", numero, error)
    return objetos, rechazos
