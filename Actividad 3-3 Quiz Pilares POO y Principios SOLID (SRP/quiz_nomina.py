# quiz_nomina.py
# Quiz Semana 3 - Fundamentos de programacion (Pilares de POO)
# Autor: Juan Sebastian Leal
# Curso: Fundamentos de Software - Fundacion Universitaria CEIPA
# Docente: Simon Pelaez Loaiza
#
# Tema: nomina de una empresa leida desde un EXCEL. Aplica los 3 pilares:
# Encapsulamiento, Herencia y Polimorfismo.
#
# Antes de ejecutar, instala las librerias (una sola vez):
#     pip install -r requirements.txt
# Para ejecutar:  python quiz_nomina.py

import pandas as pd


# 1) CLASE BASE (PADRE): datos comunes + ENCAPSULAMIENTO del salario
class EmpleadoBase:
    """Clase base: encapsula el salario y define el comportamiento comun."""

    def __init__(self, nombre, salario_base, ciudad):
        """Crea un empleado.

        Args:
            nombre: nombre del empleado.
            salario_base: salario mensual (se valida en el setter).
            ciudad: ciudad de trabajo.
        """
        self.nombre = nombre
        self.ciudad = ciudad
        # Se usa el SETTER (no _salario_base directo) para que la
        # validacion tambien se ejecute al crear el objeto.
        self.salario_base = salario_base

    # GETTER: leer el salario de forma segura
    @property
    def salario_base(self):
        """Devuelve el salario base (atributo privado _salario_base)."""
        return self._salario_base

    # SETTER: valida ANTES de guardar
    @salario_base.setter
    def salario_base(self, nuevo_salario):
        """Valida y guarda el salario.

        Raises:
            ValueError: si el salario es negativo.
            ValueError: si el valor no se puede convertir a entero
                (por ejemplo, el texto "no aplica").
        """
        valor = int(nuevo_salario)  # falla con ValueError si es texto
        if valor < 0:
            raise ValueError("El salario no puede ser negativo.")
        self._salario_base = valor  # el cero SI es valido

    # Metodo comun que CADA HIJA sobreescribe (POLIMORFISMO)
    def calcular_pago(self):
        """Calcula el pago mensual. Cada clase hija debe sobreescribirlo."""
        raise NotImplementedError("Cada tipo de empleado calcula su pago.")

    def obtener_informacion(self):
        """Devuelve un resumen, ej: 'Ana | EmpleadoPlanta | Medellin | base $3000000'."""
        return f"{self.nombre} | {type(self).__name__} | {self.ciudad} | base ${self.salario_base}"


# 2) CLASES HIJAS (HERENCIA)
class EmpleadoPlanta(EmpleadoBase):
    """Empleado de planta: recibe salario base + 30% de prestaciones."""

    def calcular_pago(self):
        # POLIMORFISMO: version propia de calcular_pago()
        return self.salario_base * 1.30


class EmpleadoContratista(EmpleadoBase):
    """Contratista: recibe unicamente su salario base."""

    def calcular_pago(self):
        # POLIMORFISMO: sin prestaciones
        return self.salario_base


# 3) Crear el objeto correcto segun el TIPO
def crear_empleado(nombre, tipo, salario_base, ciudad):
    """Fabrica de empleados: devuelve el objeto segun el tipo.

    Raises:
        ValueError: si el tipo no es PLANTA ni CONTRATISTA.
    """
    if tipo == "PLANTA":
        return EmpleadoPlanta(nombre, salario_base, ciudad)
    if tipo == "CONTRATISTA":
        return EmpleadoContratista(nombre, salario_base, ciudad)
    raise ValueError(f"tipo desconocido '{tipo}'")


# =====================================================================
# 4) LECTURA DEL EXCEL  --  PROVISTA POR EL DOCENTE (NO SE MODIFICA)
#    Es ROBUSTA: usa solo las columnas que necesita (aunque el Excel tenga
#    columnas de mas), ignora filas incompletas y salta las invalidas
#    (por ejemplo un salario negativo) sin detener el programa.
# =====================================================================
def leer_empleados_excel(nombre_archivo):
    """Lee empleados desde un Excel y devuelve una lista de objetos Empleado."""
    empleados = []
    df = pd.read_excel(nombre_archivo)

    # Normalizamos los nombres de columna (sin espacios y en minuscula)
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Verificamos que existan las columnas minimas que necesitamos
    columnas_necesarias = {"nombre", "tipo", "salario_base"}
    if not columnas_necesarias.issubset(df.columns):
        faltan = columnas_necesarias - set(df.columns)
        print(f"  [Error] Al Excel le faltan columnas: {faltan}")
        return empleados

    for _, fila in df.iterrows():
        # Saltar filas incompletas (sin nombre, tipo o salario)
        if pd.isna(fila["nombre"]) or pd.isna(fila["tipo"]) or pd.isna(fila["salario_base"]):
            print("  [Aviso] Fila incompleta ignorada.")
            continue

        nombre = str(fila["nombre"]).strip()
        tipo = str(fila["tipo"]).strip().upper()
        salario = fila["salario_base"]
        # 'ciudad' es una columna extra: si no viene, usamos texto vacio
        ciudad = str(fila["ciudad"]).strip() if "ciudad" in df.columns and not pd.isna(fila["ciudad"]) else ""

        try:
            empleado = crear_empleado(nombre, tipo, salario, ciudad)
            if empleado is not None:  # (por si aun no completas crear_empleado)
                empleados.append(empleado)
        except ValueError as error:
            print(f"  [Aviso] Se ignoro {nombre}: {error}")

    return empleados


# =====================================================================
# 5) RETO EXTRA: FUNCIONES PROPIAS
# =====================================================================
def salario_promedio(empleados):
    """Calcula el promedio del salario base de la nomina.

    Args:
        empleados: lista de objetos EmpleadoBase (o hijas).

    Returns:
        float: promedio de salario_base. Devuelve 0 si la lista esta vacia
        (evita una division por cero).
    """
    if not empleados:
        return 0
    total = sum(empleado.salario_base for empleado in empleados)
    return total / len(empleados)


def nomina_total(empleados):
    """Calcula cuanto paga la empresa en total al mes.

    Suma calcular_pago() de cada empleado. Gracias al POLIMORFISMO no hace
    falta preguntar el tipo: cada objeto sabe calcular su propio pago.

    Args:
        empleados: lista de objetos EmpleadoBase (o hijas).

    Returns:
        float: suma de los pagos mensuales (0 si la lista esta vacia).
    """
    return sum(empleado.calcular_pago() for empleado in empleados)


# 6) Funcion principal
def ejecutar_quiz():
    """Lee el Excel, imprime la nomina y muestra los resultados de las funciones propias."""
    empleados = leer_empleados_excel("empleados.xlsx")

    print("--- Nomina ---")
    for empleado in empleados:
        # POLIMORFISMO: la misma llamada, distinto resultado segun el tipo
        print(empleado.obtener_informacion(), "-> pago:", empleado.calcular_pago())

    # Funciones propias del reto extra
    print("\nTotal de empleados en nomina:", len(empleados))
    print(f"Salario promedio: ${salario_promedio(empleados):,.2f}")
    print(f"Nomina total mensual: ${nomina_total(empleados):,.2f}")


# Iniciar el programa
ejecutar_quiz()