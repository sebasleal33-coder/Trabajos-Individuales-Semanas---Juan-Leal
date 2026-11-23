"""
gestor.py
Operaciones sobre un conjunto de transacciones.

SRP: esta clase solo procesa listas de objetos; no lee archivos, no guarda
JSON y no da formato a reportes (eso lo hacen otros módulos).
"""


class GestorTransacciones:
    """Agrupa las operaciones sobre la lista principal de transacciones.

    Atributos:
        transacciones (list[TransaccionBase]): Lista principal de objetos.
    """

    def __init__(self, transacciones):
        """Recibe la lista principal de objetos."""
        self.transacciones = transacciones

    def calcular_monto_total(self):
        """Suma el monto de todas las transacciones."""
        return sum(t.monto for t in self.transacciones)

    def filtrar_por_tipo(self, tipo_filtro):
        """Devuelve las transacciones que coinciden con el tipo indicado."""
        return [t for t in self.transacciones if t.es_tipo(tipo_filtro)]

    def calcular_impacto_total(self):
        """Suma el impacto de todas las transacciones (polimorfismo).

        No se pregunta de qué tipo es cada transacción: se llama siempre a
        ``calcular_impacto()`` y cada objeto responde según su clase.
        """
        return sum(t.calcular_impacto() for t in self.transacciones)

    def resumen(self):
        """Resume el estado del conjunto en un diccionario.

        Returns:
            dict: Cantidades por tipo, monto total e impacto total.
        """
        return {
            "total_transacciones": len(self.transacciones),
            "creditos": len(self.filtrar_por_tipo("CREDITO")),
            "debitos": len(self.filtrar_por_tipo("DEBITO")),
            "monto_total": self.calcular_monto_total(),
            "impacto_total": self.calcular_impacto_total(),
        }
