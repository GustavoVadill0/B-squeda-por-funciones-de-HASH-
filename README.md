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




## 5. Colisiones y cómo resolverlas

Una **colisión** ocurre cuando dos claves diferentes producen el mismo índice:

```
h("Ana")     = 4
h("Ernesto") = 4   <- ¡colisión!
```

Las colisiones son inevitables cuando hay más claves que posiciones en la tabla. Existen dos grandes familias de estrategias para resolverlas:

---

### 5.1 Encadenamiento (Chaining)

Cada celda de la tabla contiene una **lista enlazada** con todos los elementos que colisionaron en ese índice.

```
Índice 4: -> ("Ana", 92) -> ("Ernesto", 88) -> NULL
```

**Ventajas:**
- Simple de implementar
- La tabla nunca se "llena" del todo
- La eliminación de elementos es sencilla

**Desventaja:**
- Memoria adicional por los punteros de la lista
- Si hay muchas colisiones, el tiempo de búsqueda puede degradarse a O(n)

---

### 5.2 Direccionamiento abierto (Open Addressing)

Todos los elementos se almacenan dentro de la propia tabla. Cuando hay colisión, se busca la **siguiente celda disponible** según una estrategia de sondeo.

#### a) Sondeo lineal (Linear Probing)

```
h'(k, i) = (h(k) + i) mod m     con i = 0, 1, 2, ...
```

Se avanza de celda en celda hasta encontrar una vacía.

**Problema:** Genera **agrupamiento primario** (clusters), donde las colisiones se acumulan en zonas continuas.

#### b) Sondeo cuadrático (Quadratic Probing)

```
h'(k, i) = (h(k) + c1*i + c2*i^2) mod m
```

Los saltos crecen cuadráticamente, reduciendo el agrupamiento primario. Sin embargo, puede generar **agrupamiento secundario**.

#### c) Doble hash (Double Hashing)

```
h'(k, i) = (h1(k) + i * h2(k)) mod m
```

Se usan dos funciones hash. Es el método de direccionamiento abierto que produce la distribución más uniforme y prácticamente elimina el agrupamiento.

---

## 6. Factor de carga

El **factor de carga** (`α`) mide qué tan llena está la tabla hash:

```
α = n / m
```

Donde:
- `n` = número de elementos almacenados
- `m` = tamaño de la tabla

| Factor de carga | Estado | Rendimiento |
|---|---|---|
| α < 0.5 | Tabla poco llena | Excelente |
| 0.5 ≤ α ≤ 0.75 | Uso óptimo | Bueno |
| α > 0.75 | Tabla muy llena | Empeora rápidamente |
| α = 1.0 | Tabla llena (solo con encadenamiento) | Muy bajo |

Cuando el factor de carga supera cierto umbral, se aplica **rehashing**: se crea una tabla más grande y se reinsertan todos los elementos.

---

## 7. Análisis de complejidad

### Complejidad temporal

| Operación | Caso promedio | Caso peor |
|---|---|---|
| **Búsqueda** | O(1) | O(n) |
| **Inserción** | O(1) | O(n) |
| **Eliminación** | O(1) | O(n) |

El caso promedio de **O(1)** se mantiene siempre que el factor de carga sea bajo (α ≤ 0.75) y la función hash distribuya bien.

### ¿Cuándo ocurre el peor caso O(n)?

El caso peor se da cuando **todas las claves colisionan en el mismo índice**, convirtiendo la búsqueda en un recorrido lineal por la lista de colisiones. Esto ocurre si:

- La función hash es deficiente (genera muchos índices repetidos)
- El factor de carga es demasiado alto
- Los datos tienen un patrón que la función hash no maneja bien

### Número esperado de comparaciones

Con encadenamiento y factor de carga `α`:

```
Búsqueda exitosa:    1 + α/2  comparaciones promedio
Búsqueda fallida:    α        comparaciones promedio
```

Con sondeo lineal:

```
Búsqueda exitosa:    (1/2) * (1 + 1/(1 - α))
Búsqueda fallida:    (1/2) * (1 + 1/(1 - α)^2)
```

A medida que `α` se acerca a 1, el número de comparaciones crece de forma no lineal, de ahí la importancia de controlar el factor de carga.

### Complejidad espacial

| Método | Espacio |
|---|---|
| Tabla hash básica | O(m) donde m es el tamaño de la tabla |
| Con encadenamiento | O(m + n) por los nodos de las listas |
| Con direccionamiento abierto | O(m), todo en el arreglo principal |

---

## 8. Casos de uso

### Cuándo ES la mejor opción

**1. Búsquedas frecuentes con clave exacta**
Cuando se necesita recuperar un elemento por su identificador único (ID de usuario, DNI, código de producto). La búsqueda directa en O(1) supera ampliamente a cualquier otro método.

**2. Implementación de diccionarios y conjuntos**
Lenguajes como Python (`dict`, `set`), Java (`HashMap`, `HashSet`) y JavaScript (`Map`, `Set`) usan tablas hash internamente por su eficiencia.

**3. Caché y memorización**
Almacenar resultados de cómputos costosos para evitar recalcularlos. La clave es la entrada, el valor es el resultado previo.

**4. Índices en bases de datos**
Los índices hash en bases de datos (como en PostgreSQL) permiten búsquedas por igualdad extremadamente rápidas en columnas con alta cardinalidad.

**5. Eliminación de duplicados**
Detectar si un elemento ya fue procesado o si una cadena ya apareció en un conjunto de datos grande.

**6. Tablas de símbolos en compiladores**
Los compiladores usan tablas hash para almacenar variables, funciones y tipos durante el análisis léxico y semántico.

### Cuándo NO es la mejor opción

