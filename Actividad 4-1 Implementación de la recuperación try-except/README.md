# Actividad 4-1 Implementación de la recuperación try-except

**Núcleo:** Fundamentos de Software · **Programa:** Ingeniería de Sistemas, Fundación Universitaria CEIPA
**Estudiante:** Juan Sebastián Leal Suárez · **Docente:** Simón Peláez Loaiza · **Fecha:** 15/11/2026

## 1. Descripción

En la Semana 3 la clase `Transaccion` quedó blindada con encapsulamiento: su *setter* lanza un `ValueError` cuando el monto es inválido. Sin embargo, si la función que lee el archivo crea 100 objetos y el registro #50 está dañado, ese error **detiene todo el programa** y se pierden los registros siguientes.

Esta actividad refactoriza la función de lectura para que el sistema sea **tolerante a fallos**: cuando un registro falla, el programa **lo registra (log) y continúa** con el siguiente. El resultado es un sistema que lee un archivo lleno de datos corruptos y aun así procesa todos los datos válidos, sin detenerse.

## 2. Objetivo

Asegurar la robustez del sistema implementando la gestión de errores y excepciones `try-except` en la función de carga de datos, de modo que el programa pueda detectar, aislar y recuperarse de errores de datos (montos negativos, formatos incorrectos, datos incompletos) sin colapsar la ejecución.

## 3. Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `robustez_try_except.py` | Programa principal: clase `Transaccion` (con monto encapsulado y validado) y la función `cargar_transacciones()` con la lógica `try-except`. |
| `transacciones_corruptas.txt` | Archivo de prueba con 7 registros y 3 errores intencionales. |
| `Readme.md` | Este documento. |

## 4. Requisitos

- Python 3.8 o superior.
- No requiere instalar librerías externas (solo usa la biblioteca estándar).

## 5. Cómo ejecutar

1. Clonar o descargar el repositorio.
2. Abrir una terminal **dentro de la carpeta** del proyecto (el programa busca `transacciones_corruptas.txt` en la carpeta desde la que se ejecuta).
3. Ejecutar:

```bash
python robustez_try_except.py
```

> En algunos equipos el comando es `python3` o `py`.

## 6. Datos de prueba

Cada línea del archivo tiene el formato `cliente_id,tipo,monto`.

| Línea | Registro | Estado | Excepción esperada |
|---|---|---|---|
| 1 | `C001,DEBITO,150000` | Válido | — |
| 2 | `C002,CREDITO,500000` | Válido | — |
| 3 | `C003,DEBITO,texto_invalido` | **Error 1** | `ValueError` (falla de conversión) |
| 4 | `C004,CREDITO,-200000` | **Error 2** | `ValueError` (validación del *setter*: monto negativo) |
| 5 | `C005,DEBITO,45000` | Válido | — |
| 6 | `C006,DEBITO` | **Error 3** | `TypeError` (datos insuficientes) |
| 7 | `C007,CREDITO,10000` | Válido | — |

## 7. Salida esperada

```text
  [Linea 3] ValueError: invalid literal for int() with base 10: 'texto_invalido'  ->  se ignora: C003,DEBITO,texto_invalido
  [Linea 4] ValueError: el monto no puede ser negativo  ->  se ignora: C004,CREDITO,-200000
  [Linea 6] TypeError: datos insuficientes  ->  se ignora: C006,DEBITO

Se procesaron 4 transacciones validas:
   C001 | DEBITO | $150000
   C002 | CREDITO | $500000
   C005 | DEBITO | $45000
   C007 | CREDITO | $10000
```

**Resultado:** 4 transacciones válidas procesadas, 3 errores registrados y 0 caídas del programa.

## 8. Cómo funciona

1. **Diagnóstico del punto crítico.** El único lugar donde puede fallar la carga es donde cada línea de texto se convierte en un objeto `Transaccion`, dentro de `cargar_transacciones()`. Allí (y solo allí) vive el `try-except`; la clase no atrapa sus propios errores, solo los lanza.
2. **Bloque `try-except` dentro del bucle.** El `try` envuelve la separación de campos (`split`) y la creación del objeto. Al estar *dentro* del `for`, cada línea se protege por separado y una línea mala no afecta a las demás.
   - `except ValueError`: atrapa fallos de conversión (`"texto_invalido"` no es un número) y de validación (monto negativo lanzado por el *setter*).
   - `except TypeError`: atrapa registros con datos insuficientes (una línea con dos columnas cuando se esperan tres).
3. **Estrategia de recuperación pasiva (logging).** Cada `except` imprime un mensaje con el tipo de error y la línea que lo causó, y no hace nada más: el bucle `for` continúa con el siguiente registro.

## 9. Cobertura de errores

| Situación | Excepción | ¿Cubierta? |
|---|---|---|
| Monto con texto (`texto_invalido`), vacío o decimal | `ValueError` | Sí |
| Monto negativo | `ValueError` | Sí |
| Línea con menos o más columnas de las esperadas | `TypeError` | Sí |
| Líneas en blanco | — | Se ignoran sin error |
| Archivo inexistente | `FileNotFoundError` | No (es un fallo del entorno, no de un dato; sin archivo no hay nada que procesar) |

## 10. Mejoras futuras

- Reemplazar `print()` por el módulo `logging` para guardar los fallos en un archivo de auditoría.
- Validar también el campo `tipo` (solo `DEBITO` o `CREDITO`) reutilizando la jerarquía de clases de la Semana 3.

## 11. Uso de inteligencia artificial

Se utilizó Claude (Anthropic, 2026) como apoyo para estructurar la documentación (informe y este Readme). El código base fue entregado por el docente; el estudiante ejecutó el programa y verificó los resultados.

## 12. Referencias

- Anthropic. (2026). *Claude* (versión Sonnet 5.5) [Modelo de lenguaje de gran tamaño]. https://claude.ai
- Cuevas, A. (2016). *Python 3. Curso práctico*. Rama Editorial. https://www.digitaliapublishing.com/a/110075
- Python Software Foundation. (s. f.). *Errors and exceptions*. Python 3 documentation. https://docs.python.org/3/tutorial/errors.html