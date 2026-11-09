# Quiz Semana 3 — Pilares de POO (nómina desde Excel)

**Estudiante:** Juan Sebastián Leal
**Institución:** Fundación Universitaria CEIPA
**Núcleo:** Fundamentos de Software
**Docente:** Simón Peláez Loaiza

## Descripción

Programa en Python que lee la nómina de una empresa desde `empleados.xlsx` (24 filas, 12 columnas) y aplica los tres pilares de la Programación Orientada a Objetos:

| Pilar | Dónde se aplica |
|-------|-----------------|
| **Encapsulamiento** | `EmpleadoBase` guarda el salario en el atributo privado `_salario_base` y lo expone con un *getter* (`@property`) y un *setter* que rechaza valores negativos. |
| **Herencia** | `EmpleadoPlanta` y `EmpleadoContratista` heredan de `EmpleadoBase`. |
| **Polimorfismo** | Cada clase hija sobreescribe `calcular_pago()`: la de planta paga salario + 30 % y el contratista paga solo el salario base. |

## Funciones propias (reto extra)

- `salario_promedio(empleados)`: promedio del `salario_base` de la nómina.
- `nomina_total(empleados)`: suma de `calcular_pago()` de todos los empleados (lo que la empresa paga al mes).

Ambas están documentadas con *docstring* y se llaman dentro de `ejecutar_quiz()`.

## Estructura del repositorio

```
quiz_semana3/
├── quiz_nomina.py     # Código completo (clases, lectura de Excel y funciones propias)
├── empleados.xlsx     # Datos de entrada (hoja Empleados + 2 hojas de ayuda)
├── requirements.txt   # Dependencias: pandas y openpyxl
└── README.md          # Este archivo
```

## Requisitos

- Python 3.8 o superior
- Librerías: `pandas` y `openpyxl`

## Instalación y ejecución

```bash
pip install -r requirements.txt
python quiz_nomina.py
```

> Ejecuta el comando desde la carpeta del proyecto, porque el programa busca `empleados.xlsx` en la carpeta actual.

## Resultado esperado

El programa muestra primero los avisos de las 5 filas inválidas y luego los 19 empleados que sí quedan en la nómina:

```
  [Aviso] Se ignoro Sofia: El salario no puede ser negativo.
  [Aviso] Fila incompleta ignorada.
  [Aviso] Se ignoro Gabriela: tipo desconocido 'TEMPORAL'
  [Aviso] Se ignoro Felipe: invalid literal for int() with base 10: 'no aplica'
  [Aviso] Fila incompleta ignorada.
--- Nomina ---
Ana | EmpleadoPlanta | Medellin | base $3000000 -> pago: 3900000.0
Luis | EmpleadoContratista | Bogota | base $2500000 -> pago: 2500000
...
Emilio | EmpleadoPlanta | Medellin | base $3300000 -> pago: 4290000.0

Total de empleados en nomina: 19
Salario promedio: $3,273,684.21
Nomina total mensual: $74,710,000.00
```

## Casos especiales del Excel

| Caso | Qué ocurre |
|------|-----------|
| Salario negativo (Sofía) | El setter lanza `ValueError` y la fila se ignora. |
| Sin nombre o sin tipo (ids 6 y 23) | Fila incompleta, se ignora. |
| Tipo `TEMPORAL` (Gabriela) | `crear_empleado()` lanza `ValueError`. |
| Salario en texto (Felipe) | `int("no aplica")` falla dentro del setter y se ignora. |
| Salario `0` (Santiago) | Entra: cero no es negativo. |
| Tipo `planta` en minúscula (Emilio) | Entra: `.strip().upper()` lo normaliza. |

## Nota

La función `leer_empleados_excel()` fue entregada por el docente y no se modificó.