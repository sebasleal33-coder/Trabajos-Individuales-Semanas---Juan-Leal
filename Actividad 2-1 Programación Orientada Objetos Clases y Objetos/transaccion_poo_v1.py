# transaccion_poo_v1.py
"""
Actividad 2-1 - Programación Orientada a Objetos: clases y objetos.
Núcleo: Fundamentos de Software.

Objetivo:
    Refactorizar las funciones de Programación Estructurada (PE) de la Semana 1
    (procesador_transacciones.py) hacia una Clase ``Transaccion`` que encapsule
    los datos (ID, tipo y monto) junto con el comportamiento asociado a ellos,
    dentro del contexto Quantum Core.

Estructura del módulo:
    1. Clase Transaccion ........ entidad del sistema (atributos + métodos).
    2. Clase GestorTransacciones  lógica de procesamiento sobre una colección.
    3. leer_y_almacenar_datos ... lectura del archivo; devuelve objetos.
    4. ejecutar_sistema ......... función principal que integra todo.
"""

# Tipos de transacción permitidos. Se define una sola vez para que la validación
# no dependa de textos repetidos por todo el código.
TIPOS_VALIDOS = ("CREDITO", "DEBITO")


# ---------------------------------------------------------------------------
# 1. Definición de la Clase Transaccion
# ---------------------------------------------------------------------------
class Transaccion:
    """Representa una transacción individual del sistema Quantum Core.

    Encapsula en un único objeto los datos que en la versión estructurada
    estaban dispersos en un diccionario (ID, tipo y monto), junto con las
    operaciones que dependen de ellos.

    Atributos:
        transaccion_id (str): Identificador único de la transacción (ej. "C001").
        tipo (str): Tipo de transacción: "CREDITO" o "DEBITO".
        monto (float): Valor de la transacción, mayor o igual a cero.
    """

    def __init__(self, transaccion_id, tipo, monto):
        """Constructor: crea una transacción y valida sus datos.

        Args:
            transaccion_id (str): Identificador de la transacción.
            tipo (str): "CREDITO" o "DEBITO" (no distingue mayúsculas).
            monto (float | str): Valor de la transacción; se convierte a float.

        Raises:
            ValueError: Si el tipo no es válido o el monto es negativo o no numérico.
        """
        self.transaccion_id = transaccion_id.strip()
        self.tipo = self.validar_tipo(tipo)
        self.monto = self._validar_monto(monto)

    # ----- Métodos de validación (antes eran lógica suelta en la PE) -------
    @staticmethod
    def validar_tipo(tipo):
        """Valida y normaliza el tipo de transacción.

        Args:
            tipo (str): Texto con el tipo a validar.

        Returns:
            str: Tipo en mayúsculas, garantizado como válido.

        Raises:
            ValueError: Si el tipo no pertenece a TIPOS_VALIDOS.
        """
        tipo_normalizado = tipo.strip().upper()
        if tipo_normalizado not in TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo de transacción inválido: '{tipo}'. Use {TIPOS_VALIDOS}."
            )
        return tipo_normalizado

    @staticmethod
    def _validar_monto(monto):
        """Convierte el monto a float y verifica que no sea negativo.

        Raises:
            ValueError: Si el monto no es numérico o es menor que cero.
        """
        try:
            valor = float(monto)
        except (TypeError, ValueError):
            raise ValueError(f"Monto no numérico: '{monto}'.")
        if valor < 0:
            raise ValueError(f"El monto no puede ser negativo: {valor}.")
        return valor

    # ----- Comportamientos del objeto --------------------------------------
    def es_tipo(self, tipo_filtro):
        """Indica si la transacción es del tipo consultado.

        Args:
            tipo_filtro (str): "CREDITO" o "DEBITO".

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


# ---------------------------------------------------------------------------
# 2. Clase auxiliar de gestión (lógica de procesamiento de la PE)
# ---------------------------------------------------------------------------
class GestorTransacciones:
    """Clase auxiliar que agrupa las operaciones sobre un conjunto de objetos.

    Reemplaza las funciones sueltas ``calcular_monto_total`` y
    ``filtrar_por_tipo`` de la versión estructurada; ahora la lista y la lógica
    que la procesa viven juntas.

    Atributos:
        transacciones (list[Transaccion]): Lista principal de objetos.
    """

    def __init__(self, transacciones):
        """Recibe la lista principal de objetos Transaccion."""
        self.transacciones = transacciones

    def calcular_monto_total(self):
        """Suma el monto de todas las transacciones.

        Returns:
            float: Monto total acumulado.
        """
        total = 0
        for transaccion in self.transacciones:
            total += transaccion.monto  # acceso por atributo, no por clave de diccionario
        return total

    def filtrar_por_tipo(self, tipo_filtro):
        """Devuelve las transacciones que coinciden con el tipo indicado.

        Args:
            tipo_filtro (str): "CREDITO" o "DEBITO".

        Returns:
            list[Transaccion]: Objetos que cumplen el filtro.
        """
        lista_filtrada = []
        for transaccion in self.transacciones:
            if transaccion.es_tipo(tipo_filtro):
                lista_filtrada.append(transaccion)
        return lista_filtrada


# ---------------------------------------------------------------------------
# 3. Lectura de archivos modificada: ahora almacena OBJETOS, no diccionarios
# ---------------------------------------------------------------------------
def leer_y_almacenar_datos(nombre_archivo):
    """Lee el archivo de transacciones y devuelve una lista de objetos.

    Formato esperado por línea: ``ID,TIPO,MONTO`` (ej. ``C001,DEBITO,2500000``).
    Las líneas vacías se ignoran y las líneas con datos inválidos se reportan
    sin detener la carga del resto del archivo.

    Args:
        nombre_archivo (str): Ruta del archivo de texto.

    Returns:
        list[Transaccion]: Lista principal de objetos Transaccion.
    """
    lista_transacciones = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            if not linea.strip():
                continue  # saltar líneas en blanco
            partes = linea.strip().split(",")  # separar campos delimitados por comas
            try:
                # El constructor encapsula y valida los datos de una transacción
                transaccion = Transaccion(partes[0], partes[1], partes[2])
                lista_transacciones.append(transaccion)
            except (ValueError, IndexError) as error:
                print(f"[Aviso] Línea {numero_linea} omitida: {error}")
    return lista_transacciones


# ---------------------------------------------------------------------------
# 4. Función principal
# ---------------------------------------------------------------------------
def ejecutar_sistema():
    """Integra lectura, procesamiento y presentación de resultados."""
    transacciones = leer_y_almacenar_datos("Transacciones.txt")  # misma carpeta
    gestor = GestorTransacciones(transacciones)

    total = gestor.calcular_monto_total()
    creditos = gestor.filtrar_por_tipo("CREDITO")

    print("--- INICIO PROCESAMIENTO POO v1 ---")
    print(f"Total de objetos Transaccion cargados: {len(transacciones)}")

    print("\n--- Información de cada objeto (obtener_informacion) ---")
    for transaccion in transacciones:
        print(transaccion.obtener_informacion())

    print(f"\nMonto Total de todas las transacciones: ${total:,.2f}")

    print("\n--- Resultado del Filtrado ---")
    print(f"Transacciones de CREDITO encontradas: {len(creditos)}")
    for transaccion in creditos:
        print(f"> {transaccion.obtener_informacion()}")

    print("\n--- FIN PROCESAMIENTO ---")


# Inicia el programa solo si se ejecuta este archivo directamente
if __name__ == "__main__":
    ejecutar_sistema()