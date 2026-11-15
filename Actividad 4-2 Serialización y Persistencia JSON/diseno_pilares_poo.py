# diseno_pilares_poo.py
"""
Actividad 3-1: Robustez con Encapsulamiento, Herencia y Polimorfismo (POO)

Objetivo:
    Dominar el Diseño Orientado a Objetos (POO) mediante la aplicación práctica
    del Encapsulamiento (visibilidad, Getters/Setters) y los pilares de Herencia
    y Polimorfismo para refactorizar la clase base del proyecto, logrando una
    estructura de código modular, segura y extensible.

Descripción de la Actividad:
    En la Semana 2, el código funcionaba bajo el paradigma POO. Ahora se hace
    robusto y profesional: la clase de transacciones queda segura contra errores
    y fácil de extender, aplicando los principios SOLID (específicamente SRP y
    OCP).

Estructura del módulo:
    1. Encapsulamiento .......... Blindaje de datos (atributos privados,
                                  getters y setters con validación).
    2. Herencia ................. Jerarquía TransaccionBase -> Credito / Debito.
    3. Polimorfismo ............. calcular_impacto() distinto en cada clase hija.

Principios SOLID aplicados:
    SRP (Responsabilidad Única): cada clase tiene un solo trabajo.
        - TransaccionBase ........ guardar y proteger los datos comunes.
        - TransaccionCredito ..... conocer el impacto de un crédito (interés).
        - TransaccionDebito ...... conocer el impacto de un débito (comisión).
        - GestorTransacciones .... procesar listas de transacciones.
    OCP (Abierto/Cerrado): para agregar un nuevo tipo (por ejemplo, una
        transferencia) se crea una clase hija nueva y se registra en
        TIPOS_TRANSACCION, sin modificar TransaccionBase ni GestorTransacciones.
"""

from abc import ABC, abstractmethod

# ---------------------------------------------------------------------------
# Parámetros de negocio (Se dejan en este apartado para que sean fáciles de cambiar)
# ---------------------------------------------------------------------------
# Tasa de interés mensual aplicada a los créditos (0.018 = 1.8 % mensual).
TASA_INTERES_CREDITO = 0.018
# Comisión fija en pesos que se cobra por cada débito.
COMISION_FIJA_DEBITO = 6500


