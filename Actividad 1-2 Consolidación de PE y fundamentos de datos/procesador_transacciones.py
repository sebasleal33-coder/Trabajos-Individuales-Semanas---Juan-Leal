# procesador_transacciones.py

# Actividad 1.2 - Consolidación de PE y fundamentos de datos

# Objetivo: Aplicar los principios de la PE como el uso de funciones y estructuras de
# control para leer y procesar datos, preparando la lógica para el Modelado de Sistemas.

#Descrición de la Actividad: Simular la lectura y procesamiento de una lista básica de transacciones
#para evaluar la lógica de PE dentro del contexto Quantum Core

#1. Función de lectura y almacenamiento de datos.
#Lee el archivo de transacciones y devuelve una lista de diccionarios.

def leer_y_almacenar_datos(nombre_archivo):
    lista_transacciones = []
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")  # separar los campos delimitados por comas
            transaccion = {
                "transaccion_id": partes[0],
                "tipo": partes[1],
                "monto": float(partes[2]),  # convertir el monto a número decimal
            }
            lista_transacciones.append(transaccion)
    return lista_transacciones

#2. Funciones Modulares de Procesamiento
# Calcula el monto total de todas las transacciones.

def calcular_monto_total(lista_transacciones):
    total = 0
    for transaccion in lista_transacciones:
        total += transaccion["monto"]
    return total

# Filtra las transacciones por tipo (CREDITO o DEBITO) y devuelve una lista filtrada.
def filtrar_por_tipo(lista_transacciones, tipo_filtro):
    lista_filtrada = []
    for transaccion in lista_transacciones:
        if transaccion["tipo"] == tipo_filtro:
            lista_filtrada.append(transaccion)
    return lista_filtrada

# Corresponde a la función principal que integra todas las funciones anteriores para ejecutar el sistema de procesamiento de transacciones.
def ejecutar_sistema():
    transacciones = leer_y_almacenar_datos("Transacciones.txt") #Tener presente que se ejecuta debido a que están en la misma carpeta
       
    total = calcular_monto_total(transacciones)
    tipo_especifico = filtrar_por_tipo(transacciones, "CREDITO")

    print("--- INICIO PROCESAMIENTO PE LIMPIO ---")
    print(f"Total de registros cargados: {len(transacciones)}")
    print(f"\nMonto Total de todas las transacciones: ${total:,.2f}")
    print("\n--- Resultado del Filtrado ---")
    print(f"Transacciones de CREDITO encontradas: {len(tipo_especifico)}")
    for transaccion in tipo_especifico:
        print(
            f"> Cliente {transaccion['transaccion_id']} / "
            f"Monto: ${transaccion['monto']:,.2f}"
        )
    print("\n--- FIN PROCESAMIENTO ---")

# Inicia el programa
ejecutar_sistema()

#Anotaciones Personales:

#La f antes de las comillas indica que es una f-string, lo que permite incluir expresiones dentro de las llaves {} y 
#formatearlas de manera más legible.

#El .2f dentro de las llaves indica que el número debe formatearse como un número decimal con dos dígitos después del punto decimal,
#lo que es útil para mostrar valores monetarios de manera consistente.

#El \n es un carácter de escape que representa un salto de línea, lo que permite organizar la salida en varias
# líneas para mejorar la legibilidad.

#len() es una función incorporada en Python que devuelve la longitud (el número de elementos) de un objeto, como una lista o una cadena.