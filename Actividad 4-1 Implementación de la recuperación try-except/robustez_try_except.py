"""
robustez_try_except.py
Semana 4 - Actividad 1: Implementacion de la recuperacion try/except.

EL PROBLEMA QUE RESOLVEMOS
--------------------------
En la Semana 3 blindaste la clase: el setter lanza ValueError si el monto es
malo. Eso esta bien... pero si NADIE atrapa ese error, el programa entero se
detiene en el primer registro corrupto. Si lees 100 registros y el #50 esta
malo, pierdes los 50 que venian despues.

Esta semana le damos al sistema la capacidad de RECUPERARSE: cuando una linea
falla, la registramos (log) y CONTINUAMOS con la siguiente.

Vocabulario (el mismo de la plataforma, Semana 4):
    Excepcion  -> un error que interrumpe el flujo normal del programa.
    try        -> el bloque donde ponemos el codigo que PODRIA fallar.
    except     -> el bloque que ATRAPA el fallo y decide que hacer con el.
    ValueError -> el tipo de dato es correcto, pero el VALOR no sirve.
    TypeError  -> el tipo o la CANTIDAD de datos no es la esperada.
    Logging    -> dejar constancia del fallo para poder auditarlo despues.

El archivo transacciones_corruptas.txt trae 7 registros con 3 errores a
proposito. Al terminar deberias ver 4 transacciones validas procesadas y 3
avisos de error, sin que el programa se caiga ni una sola vez.

Cada linea del archivo tiene:  cliente_id, tipo, monto
Para ejecutar:  python robustez_try_except.py
"""


# 1) La clase con el monto ENCAPSULADO y VALIDADO (tal como quedo en la Semana 3).
#    Fijate que aqui NO hay ningun try/except: el objeto solo sabe protegerse a
#    si mismo lanzando el error. Decidir que hacer con ese error es trabajo de
#    quien lo llama (la funcion de carga, mas abajo).
class Transaccion:
    """Transaccion que se protege a si misma: rechaza montos invalidos."""

    def __init__(self, cliente_id, tipo, monto):
        self.cliente_id = cliente_id
        self.tipo = tipo
        self.monto = monto            # pasa por el SETTER, asi que se valida

    @property
    def monto(self):
        """GETTER: puente de lectura seguro al atributo privado."""
        return self._monto

    @monto.setter
    def monto(self, valor):
        """
        SETTER: aqui nacen DOS de los tres errores del archivo.

        - int(valor) lanza ValueError si 'valor' es texto no numerico, como
          "texto_invalido" (registro C003). Ese error lo lanza Python solo.
        - Si el numero es negativo, el ValueError lo lanzamos NOSOTROS
          (registro C004). Esa es la validacion que escribiste en la Semana 3.
        """
        if int(valor) < 0:
            raise ValueError("el monto no puede ser negativo")
        self._monto = int(valor)

    def __str__(self):
        return f"{self.cliente_id} | {self.tipo} | ${self.monto}"


# 2) Lectura TOLERANTE A FALLOS.
#    Este es el "punto critico" del Paso 1 de la actividad: el unico lugar donde
#    debe vivir el try/except es donde se construye el objeto, porque es ahi
#    donde los datos crudos del archivo se convierten en un objeto y pueden
#    fallar. El try va DENTRO del bucle: asi cada linea se protege por separado
#    y una mala no arrastra a las demas.
def cargar_transacciones(nombre_archivo):
    """Lee el archivo; si una linea falla, la registra (log) y CONTINUA con la siguiente."""
    transacciones = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            linea = linea.strip()
            if not linea:
                continue  # ignora lineas en blanco

            try:
                partes = linea.split(",")
                # Aqui pueden ocurrir los dos tipos de fallo:
                #   - Si faltan columnas (C006 solo trae 2), al constructor le
                #     faltan argumentos -> TypeError.
                #   - Si el monto es texto o negativo -> ValueError (del setter).
                transacciones.append(Transaccion(*partes))

            # Paso 3 de la actividad: ESTRATEGIA DE RECUPERACION.
            # En ambos except hacemos lo mismo: (a) dejamos constancia del fallo
            # indicando el tipo de error y la linea exacta, y (b) no hacemos nada
            # mas, para que el bucle 'for' siga con el siguiente registro.
            except ValueError as error:
                print(f"  [Linea {numero}] ValueError: {error}  ->  se ignora: {linea}")
            except TypeError:
                print(f"  [Linea {numero}] TypeError: datos insuficientes  ->  se ignora: {linea}")

    return transacciones


# 3) Programa principal
def ejecutar_sistema():
    transacciones = cargar_transacciones("transacciones_corruptas.txt")

    print()
    print(f"Se procesaron {len(transacciones)} transacciones validas:")
    for t in transacciones:
        print("  ", t)

    # El resultado es un sistema TOLERANTE A FALLOS: leyo un archivo lleno de
    # datos corruptos y aun asi proceso todos los datos validos, dejando un
    # registro de los errores, sin detenerse ni una vez.


# Nota para la Actividad 3 (foro): en un sistema real este print() se
# reemplazaria por el modulo `logging`, que guarda los fallos en un archivo de
# auditoria en vez de solo mostrarlos en consola. Imprimir en pantalla sirve
# para un ejercicio de clase; en un sistema financiero, cuando se cierra la
# terminal, esa evidencia desaparece.
if __name__ == "__main__":
    ejecutar_sistema()