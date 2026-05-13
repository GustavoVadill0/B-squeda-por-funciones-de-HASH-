## ¿Qué es?

El método hash es una técnica de búsqueda que permite localizar elementos de forma muy rápida, sin necesidad de tener los datos ordenados. Su mayor ventaja es que el tiempo que tarda en encontrar un elemento es casi el mismo sin importar cuántos datos haya en el arreglo. Funciona asi:

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
Funciones Hash
---

## 1.  Función Módulo (por división)

Es la más usada y sencilla. Divide la clave entre el tamaño del arreglo y usa el **residuo** como dirección.

**Fórmula:**
```
H(K) = (K mod N) + 1
```

### Ejemplo paso a paso:
```
K = 259,  N = 11 (primo)

259 ÷ 11 = 23  con residuo 6

H(259) = 6 + 1 = 7  → se guarda en la posición 7
```

### ¿Por qué N debe ser primo?

| N es primo | N NO es primo |
|---|---|
| Las claves se distribuyen uniformemente | Muchas claves caen en las mismas posiciones |
| Menos colisiones | Más colisiones |
| Recomendado |  No recomendado |

> Si N no es primo, muchas claves tienden a caer en las mismas posiciones, generando más colisiones.

---

## 2.  Función Centro de Cuadrados

Eleva la clave al cuadrado y toma los dígitos del **centro** del resultado.

**Fórmula:**
```
H(K) = dígitos_centrales(K²) + 1
```

### Ejemplo paso a paso:
```
K = 123

K² = 123 × 123 = 15,129

Resultado:  1  5  1  2  9
                  ↑  ↑
         dígitos centrales = 12

H(123) = 12 + 1 = 13  → posición 13
```

### ¿Cuántos dígitos tomar del centro?

Depende del tamaño del arreglo:

| Tamaño del arreglo | Dígitos a tomar |
|---|---|
| Hasta 99 posiciones | 2 dígitos |
| Hasta 999 posiciones | 3 dígitos |
| Hasta 9,999 posiciones | 4 dígitos |

> Los dígitos del centro tienden a mezclar mejor los valores de la clave, lo que produce una distribución más uniforme.

---

## 3. Función Plegamiento

Divide la clave en partes iguales y las **suma**. Luego toma los dígitos menos significativos (los de la derecha) como dirección.

**Fórmula:**
```
H(K) = díg_menos_significativos(parte1 + parte2 + ... + parteN) + 1
```

### Ejemplo paso a paso:
```
K = 87304251  (arreglo de 3 dígitos → partes de 3 en 3)

Paso 1 — Dividir la clave en partes:
  873 | 042 | 51
  (la última parte puede tener menos dígitos)

Paso 2 — Sumar las partes:
  873 + 042 + 051 = 966

Paso 3 — Tomar los dígitos menos significativos:
  966 → los 3 últimos dígitos = 966

H(K) = 966 + 1 = 967  → posición 967
```

### Variantes del plegamiento

| Variante | Operación | Cuándo usarla |
|---|---|---|
| **Suma** | parte1 + parte2 + ... | Caso general, más común |
| **Multiplicación** | parte1 × parte2 × ... | Cuando se quiere mayor dispersión |

> Es especialmente útil cuando las claves son muy largas, ya que aprovecha todos sus dígitos.

---

## 4. Función Truncamiento

La más simple de todas. Solo **selecciona algunos dígitos** de la clave y los usa directamente como dirección.

**Fórmula:**
```
H(K) = elegir_dígitos(d1, d2, ..., dn) + 1
```

### Ejemplo paso a paso:
```
K = 84756231  (arreglo de 3 posiciones → tomamos 3 dígitos)

Posiciones:  8  4  7  5  6  2  3  1
             1° 2° 3° 4° 5° 6° 7° 8°

Elegimos el 2°, 5° y 8° dígito:
             4     6           1

H(K) = 461 + 1 = 462  → posición 462
```

### Formas de elegir los dígitos

| Criterio | Ejemplo con K = 84756231 |
|---|---|
| Primeros dígitos | 8, 4, 7 → 847 |
| Últimos dígitos | 2, 3, 1 → 231 |
| Dígitos alternos | 8, 7, 6, 3 → 8763 |
| Posiciones fijas | 2°, 5°, 8° → 461 |

>  Su mayor debilidad es que si se eligen mal los dígitos, muchas claves terminarán en la misma posición, generando colisiones.

---

Tipos de Busqueda Hash

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


