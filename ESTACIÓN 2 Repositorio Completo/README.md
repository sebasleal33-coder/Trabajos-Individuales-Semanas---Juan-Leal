# Sistema de Gestión de Transacciones — Estación 2 (Segunda entrega)

Sistema en Python que integra, en un solo proyecto, los componentes desarrollados en el núcleo **Fundamentos de Software**: programación orientada a objetos, tolerancia a fallos, serialización JSON y control de versiones con Git y GitHub.

## Autor

| Dato | Detalle |
|---|---|
| Autor | Juan Sebastián Leal Suárez |
| Institución | Fundación Universitaria CEIPA — Ingeniería de Sistemas |
| Núcleo | Fundamentos de Software |
| Docente | Simón Peláez Loaiza |
| Fecha de entrega | 22 de noviembre de 2026 |
| Modalidad | Trabajo individual |

## ¿Qué hace el sistema?

1. **Lee** un archivo de texto con líneas `ID,TIPO,MONTO` y crea objetos `TransaccionCredito` o `TransaccionDebito`.
2. **Tolera los datos dañados**: si una línea falla (tipo desconocido, monto negativo, monto no numérico o columnas faltantes), la registra en un log y continúa con la siguiente.
3. **Procesa** las transacciones: monto total, impacto total (interés de créditos y comisión de débitos) y filtros por tipo.
4. **Persiste** los objetos en `salida/transacciones.json` y los reconstruye desde el archivo.
5. **Reporta** el resultado en texto plano o en JSON.

## Estructura del repositorio

```
Estacion-2-Sistema-Transacciones/
├── main.py                      # Punto de entrada: integra todos los componentes
├── transacciones/               # Paquete principal
│   ├── config.py                # Tasa de interés y comisión fija
│   ├── modelos.py               # POO: encapsulamiento, herencia, polimorfismo
│   ├── gestor.py                # Operaciones sobre listas de transacciones
│   ├── lector.py                # Lectura .txt tolerante a fallos (try-except + logging)
│   ├── persistencia.py          # Serialización y deserialización JSON
│   └── reportes.py              # Reportes en texto o JSON (abierto a extensión)
├── datos/
│   ├── Transacciones.txt            # Datos de prueba (8 válidas, 3 inválidas)
│   └── transacciones_corruptas.txt  # Datos de prueba con 3 errores de distinto tipo
├── salida/
│   └── transacciones.json       # Ejemplo del archivo generado por el sistema
├── tests/
│   └── test_transacciones.py    # 15 pruebas unitarias (unittest)
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 o superior.
- No requiere instalar librerías externas (solo usa la biblioteca estándar).

## Cómo ejecutarlo

Desde la carpeta raíz del proyecto:

```bash
# Ejecución normal (usa datos/Transacciones.txt)
python main.py

# Con el archivo de datos corruptos
python main.py --entrada datos/transacciones_corruptas.txt

# Reporte en formato JSON
python main.py --reporte json

# Pruebas unitarias
python -m unittest discover -s tests -v
```

Cada ejecución genera `registro_errores.log` (auditoría de los registros rechazados; no se sube al repositorio) y `salida/transacciones.json`.

## Componentes y conceptos aplicados

### Programación orientada a objetos (Semana 3)

| Pilar | Dónde se ve |
|---|---|
| Encapsulamiento | `TransaccionBase`: atributos privados `_transaccion_id` y `_monto`, con getters y setters que validan |
| Herencia | `TransaccionCredito` y `TransaccionDebito` heredan de `TransaccionBase` (clase abstracta) |
| Polimorfismo | `calcular_impacto()`: interés en créditos, comisión fija en débitos; el gestor lo llama sin preguntar el tipo |

### Principios SOLID (Semana 3)

- **SRP**: cada módulo tiene una sola responsabilidad (validar y modelar, leer, procesar, persistir, reportar).
- **OCP**: para agregar un tipo de transacción se crea una clase hija y se registra en `TIPOS_TRANSACCION`; para agregar un formato de reporte se crea una clase hija de `ReporteBase` y se registra en `FORMATOS_REPORTE`. No se modifica código existente.

### Tolerancia a fallos (Semana 4, Actividad 1)

El `try-except` vive **dentro** del bucle de lectura (`lector.py`), de modo que cada línea se protege por separado: una línea corrupta se registra con `logging` y la carga continúa.

| Error | Ejemplo | Resultado |
|---|---|---|
| Tipo no registrado | `C009,EFECTIVO,1500000` | Línea rechazada |
| Monto negativo | `C010,DEBITO,-2000000` | Línea rechazada por el setter |
| Monto no numérico | `C003,DEBITO,texto_invalido` | Línea rechazada |
| Columnas faltantes | `C006,CREDITO` | Línea rechazada |

### Serialización y persistencia JSON (Semana 4, Actividad 2)

```
Serializar:    Objeto -> Diccionario -> Texto JSON
Deserializar:  Texto JSON -> Diccionario -> Objeto (llamando al constructor)
```

Al deserializar se validan las claves obligatorias y los datos pasan de nuevo por los setters; un registro dañado se aísla y el resto se recupera.

### Control de versiones (Semana 5)

El proyecto se gestiona con Git y se publica en GitHub, con historial de commits por componente y ramas por funcionalidad (ver la siguiente sección).

## Flujo de trabajo con Git

**Ramas**

| Rama | Propósito |
|---|---|
| `main` | Versión estable y entregable |
| `feature/poo` | Clases del dominio y gestor |
| `feature/excepciones` | Lectura tolerante a fallos y logging |
| `feature/json` | Serialización y persistencia |
| `feature/reportes` | Reportes y punto de entrada |
| `docs` | README y documentación |

**Convención de mensajes de commit**: prefijo + descripción corta en imperativo (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).

Ejemplo: `feat: agrega validación del monto en el setter de TransaccionBase`.

## Pruebas

Las 15 pruebas unitarias cubren encapsulamiento, herencia, polimorfismo, el gestor, la lectura tolerante a fallos y la serialización, incluidos los casos de error.

## Uso de inteligencia artificial

Este proyecto se elaboró con apoyo de Claude (Anthropic, 2026) para la integración de los módulos, la redacción de la documentación y la generación de las pruebas unitarias. El autor revisó, ejecutó y validó el código, y es responsable del resultado entregado.
