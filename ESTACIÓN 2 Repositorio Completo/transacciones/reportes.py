"""
reportes.py
Generación de reportes con la estrategia abierta a extensión (OCP).

ReporteBase define el contrato; cada formato es una clase hija. Para agregar
un formato nuevo (por ejemplo XML) se crea otra clase hija y se registra en
FORMATOS_REPORTE, sin modificar el código existente.
"""

import json
from abc import ABC, abstractmethod


class ReporteBase(ABC):
    """Contrato común: recibe el resumen del gestor y devuelve un texto."""

    @abstractmethod
    def generar(self, resumen, rechazadas):
        """Genera el reporte.

        Args:
            resumen (dict): Resultado de ``GestorTransacciones.resumen()``.
            rechazadas (list[tuple]): Líneas rechazadas durante la lectura.

        Returns:
            str: Reporte listo para imprimir o guardar.
        """


class ReporteTexto(ReporteBase):
    """Reporte en texto plano, legible para una persona."""

    def generar(self, resumen, rechazadas):
        lineas = [
            "===== REPORTE DE TRANSACCIONES =====",
            f"Transacciones válidas : {resumen['total_transacciones']}",
            f"  - Créditos          : {resumen['creditos']}",
            f"  - Débitos           : {resumen['debitos']}",
            f"Monto total           : ${resumen['monto_total']:,.2f}",
            f"Impacto total         : ${resumen['impacto_total']:,.2f}",
            f"Líneas rechazadas     : {len(rechazadas)}",
        ]
        for numero, texto, motivo in rechazadas:
            lineas.append(f"  * Línea {numero} ({texto}): {motivo}")
        return "\n".join(lineas)


class ReporteJSON(ReporteBase):
    """Reporte en JSON, pensado para que otro sistema lo consuma."""

    def generar(self, resumen, rechazadas):
        datos = dict(resumen)
        datos["rechazadas"] = [
            {"linea": n, "texto": t, "motivo": m} for n, t, m in rechazadas
        ]
        return json.dumps(datos, indent=4, ensure_ascii=False)


FORMATOS_REPORTE = {
    "texto": ReporteTexto,
    "json": ReporteJSON,
}
