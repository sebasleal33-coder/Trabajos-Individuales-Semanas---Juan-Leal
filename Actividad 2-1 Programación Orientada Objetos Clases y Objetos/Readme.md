# Actividad 2-1: Programación Orientada a Objetos – Clases y Objetos

**Núcleo:** Fundamentos de Software · **Docente:** Simón Peláez Loaiza
**Estudiante:** Juan Sebastián Leal Suárez · Fundación Universitaria CEIPA

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `procesador_transacciones.py` | Versión de la Semana 1 (Programación Estructurada). |
| `transaccion_poo_v1.py` | Refactorización a POO: clase `Transaccion` y clase auxiliar `GestorTransacciones`. |
| `Transacciones.txt` | Datos de entrada (formato `ID,TIPO,MONTO`). |

## Ejecución

```bash
python transaccion_poo_v1.py
```

Los archivos deben estar en la misma carpeta (el programa abre `Transacciones.txt` por ruta relativa).

## Paso 1: Análisis de fragilidad de la Programación Estructurada

La pregunta es: ¿por qué la PE fallaría si hubiera que manejar **10 tipos de transacciones diferentes**, y por qué tener los datos (`transaccion_id`, `monto`) separados de la lógica (`calcular_monto_total`) crea un riesgo de *debugging*?

### 1. Los datos y la lógica no se pertenecen entre sí
Cada transacción es un diccionario sin estructura garantizada. Cualquier función puede leerlo o modificarlo, y ninguna lo "protege". Si una función espera la clave `"monto"` y otra parte del programa crea el diccionario con `"valor"`, el error (`KeyError`) aparece lejos de donde se originó.

### 2. Crecimiento por copia y condicionales
Con 10 tipos, cada comportamiento propio (comisiones, impuestos, validaciones) obligaría a añadir ramas `if/elif` dentro de las mismas funciones o a duplicar funciones (`calcular_total_credito`, `calcular_total_transferencia`, …). Cada nuevo tipo obliga a **tocar código que ya funcionaba**, con riesgo de romperlo.

### 3. Los tipos son simples cadenas de texto
En `filtrar_por_tipo`, el tipo es un `str` comparado con `==`. Un error de escritura como `"CREDTIO"` no produce ningún error: devuelve una lista vacía y el programa "funciona" con resultados incorrectos. Es el peor tipo de falla para depurar, porque es silenciosa.

### 4. Sin validación en el punto de creación
`leer_y_almacenar_datos` convierte el monto con `float()`, pero no valida que el tipo exista ni que el monto sea no negativo. Los datos inválidos entran a la lista y fallan después, en otra función.

### 5. Inconsistencias que el diseño no previene
En el código de la Semana 1 la clave del diccionario es `transaccion_id`, pero la salida imprime `"Cliente"`, y el enunciado habla de `cliente_id`. El diseño no obliga a usar un nombre único para el concepto; en un sistema con 10 tipos, esas diferencias se multiplican.

### Por qué esto crea riesgo de *debugging*
Cuando el dato está separado de la lógica, para entender un fallo hay que revisar **todas** las funciones que tocan el diccionario, porque cualquiera pudo haberlo alterado o interpretado distinto. La causa de un error y el lugar donde se manifiesta quedan lejos uno del otro. Al crecer el sistema, el número de lugares a revisar crece con él.

## Paso 2: El salto al objeto (refactorización)

| Paso del enunciado | Implementación en `transaccion_poo_v1.py` |
|---|---|
| 1. Definición de la clase | `class Transaccion` representa una entidad del sistema. |
| 2. Constructor | `__init__(transaccion_id, tipo, monto)` encapsula los tres datos como atributos y los valida. |
| 3. Métodos y comportamientos | `obtener_informacion()`, `es_tipo()`, `validar_tipo()`; los cálculos sobre la colección pasan a `GestorTransacciones` (`calcular_monto_total()`, `filtrar_por_tipo()`). |
| 4. Lectura de archivos | `leer_y_almacenar_datos()` crea y almacena **objetos `Transaccion`** en la lista principal en lugar de diccionarios. |

## Resultado

La ejecución produce los mismos resultados que la versión estructurada (8 registros, total **$11,246,000.00** y 4 transacciones de tipo `CREDITO`), pero ahora los datos viajan junto con su comportamiento y se validan al crearse.

## Uso de inteligencia artificial

Se utilizó Claude (Anthropic) como apoyo para revisar la estructura del código, redactar la documentación y el informe. Los detalles se declaran en el apartado correspondiente del informe en Word que se entregará en el CANVAS.