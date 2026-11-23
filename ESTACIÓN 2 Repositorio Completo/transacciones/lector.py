"""
lector.py
Lectura de archivos de texto tolerante a fallos (try-except).

Si una línea falla, se registra en el log y el programa CONTINÚA con la
siguiente: un registro corrupto no tumba la carga de los demás.

Formato esperado por línea: ``ID,TIPO,MONTO`` (ej. ``C001,DEBITO,2500000``).
"""

import logging

from .modelos import crear_transaccion

logger = logging.getLogger(__name__)

COLUMNAS_ESPERADAS = 3


def leer_y_almacenar_datos(nombre_archivo):
    """Lee el archivo y devuelve los objetos válidos y las líneas rechazadas.

    El ``try`` vive DENTRO del bucle: así cada línea se protege por separado.
    Los errores posibles son:
        - Faltan columnas -> ValueError (datos insuficientes).
        - Tipo desconocido, monto no numérico o negativo -> ValueError lanzado
          por la fábrica y los setters de las clases (encapsulamiento).

    Args:
        nombre_archivo (str | Path): Ruta del archivo de texto.

    Returns:
        tuple[list[TransaccionBase], list[tuple]]: Lista principal de objetos y
        lista de rechazos con el formato ``(numero_linea, texto_linea, motivo)``.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    lista_transacciones = []
    lineas_rechazadas = []

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            linea = linea.strip()
            if not linea:
                continue  # se ignoran las líneas en blanco

            try:
                partes = [parte.strip() for parte in linea.split(",")]
                if len(partes) != COLUMNAS_ESPERADAS:
                    raise ValueError(
                        f"Datos insuficientes: se esperaban {COLUMNAS_ESPERADAS} "
                        f"columnas y llegaron {len(partes)}."
                    )
                lista_transacciones.append(crear_transaccion(*partes))
            except ValueError as error:
                # Estrategia de recuperación: dejar constancia y continuar.
                lineas_rechazadas.append((numero_linea, linea, str(error)))
                logger.warning("Línea %d rechazada (%s): %s", numero_linea, linea, error)

    logger.info(
        "Lectura de '%s': %d válidas, %d rechazadas.",
        nombre_archivo, len(lista_transacciones), len(lineas_rechazadas),
    )
    return lista_transacciones, lineas_rechazadas
