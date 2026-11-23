"""
Pruebas unitarias del sistema (unittest, incluido en Python).

Ejecutar desde la raíz del proyecto:
    python -m unittest discover -s tests -v
"""

import json
import tempfile
import unittest
from pathlib import Path

from transacciones.config import COMISION_FIJA_DEBITO, TASA_INTERES_CREDITO
from transacciones.gestor import GestorTransacciones
from transacciones.lector import leer_y_almacenar_datos
from transacciones.modelos import (
    TransaccionBase, TransaccionCredito, TransaccionDebito, crear_transaccion,
)
from transacciones.persistencia import (
    cargar_desde_archivo, deserializar, guardar_en_archivo, serializar,
)


class PruebasModelos(unittest.TestCase):
    def test_encapsulamiento_rechaza_monto_negativo(self):
        with self.assertRaises(ValueError):
            crear_transaccion("C1", "CREDITO", -1)

    def test_encapsulamiento_rechaza_monto_no_numerico(self):
        with self.assertRaises(ValueError):
            crear_transaccion("C1", "DEBITO", "mucho")

    def test_setter_valida_despues_de_crear(self):
        t = crear_transaccion("C1", "DEBITO", 100)
        with self.assertRaises(ValueError):
            t.monto = -5
        self.assertEqual(t.monto, 100.0)

    def test_clase_base_es_abstracta(self):
        with self.assertRaises(TypeError):
            TransaccionBase("C1", 100)

    def test_herencia_y_fabrica(self):
        self.assertIsInstance(crear_transaccion("C1", "credito", 10), TransaccionCredito)
        self.assertIsInstance(crear_transaccion("C2", "DEBITO", 10), TransaccionDebito)

    def test_tipo_desconocido(self):
        with self.assertRaises(ValueError):
            crear_transaccion("C1", "EFECTIVO", 10)

    def test_polimorfismo_del_impacto(self):
        credito = crear_transaccion("C1", "CREDITO", 1000)
        debito = crear_transaccion("C2", "DEBITO", 1000)
        self.assertAlmostEqual(credito.calcular_impacto(), 1000 * TASA_INTERES_CREDITO)
        self.assertEqual(debito.calcular_impacto(), COMISION_FIJA_DEBITO)


class PruebasGestor(unittest.TestCase):
    def test_totales_y_filtros(self):
        gestor = GestorTransacciones([
            crear_transaccion("C1", "CREDITO", 1000),
            crear_transaccion("C2", "DEBITO", 500),
        ])
        self.assertEqual(gestor.calcular_monto_total(), 1500)
        self.assertEqual(len(gestor.filtrar_por_tipo("DEBITO")), 1)
        self.assertEqual(gestor.resumen()["creditos"], 1)


class PruebasLector(unittest.TestCase):
    def test_una_linea_mala_no_detiene_la_carga(self):
        contenido = "C1,DEBITO,100\nC2,CREDITO,texto\nC3,CREDITO\nC4,CREDITO,-5\nC5,CREDITO,200\n"
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "datos.txt"
            ruta.write_text(contenido, encoding="utf-8")
            validas, rechazadas = leer_y_almacenar_datos(ruta)
        self.assertEqual([t.transaccion_id for t in validas], ["C1", "C5"])
        self.assertEqual([r[0] for r in rechazadas], [2, 3, 4])

    def test_archivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            leer_y_almacenar_datos("no_existe.txt")


class PruebasPersistencia(unittest.TestCase):
    def test_ida_y_vuelta_de_un_objeto(self):
        original = crear_transaccion("C1", "CREDITO", 700000)
        nuevo = deserializar(serializar(original))
        self.assertEqual(nuevo.obtener_informacion(), original.obtener_informacion())

    def test_json_mal_formado(self):
        with self.assertRaises(ValueError):
            deserializar('{"transaccion_id": "C1", "tipo": "CREDITO"')

    def test_faltan_claves(self):
        with self.assertRaises(ValueError):
            deserializar('{"transaccion_id": "C1", "tipo": "DEBITO"}')

    def test_archivo_con_registros_danados(self):
        registros = [
            {"transaccion_id": "C1", "tipo": "DEBITO", "monto": 100},
            {"transaccion_id": "C2", "tipo": "CREDITO"},
            {"transaccion_id": "C3", "tipo": "EFECTIVO", "monto": 5},
        ]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "t.json"
            ruta.write_text(json.dumps(registros), encoding="utf-8")
            objetos, rechazos = cargar_desde_archivo(ruta)
        self.assertEqual(len(objetos), 1)
        self.assertEqual(len(rechazos), 2)

    def test_guardar_y_recargar(self):
        originales = [crear_transaccion("C1", "DEBITO", 10), crear_transaccion("C2", "CREDITO", 20)]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "sub" / "t.json"
            guardar_en_archivo(originales, ruta)
            recargados, rechazos = cargar_desde_archivo(ruta)
        self.assertEqual(len(recargados), 2)
        self.assertEqual(rechazos, [])


if __name__ == "__main__":
    unittest.main()
