# Actividad 3-1: Robustez con Encapsulamiento, Herencia y Polimorfismo (POO)

**Núcleo:** Fundamentos de Software · **Docente:** Simón Peláez Loaiza
**Estudiante:** Juan Sebastián Leal Suárez · Fundación Universitaria CEIPA

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `diseno_pilares_poo.py` | Programa principal: jerarquía de clases con encapsulamiento, herencia y polimorfismo. |
| `Transacciones.txt` | Datos de entrada (formato `ID,TIPO,MONTO`), incluye líneas inválidas a propósito para probar el blindaje de datos. |
| `Readme.md` | Esta documentación. |

## Ejecución

```bash
python diseno_pilares_poo.py
```

Los archivos deben estar en la misma carpeta (el programa abre `Transacciones.txt` por ruta relativa). Solo usa la biblioteca estándar de Python (`abc`), no hay que instalar nada.

## Punto de partida y objetivo

En la Semana 2 la clase `Transaccion` ya funcionaba bajo el paradigma POO, pero seguía siendo frágil: sus datos podían modificarse desde cualquier parte, un solo tipo de comportamiento servía para todo y agregar un tipo nuevo obligaba a tocar código que ya funcionaba. Esta actividad la vuelve **segura contra errores** y **fácil de extender**, aplicando los tres pilares de la POO y dos principios SOLID: **SRP** (Responsabilidad Única) y **OCP** (Abierto/Cerrado).

## Paso 1: Blindaje de datos (Encapsulamiento)

| Elemento | Implementación en `diseno_pilares_poo.py` |
|---|---|
| Atributos privados | `_transaccion_id` y `_monto` (guion bajo inicial, convención de Python para "uso interno"). |
| Getters (lectura) | `@property` en `transaccion_id`, `monto` y `tipo`: se leen como si fueran variables, pero son funciones. |
| Setters (escritura con validación) | `@monto.setter` convierte a `float`, rechaza valores no numéricos y **nunca permite un monto negativo** (`ValueError`). `@transaccion_id.setter` rechaza IDs vacíos. |
| Validación desde la creación | El constructor asigna con `self.monto = monto` (sin guion bajo), así los setters también se ejecutan al crear el objeto. |
| `tipo` de solo lectura | No tiene setter: el tipo lo define la clase y un objeto de crédito no puede "convertirse" en débito. |

## Paso 2: Jerarquía de clases (Herencia)

```
TransaccionBase (clase abstracta)
├── TransaccionCredito   TIPO = "CREDITO"
└── TransaccionDebito    TIPO = "DEBITO"
```

- **`TransaccionBase`** concentra todo lo común: constructor, getters/setters, `es_tipo()` y `obtener_informacion()`. Hereda de `ABC`, por lo que no se puede instanciar directamente.
- **`TransaccionCredito` y `TransaccionDebito`** heredan todo lo anterior y solo definen lo que las diferencia (`TIPO` y `calcular_impacto()`).

## Paso 3: Comportamiento único (Polimorfismo)

`calcular_impacto()` se declara como método abstracto en la clase base (el *placeholder* que pide el enunciado) y cada clase hija lo **sobrescribe**:

| Clase | Regla de `calcular_impacto()` | Ejemplo |
|---|---|---|
| `TransaccionCredito` | `monto * TASA_INTERES_CREDITO` (1.8 % mensual) | Crédito de $700,000 → $12,600.00 |
| `TransaccionDebito` | `COMISION_FIJA_DEBITO` ($6,500, no depende del monto) | Débito de $2,500,000 → $6,500.00 |

`GestorTransacciones.calcular_impacto_total()` recorre la lista y llama siempre a `transaccion.calcular_impacto()` **sin preguntar de qué tipo es cada objeto**: la misma llamada produce un resultado distinto según el objeto.

> La tasa (`0.018`) y la comisión (`6500`) son valores de ejemplo y están al inicio del archivo para cambiarlos en un solo lugar.

## Principios SOLID aplicados

- **SRP (Responsabilidad Única):** cada clase tiene un solo trabajo: `TransaccionBase` protege los datos comunes, `TransaccionCredito` y `TransaccionDebito` conocen su propia regla de impacto y `GestorTransacciones` procesa listas (suma, filtra, calcula impacto total).
- **OCP (Abierto/Cerrado):** el código está abierto a extensión y cerrado a modificación. Un tipo nuevo se agrega creando una clase hija y registrándola en `TIPOS_TRANSACCION`; `TransaccionBase` y `GestorTransacciones` no se tocan. La función `crear_transaccion()` (fábrica) elige la clase correcta según el texto del archivo.

Ejemplo de extensión:

```python
class TransaccionTransferencia(TransaccionBase):
    TIPO = "TRANSFERENCIA"

    def calcular_impacto(self):
        return 3500  # comisión fija de ejemplo

TIPOS_TRANSACCION["TRANSFERENCIA"] = TransaccionTransferencia
```

## Pruebas de robustez con el archivo de datos

La prueba del encapsulamiento sale del propio `Transacciones.txt`, no de datos escritos dentro del código. Al final del archivo hay tres líneas inválidas:

| Línea | Contenido | Resultado |
|---|---|---|
| 9 | `C009,EFECTIVO,1500000` | Rechazada: tipo de transacción inválido (solo `CREDITO` o `DEBITO`). |
| 10 | `C010,DEBITO,-2000000` | Rechazada por el setter: el monto no puede ser negativo. |
| 11 | `C011,CREDITO,-5000000` | Rechazada por el setter: el monto no puede ser negativo. |

`leer_y_almacenar_datos()` no se detiene ante un dato inválido: registra la línea (número, texto y motivo) y sigue cargando el resto. El programa imprime las líneas rechazadas en la sección *Encapsulamiento*.

## Resultado de la ejecución

Con el archivo de 11 líneas, la salida es:

- **8 objetos cargados** y **3 líneas rechazadas** (C009, C010 y C011).
- Cada objeto se muestra con su clase hija (`TransaccionDebito` o `TransaccionCredito`).
- **Monto total:** $11,246,000.00
- **Impacto total (intereses + comisiones):** $99,620.00, que corresponde a $73,620.00 de intereses de 4 créditos y $26,000.00 de comisiones de 4 débitos.
- **Filtros:** 4 transacciones de `DEBITO` (C001, C003, C005, C006) y 4 de `CREDITO` (C002, C004, C007, C008).

## Documentación técnica

Todo el código incluye comentarios y *docstrings* (descripción, `Args`, `Returns` y `Raises`) en módulo, clases, métodos y funciones, como exige el formato de entrega.

## Uso de inteligencia artificial

Se utilizó Claude (Anthropic, 2026) como apoyo para proponer y revisar la estructura del código, redactar la documentación y preparar el informe. El estudiante aportó los datos, ajustó el código (atributos privados, filtro de débitos y líneas de prueba), lo ejecutó en Visual Studio Code y verificó los resultados. El detalle completo se declara en el apartado correspondiente del informe en Word entregado en CANVAS.

## Referencia

Anthropic. (2026). *Claude* (Claude Sonnet 5.5) [Modelo de lenguaje de gran tamaño]. https://claude.ai