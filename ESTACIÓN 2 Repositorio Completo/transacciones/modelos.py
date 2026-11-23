"""
modelos.py
Clases del dominio: encapsulamiento, herencia y polimorfismo (POO).

    1. Encapsulamiento .... atributos privados con getters y setters validados.
    2. Herencia ........... TransaccionBase -> TransaccionCredito / TransaccionDebito.
    3. Polimorfismo ....... calcular_impacto() distinto en cada clase hija.

Principios SOLID aplicados:
    SRP: cada clase tiene un solo trabajo (la base protege los datos comunes,
         cada hija conoce su propio impacto).
    OCP: para agregar un tipo nuevo (por ejemplo, una transferencia) se crea
         una clase hija y se registra en TIPOS_TRANSACCION, sin modificar
         TransaccionBase ni el resto del sistema.
"""

from abc import ABC, abstractmethod

from .config import COMISION_FIJA_DEBITO, TASA_INTERES_CREDITO


class TransaccionBase(ABC):
    """Clase base de todas las transacciones.

    Es abstracta: no se crean objetos directamente de ella, solo de sus clases
    hijas, que deben implementar ``calcular_impacto``.

    Atributos privados (por convención, con guion bajo inicial):
        _transaccion_id (str): Identificador de la transacción.
        _monto (float): Valor de la transacción, nunca negativo.
    """

    # Cada clase hija define su propio tipo (CREDITO, DEBITO, etc.).
    TIPO = None

    def __init__(self, transaccion_id, monto):
        """Crea la transacción validando los datos desde el primer momento.

        Se asigna con ``self.transaccion_id = ...`` (sin guion bajo) a propósito:
        así se ejecutan los setters y la validación corre también al crear el
        objeto, no solo cuando se modifica después.

        Args:
            transaccion_id (str): Identificador de la transacción.
            monto (float | str): Valor de la transacción; se convierte a float.

        Raises:
            ValueError: Si el ID está vacío o el monto es inválido o negativo.
        """
        self.transaccion_id = transaccion_id
        self.monto = monto

    # ----- Getters y setters con validación --------------------------------
    @property
    def transaccion_id(self):
        """Getter: devuelve el ID de la transacción."""
        return self._transaccion_id

    @transaccion_id.setter
    def transaccion_id(self, nuevo_id):
        """Setter: valida que el ID sea un texto no vacío."""
        if not isinstance(nuevo_id, str) or not nuevo_id.strip():
            raise ValueError("El ID de la transacción no puede estar vacío.")
        self._transaccion_id = nuevo_id.strip()

    @property
    def monto(self):
        """Getter: devuelve el monto de la transacción."""
        return self._monto

    @monto.setter
    def monto(self, nuevo_monto):
        """Setter: convierte a float y asegura que el monto no sea negativo."""
        try:
            valor = float(nuevo_monto)
        except (TypeError, ValueError):
            raise ValueError(f"Monto no numérico: '{nuevo_monto}'.")
        if valor < 0:
            raise ValueError(f"El monto no puede ser negativo: {valor}.")
        self._monto = valor

    @property
    def tipo(self):
        """Getter de solo lectura: el tipo lo define la clase, no se cambia."""
        return self.TIPO

    # ----- Lógica común a todos los tipos ----------------------------------
    def es_tipo(self, tipo_filtro):
        """Indica si la transacción es del tipo consultado (sin distinguir mayúsculas)."""
        return self.tipo == tipo_filtro.strip().upper()

    def obtener_informacion(self):
        """Devuelve una descripción legible con ID, tipo y monto en moneda."""
        return (
            f"Transacción {self.transaccion_id} | "
            f"Tipo: {self.tipo} | Monto: ${self.monto:,.2f}"
        )

    @abstractmethod
    def calcular_impacto(self):
        """Calcula el costo adicional de la transacción (cada hija lo sobrescribe).

        Returns:
            float: Valor del impacto en pesos.
        """


class TransaccionCredito(TransaccionBase):
    """Transacción de crédito: su impacto es el interés sobre el monto."""

    TIPO = "CREDITO"

    def calcular_impacto(self):
        """Devuelve el interés generado: monto * TASA_INTERES_CREDITO."""
        return self.monto * TASA_INTERES_CREDITO


class TransaccionDebito(TransaccionBase):
    """Transacción de débito: su impacto es una comisión fija."""

    TIPO = "DEBITO"

    def calcular_impacto(self):
        """Devuelve la comisión fija, que no depende del monto."""
        return COMISION_FIJA_DEBITO


# Registro de tipos: relaciona el texto del archivo con la clase que lo maneja.
# Para extender el sistema (OCP) se crea una clase nueva y se agrega aquí.
TIPOS_TRANSACCION = {
    TransaccionCredito.TIPO: TransaccionCredito,
    TransaccionDebito.TIPO: TransaccionDebito,
}


def crear_transaccion(transaccion_id, tipo, monto):
    """Fábrica: crea el objeto de la clase hija que corresponde al tipo.

    Args:
        transaccion_id (str): Identificador de la transacción.
        tipo (str): "CREDITO" o "DEBITO" (no distingue mayúsculas).
        monto (float | str): Valor de la transacción.

    Returns:
        TransaccionBase: Instancia de TransaccionCredito o TransaccionDebito.

    Raises:
        ValueError: Si el tipo no está registrado o los datos son inválidos.
    """
    if not isinstance(tipo, str):
        raise ValueError(f"El tipo debe ser texto, se recibió: {tipo!r}.")
    clase = TIPOS_TRANSACCION.get(tipo.strip().upper())
    if clase is None:
        raise ValueError(
            f"Tipo de transacción inválido: '{tipo}'. "
            f"Use {tuple(TIPOS_TRANSACCION)}."
        )
    return clase(transaccion_id, monto)