| Situación | Método más adecuado |
|---|---|
| Búsqueda por rango (ej: edades entre 20 y 30) | Árbol binario de búsqueda, B-Tree |
| Datos que deben estar ordenados | Búsqueda binaria, árbol AVL |
| Memoria muy limitada | Búsqueda binaria sobre arreglo ordenado |
| Se requiere el elemento mínimo o máximo | Heap / árbol de búsqueda |
| Claves con patrones similares frecuentes | Trie (árbol de prefijos) |

---

## 9. Comparativa: Hash vs Búsqueda Binaria

La búsqueda binaria es el método más común que compite directamente con el hashing en escenarios de búsqueda estática o semi-estática.

| Criterio | Hash | Búsqueda Binaria |
|---|---|---|
| **Complejidad de búsqueda** | O(1) promedio | O(log n) |
| **Complejidad de inserción** | O(1) promedio | O(n) (desplazar elementos) |
| **Requisito de orden** | No requiere orden | Requiere datos ordenados |
| **Búsqueda por rango** | No soportada | Soportada |
| **Memoria adicional** | Sí (tabla + posibles listas) | Mínima (solo el arreglo) |
| **Predecibilidad** | Variable (depende de colisiones) | Consistente siempre |
| **Peor caso** | O(n) (muchas colisiones) | O(log n) garantizado |
| **Implementación** | Moderadamente compleja | Simple |
| **Datos dinámicos** | Muy eficiente | Costoso (reordenamiento) |

### Conclusión de la comparativa

- Usar **hash** cuando se prioriza la velocidad de búsqueda exacta y los datos cambian frecuentemente.
- Usar **búsqueda binaria** cuando se requieren operaciones de rango, el conjunto es estático, la memoria es escasa o se necesita un peor caso garantizado.

En la práctica, muchos sistemas combinan ambos: usan **índices hash** para búsquedas puntuales e **índices de árbol B** (que internamente se comportan como búsqueda binaria) para rangos y ordenamiento.

---

## 10. Ejemplo en Python

Implementación de una tabla hash con **encadenamiento** para resolver colisiones, en Python:

```python
class Nodo:
    """Nodo de la lista enlazada para encadenamiento."""
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None


class TablaHash:
    def __init__(self, tamaño=11):
        self.tamaño = tamaño          # Preferiblemente un número primo
        self.tabla = [None] * self.tamaño
        self.n_elementos = 0

    # Función hash
    def _hash(self, clave):
        """Convierte la clave a un índice válido dentro de la tabla."""
        if isinstance(clave, str):
            total = 0
            for caracter in clave:
                total = (total * 31 + ord(caracter)) % self.tamaño
            return total
        return clave % self.tamaño

    # Factor de carga
    @property
    def factor_de_carga(self):
        return self.n_elementos / self.tamaño

    # Inserción
    def insertar(self, clave, valor):
        idx = self._hash(clave)
        nodo = self.tabla[idx]

        # Si ya existe la clave, actualizamos el valor
        while nodo:
            if nodo.clave == clave:
                nodo.valor = valor
                return
            nodo = nodo.siguiente

        # Inserción al inicio de la lista enlazada
        nuevo = Nodo(clave, valor)
        nuevo.siguiente = self.tabla[idx]
        self.tabla[idx] = nuevo
        self.n_elementos += 1

    # Búsqueda
    def buscar(self, clave):
        idx = self._hash(clave)
        nodo = self.tabla[idx]

        while nodo:
            if nodo.clave == clave:
                return nodo.valor       # Encontrado
            nodo = nodo.siguiente

        return None                     # No encontrado

    # Eliminación
    def eliminar(self, clave):
        idx = self._hash(clave)
        nodo = self.tabla[idx]
        anterior = None

        while nodo:
            if nodo.clave == clave:
                if anterior:
                    anterior.siguiente = nodo.siguiente
                else:
                    self.tabla[idx] = nodo.siguiente
                self.n_elementos -= 1
                return True             # Eliminado con éxito
            anterior = nodo
            nodo = nodo.siguiente

        return False                    # No encontrado

    # Visualización de la tabla
    def mostrar(self):
        for i, nodo in enumerate(self.tabla):
            elementos = []
            actual = nodo
            while actual:
                elementos.append(f"({actual.clave}: {actual.valor})")
                actual = actual.siguiente
            contenido = " -> ".join(elementos) if elementos else "vacío"
            print(f"  [{i:2d}]  {contenido}")


# Demostración
if __name__ == "__main__":
    th = TablaHash(tamaño=11)

    th.insertar("Ana", 92)
    th.insertar("Luis", 78)
    th.insertar("Carlos", 85)
    th.insertar("María", 91)
    th.insertar("Ernesto", 74)

    print("=== Tabla Hash ===")
    th.mostrar()
    print(f"\nFactor de carga: {th.factor_de_carga:.2f}")

    print("\n=== Búsquedas ===")
    print(f"Buscar 'Carlos': {th.buscar('Carlos')}")    # -> 85
    print(f"Buscar 'Pedro':  {th.buscar('Pedro')}")     # -> None

    th.eliminar("Luis")
    print(f"\nBuscar 'Luis' tras eliminarlo: {th.buscar('Luis')}")  # -> None
```

### Salida esperada

```
=== Tabla Hash ===
  [ 0]  vacío
  [ 1]  (Ana: 92)
  [ 2]  vacío
  [ 3]  (Ernesto: 74)
  [ 4]  vacío
  [ 5]  (María: 91)
  [ 6]  (Carlos: 85)
  [ 7]  vacío
  [ 8]  vacío
  [ 9]  (Luis: 78)
  [10]  vacío

Factor de carga: 0.45