# ---------------------------------------------------------------------------
# 1 y 2. Clase base (Padre) con encapsulamiento
# ---------------------------------------------------------------------------
class TransaccionBase(ABC):
    """Clase base de todas las transacciones.

    Contiene el constructor, los getters/setters con validación y la lógica
    común. Es abstracta: no se crean objetos directamente de ella, solo de sus
    clases hijas, que deben implementar ``calcular_impacto``.

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

    # ----- Getters (lectura) y Setters (escritura con validación) ----------
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
            # Aquí se evita un bug futuro al asegurar la integridad del dato.
            raise ValueError(f"El monto no puede ser negativo: {valor}.")
        self._monto = valor

    @property
    def tipo(self):
        """Getter de solo lectura: el tipo lo define la clase, no se cambia."""
        return self.TIPO

    # ----- Lógica común a todos los tipos de transacción -------------------
    def es_tipo(self, tipo_filtro):
        """Indica si la transacción es del tipo consultado.

        Args:
            tipo_filtro (str): "CREDITO" o "DEBITO" (no distingue mayúsculas).

        Returns:
            bool: True si coincide con el tipo de la transacción.
        """
        return self.tipo == tipo_filtro.strip().upper()

    def obtener_informacion(self):
        """Devuelve una descripción legible de la transacción.

        Returns:
            str: Texto con ID, tipo y monto formateado como moneda.
        """
        return (
            f"Transacción {self.transaccion_id} | "
            f"Tipo: {self.tipo} | Monto: ${self.monto:,.2f}"
        )

    # ----- Método común (placeholder) para el polimorfismo -----------------
    @abstractmethod
    def calcular_impacto(self):
        """Calcula el costo adicional de la transacción.

        Cada clase hija DEBE sobrescribir este método con su propia regla.

        Returns:
            float: Valor del impacto en pesos.
        """


# ---------------------------------------------------------------------------
# 2 y 3. Clases hijas (Herencia) con comportamiento único (Polimorfismo)
# ---------------------------------------------------------------------------
class TransaccionCredito(TransaccionBase):
    """Transacción de crédito: su impacto es el interés sobre el monto."""

    TIPO = "CREDITO"

    def calcular_impacto(self):
        """Sobrescribe el método base: devuelve el interés generado.

        Returns:
            float: monto * TASA_INTERES_CREDITO.
        """
        return self.monto * TASA_INTERES_CREDITO


class TransaccionDebito(TransaccionBase):
    """Transacción de débito: su impacto es una comisión fija."""

    TIPO = "DEBITO"

    def calcular_impacto(self):
        """Sobrescribe el método base: devuelve la comisión fija.

        Returns:
            float: COMISION_FIJA_DEBITO (no depende del monto).
        """
        return COMISION_FIJA_DEBITO


# Registro de tipos: relaciona el texto del archivo con la clase que lo maneja.
# Para extender el sistema (OCP) se crea una clase nueva y se agrega aquí.
TIPOS_TRANSACCION = {
    "CREDITO": TransaccionCredito,
    "DEBITO": TransaccionDebito,
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
    clase = TIPOS_TRANSACCION.get(tipo.strip().upper())
    if clase is None:
        raise ValueError(
            f"Tipo de transacción inválido: '{tipo}'. "
            f"Use {tuple(TIPOS_TRANSACCION)}."
        )
    return clase(transaccion_id, monto)


# ---------------------------------------------------------------------------
# Clase auxiliar de gestión (SRP: solo procesa listas de transacciones)
# ---------------------------------------------------------------------------
class GestorTransacciones:
    """Agrupa las operaciones sobre un conjunto de transacciones.

    Atributos:
        transacciones (list[TransaccionBase]): Lista principal de objetos.
    """

    def __init__(self, transacciones):
        """Recibe la lista principal de objetos."""
        self.transacciones = transacciones

    def calcular_monto_total(self):
        """Suma el monto de todas las transacciones.

        Returns:
            float: Monto total acumulado.
        """
        total = 0
        for transaccion in self.transacciones:
            total += transaccion.monto
        return total

    def filtrar_por_tipo(self, tipo_filtro):
        """Devuelve las transacciones que coinciden con el tipo indicado.

        Args:
            tipo_filtro (str): "CREDITO" o "DEBITO".

        Returns:
            list[TransaccionBase]: Objetos que cumplen el filtro.
        """
        lista_filtrada = []
        for transaccion in self.transacciones:
            if transaccion.es_tipo(tipo_filtro):
                lista_filtrada.append(transaccion)
        return lista_filtrada

    def calcular_impacto_total(self):
        """Suma el impacto de todas las transacciones (polimorfismo).

        Observa que NO se pregunta de qué tipo es cada transacción: se llama
        siempre a ``calcular_impacto()`` y cada objeto responde a su manera.

        Returns:
            float: Impacto total (intereses + comisiones).
        """
        total = 0
        for transaccion in self.transacciones:
            total += transaccion.calcular_impacto()
        return total


# ---------------------------------------------------------------------------
# Lectura de archivo: almacena OBJETOS de las clases hijas
# ---------------------------------------------------------------------------
def leer_y_almacenar_datos(nombre_archivo):
    """Lee el archivo de transacciones y devuelve objetos y rechazos.

    Formato esperado por línea: ``ID,TIPO,MONTO`` (ej. ``C001,DEBITO,2500000``).
    Las líneas vacías se ignoran. Si una línea trae datos inválidos (por ejemplo,
    un monto negativo), los setters de la clase la rechazan: la línea se registra
    como rechazada y la carga del resto del archivo continúa.

    Args:
        nombre_archivo (str): Ruta del archivo de texto.

    Returns:
        tuple[list[TransaccionBase], list[tuple]]: Lista principal de objetos y
        lista de rechazos con el formato ``(numero_linea, texto_linea, motivo)``.
    """
    lista_transacciones = []
    lineas_rechazadas = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            if not linea.strip():
                continue  # saltar líneas en blanco
            partes = linea.strip().split(",")  # separar campos por comas
            try:
                # Si el dato es inválido, el setter lanza ValueError y no se crea el objeto
                transaccion = crear_transaccion(partes[0], partes[1], partes[2])
                lista_transacciones.append(transaccion)
            except (ValueError, IndexError) as error:
                lineas_rechazadas.append((numero_linea, linea.strip(), str(error)))
    return lista_transacciones, lineas_rechazadas


# ---------------------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------------------
def ejecutar_sistema():
    """Integra lectura, procesamiento y presentación de resultados."""
    transacciones, rechazadas = leer_y_almacenar_datos("Transacciones.txt")
    gestor = GestorTransacciones(transacciones)

    print("--- INICIO PROCESAMIENTO POO (PILARES) ---")
    print(f"Total de objetos cargados: {len(transacciones)}")

    print("\n--- Encapsulamiento: líneas rechazadas por los setters ---")
    if rechazadas:
        for numero_linea, texto, motivo in rechazadas:
            print(f"Línea {numero_linea} ({texto}) rechazada -> {motivo}")
    else:
        print("Ninguna línea fue rechazada.")

    print("\n--- Herencia: cada objeto es de una clase hija ---")
    for transaccion in transacciones:
        print(
            f"{transaccion.obtener_informacion()} "
            f"[clase: {type(transaccion).__name__}]"
        )

    print("\n--- Polimorfismo: la misma llamada, resultado distinto (impacto) ---")
    for transaccion in transacciones:
        impacto = transaccion.calcular_impacto()
        print(f"{transaccion.transaccion_id} ({transaccion.tipo}): "
              f"impacto = ${impacto:,.2f}")

    print(f"\nMonto total de las transacciones: ${gestor.calcular_monto_total():,.2f}")
    print(f"Impacto total (intereses + comisiones): "
          f"${gestor.calcular_impacto_total():,.2f}")

    debitos = gestor.filtrar_por_tipo("DEBITO")
    print(f"\nTransacciones de DEBITO encontradas: {len(debitos)}")
    for transaccion in debitos:
        print(f"> {transaccion.obtener_informacion()}")

    creditos = gestor.filtrar_por_tipo("CREDITO")
    print(f"\nTransacciones de CREDITO encontradas: {len(creditos)}")
    for transaccion in creditos:
        print(f"> {transaccion.obtener_informacion()}")

    print("\n--- FIN PROCESAMIENTO ---")


# Inicia el programa solo si se ejecuta este archivo directamente
if __name__ == "__main__":
    ejecutar_sistema()
