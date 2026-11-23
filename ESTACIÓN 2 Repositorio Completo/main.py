"""
main.py
Punto de entrada del Sistema de Gestión de Transacciones (Estación 2).

Integra los componentes de las semanas 3, 4 y 5:
    - POO (encapsulamiento, herencia, polimorfismo) ... transacciones.modelos
    - Tolerancia a fallos (try-except + logging) ...... transacciones.lector
    - Serialización y persistencia JSON ............... transacciones.persistencia
    - Reportes abiertos a extensión (OCP) ............. transacciones.reportes

Uso:
    python main.py
    python main.py --entrada datos/transacciones_corruptas.txt
    python main.py --reporte json
"""

import argparse
import logging
import sys
from pathlib import Path

from transacciones.gestor import GestorTransacciones
from transacciones.lector import leer_y_almacenar_datos
from transacciones.persistencia import cargar_desde_archivo, guardar_en_archivo
from transacciones.reportes import FORMATOS_REPORTE

BASE = Path(__file__).parent
ENTRADA_POR_DEFECTO = BASE / "datos" / "Transacciones.txt"
SALIDA_JSON = BASE / "salida" / "transacciones.json"
ARCHIVO_LOG = BASE / "registro_errores.log"


def configurar_logging():
    """Los avisos van a consola y a un archivo de auditoría (registro_errores.log)."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(ARCHIVO_LOG, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def leer_argumentos(argv=None):
    parser = argparse.ArgumentParser(description="Sistema de gestión de transacciones.")
    parser.add_argument("--entrada", type=Path, default=ENTRADA_POR_DEFECTO,
                        help="Archivo .txt con líneas ID,TIPO,MONTO.")
    parser.add_argument("--reporte", choices=FORMATOS_REPORTE, default="texto",
                        help="Formato del reporte final.")
    return parser.parse_args(argv)


def ejecutar_sistema(argv=None):
    """Flujo completo: leer -> procesar -> persistir -> recargar -> reportar."""
    args = leer_argumentos(argv)
    configurar_logging()

    print("--- INICIO DEL SISTEMA ---")

    # 1) Lectura tolerante a fallos.
    try:
        transacciones, rechazadas = leer_y_almacenar_datos(args.entrada)
    except FileNotFoundError:
        print(f"ERROR: no se encontró el archivo '{args.entrada}'.")
        return 1

    # 2) Procesamiento (polimorfismo).
    gestor = GestorTransacciones(transacciones)
    print("\n--- Transacciones cargadas ---")
    for t in transacciones:
        print(f"{t.obtener_informacion()} | impacto: ${t.calcular_impacto():,.2f} "
              f"[{type(t).__name__}]")

    # 3) Persistencia: guardar y volver a cargar desde JSON.
    guardar_en_archivo(transacciones, SALIDA_JSON)
    recargadas, rechazos_json = cargar_desde_archivo(SALIDA_JSON)
    coinciden = len(recargadas) == len(transacciones) and all(
        a.calcular_impacto() == b.calcular_impacto()
        for a, b in zip(transacciones, recargadas)
    )
    print(f"\nPersistencia JSON: {len(recargadas)} objetos reconstruidos "
          f"({len(rechazos_json)} rechazados). Resultado idéntico: "
          f"{'SI' if coinciden else 'NO'}")

    # 4) Reporte final en el formato elegido.
    reporte = FORMATOS_REPORTE[args.reporte]()
    print("\n" + reporte.generar(gestor.resumen(), rechazadas))
    print("\n--- FIN DEL SISTEMA ---")
    return 0


if __name__ == "__main__":
    sys.exit(ejecutar_sistema())
