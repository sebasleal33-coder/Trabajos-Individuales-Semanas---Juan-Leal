# Actividad 4-2 Serialización y Persistencia JSON

**Núcleo:** Fundamentos de Software  
**Institución:** Fundación Universitaria CEIPA  
**Estudiante:** Juan Sebastián Leal Suárez  
**Docente:** Simón Peláez Loaiza  
**Fecha:** 15 de noviembre de 2026

## Descripción

Esta actividad (Semana 4, Actividad 2) muestra cómo convertir objetos de Python en texto **JSON** (serialización) y cómo reconstruirlos a partir de ese texto (deserialización). Se reutilizan las clases robustas de la Semana 3 (`TransaccionCredito` y `TransaccionDebito`) y se aplica el manejo de errores con `try-except` de la Actividad 4-1.

El proceso siempre sigue dos escalas:

```
Serializar:     Objeto Python  ->  Diccionario  ->  Texto JSON
Deserializar:   Texto JSON     ->  Diccionario  ->  Objeto Python (llamando al constructor)
```

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `serializacion_json.py` | Programa principal con la serialización, deserialización, manejo de errores y persistencia en archivo. |
| `diseno_pilares_poo.py` | Clases de la Semana 3 (encapsulamiento, herencia y polimorfismo), reutilizadas sin cambios. |
| `Transacciones.txt` | Datos de entrada de la Semana 3 (incluye registros inválidos a propósito). |
| `transacciones.json` | Archivo generado por el programa con las transacciones guardadas en JSON. |
| `Informe_Actividad_4-2.docx` | Informe técnico en formato APA. |

## Requisitos

- Python 3.8 o superior.
- No requiere instalar librerías externas: usa solo `json` y `pathlib`, que vienen incluidas con Python.

## Cómo ejecutar

1. Verificar que `serializacion_json.py`, `diseno_pilares_poo.py` y `Transacciones.txt` estén en la misma carpeta.
2. Abrir una terminal en esa carpeta y ejecutar:

```bash
python serializacion_json.py
```

## Qué demuestra el programa

1. **Parte 1 – El viaje completo:** una transacción se convierte en diccionario, luego en texto JSON y regresa a ser un objeto, mostrando el tipo de dato en cada escala.
2. **Parte 2 – Casos de error:** ocho textos JSON (uno válido y siete dañados) se procesan sin que el programa se detenga. Cada error se rechaza con un mensaje claro.
3. **Parte 3 – Persistencia:** las transacciones válidas se guardan en `transacciones.json`, se leen de nuevo y se verifica que los datos sean idénticos. También se prueba un archivo con registros dañados, un archivo truncado y un archivo inexistente.

## Errores contemplados

- JSON mal formado (sintaxis incorrecta o texto cortado).
- Clave obligatoria ausente (`transaccion_id`, `tipo` o `monto`).
- Tipo de transacción no registrado (por ejemplo, `EFECTIVO`).
- Monto negativo o no numérico.
- Dato con tipo incorrecto.
- Contenido que no es un diccionario o una lista.
- Archivo inexistente.

## Decisiones de diseño

- **SRP:** las clases de la Semana 3 no se modificaron; las funciones de conversión a JSON viven aparte.
- **Reutilización de validaciones:** al reconstruir un objeto se llama a `crear_transaccion`, por lo que los setters siguen validando los datos.
- **Aislamiento de errores:** si un registro del archivo está dañado, se anota como rechazado y se continúa con el siguiente.

## Uso de inteligencia artificial

Se utilizó Claude (Anthropic) como apoyo para estructurar el código y la documentación. El código fue ejecutado, revisado y comprendido por el estudiante.