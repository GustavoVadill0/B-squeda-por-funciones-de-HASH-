 Búsqueda por Función Hash (Hash Lookup)

## ¿Qué es?

La **búsqueda hash** es una técnica que permite encontrar y reemplazar valores en una base de datos de forma rápida y segura. Funciona así:

1. Toma un valor de una **columna de origen**
2. Le aplica una **función hash** → obtiene un número único
3. Usa ese número para buscar una fila en una **tabla de búsqueda**
4. Inserta el valor encontrado en la **columna de destino**

> Es muy útil para **enmascarar datos sensibles** de forma consistente: el mismo valor de origen siempre producirá el mismo hash, en cualquier entorno.

---

## ¿Cómo funciona internamente?

```
Valor original  →  Función Hash  →  Número (clave)  →  Tabla de búsqueda  →  Valor reemplazado
"Juan García"         SHA-256           4821              fila 4821            "Persona_A"
```

Si el número generado por el hash **no existe** en la tabla de búsqueda, ocurre un **error de conversión**.

---

## Tipos de búsqueda hash

| Tipo | Descripción |
|---|---|
| **Columna única** | Se aplica hash a una sola columna de origen |
| **Columna múltiple** | Se aplica hash a varias columnas a la vez (máximo 16) |

---

## La tabla de búsqueda

La tabla de búsqueda es el corazón del proceso. Debe cumplir estas reglas:

- Estar **indexada**
- Tener una **columna clave numérica** con valores secuenciales (sin saltos)
- Incluir filas especiales para valores reservados:

| Valor de origen | Clave en la tabla |
|---|---|
| `NULL` | `-1` |
| Espacios (CHAR o VARCHAR) | `-2` |
| VARCHAR de longitud cero | `-3` |

> Estos valores especiales **no se someten a hash**, por eso necesitan filas propias en la tabla.

---

## Parámetros principales

### `sourcesearchcol`
Columna de origen de la que se toman los valores para calcular el hash.
> No tiene que ser necesariamente la columna que se va a reemplazar.

### `SRCSEARCH=`
Para búsquedas en **múltiples columnas**. Se listan los nombres separados por comas.
```
SRCSEARCH=(nombre, apellido, email)
```

### `trim=`
Permite limpiar el valor **antes** de aplicar el hash. Útil para normalizar datos:
- Eliminar caracteres específicos (comas, espacios, etc.)
- Convertir a mayúsculas con `\u`

**Ejemplo práctico:** Si eliminas las comas, entonces `"García, Juan"` y `"García Juan"` producirán el **mismo hash**.

### `dest=`
Columnas de destino donde se insertarán los valores encontrados en la tabla de búsqueda. Obligatorio en búsquedas de múltiples columnas.

### `ALGO=`
Algoritmo usado para calcular el hash:

| Valor | Descripción |
|---|---|
| `SHA256` | Algoritmo SHA-256 (más seguro, recomendado) |
| `DEFAULT` | Algoritmo hash predeterminado del sistema |

### `cache` / `nocache`
Controla si los resultados se guardan en memoria:

| Opción | Ventaja | Desventaja |
|---|---|---|
| `cache` (predeterminado) | Más rápido al repetir búsquedas | Consume más memoria |
| `nocache` | Menos uso de memoria | Más lento en valores repetidos |

### `PRESERVE=`
Define qué hacer cuando **no se encuentra** un valor en la tabla:
- `NOT_FOUND` → inserta el valor original tal cual en el destino
- También permite definir comportamiento para `NULL`, `SPACES` y `ZERO_LEN`

### `seed=`
Un valor adicional que **varía el cálculo del hash**, añadiendo una capa extra de seguridad:
- Puede ser un número del `1` al `2,000,000,000`
- O `HMAC` para usar una clave externa (solo con `ALGO=SHA256`)

---

## Sintaxis completa

```sql
HASH_LOOKUP(
  { sourcesearchcol | SRCSEARCH=(col1,...,coln) }
  [, trim=([caracteres][\u]) ]
  [, dest=(col1,...,coln) ]
  , nombre_tabla_busqueda (columna_clave, { columna_valor | values=(col1,...,coln) })
  [, ALGO={ SHA256 | DEFAULT } ]
  [, cache | nocache ]
  [, PRESERVE=([NOT_FOUND,] colname(SPACES, NULL, ZERO_LEN)...) ]
  [, seed={ n | HMAC } ]
)
```

---

## Hashing vs. Búsqueda Hash — ¿cuál es la diferencia?

| Concepto | Descripción |
|---|---|
| **Hashing** | El proceso general de transformar un dato en un código único e irreversible |
| **Búsqueda hash** | Uso específico del hashing para **localizar y reemplazar** valores en una tabla |

> El hashing es el motor. La búsqueda hash es una de sus aplicaciones prácticas.

---


