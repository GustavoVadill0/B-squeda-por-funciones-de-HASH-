import time

class TablaHashDirecta:
    def __init__(self, tamaño):
        self.tamaño = tamaño
        self.tabla = [[] for _ in range(tamaño)]

    def _función_hash(self, llave):
        return llave % self.tamaño

    def insertar(self, valor):
        índice = self._función_hash(valor)
        self.tabla[índice].append(valor)

    def obtener_datos_organizados(self):
        datos_resultado = []
        for casilla in self.tabla:
            if casilla:
                casilla.sort()  
                datos_resultado.extend(casilla)
        return datos_resultado

    def buscar(self, valor_a_buscar):
        índice = self._función_hash(valor_a_buscar)
        
        if valor_a_buscar in self.tabla[índice]:
            return True
        return False


def ejecutar_proceso_hash(archivo_entrada, archivo_salida):
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
            lista_números = [int(n) for n in contenido.split()]
        
        tamaño_calculado = max(11, len(lista_números) * 2)
        tabla_hash = TablaHashDirecta(tamaño_calculado)

        inicio_estructura = time.time()
        for número in lista_números:
            tabla_hash.insertar(número)
        números_procesados = tabla_hash.obtener_datos_organizados()
        fin_estructura = time.time()
        
        tiempo_estructura_ms = (fin_estructura - inicio_estructura) * 1000
        
        with open(archivo_salida, 'w', encoding='utf-8') as f_out:
            f_out.write(" ".join(map(str, números_procesados)))
        
        print("==================================================")
        print("Proceso por Función Hash estructurado con éxito.")
        print(f"Tiempo de carga y ordenamiento: {tiempo_estructura_ms:.4f} ms")
        print(f"Los datos guardados en: {archivo_salida}")
        print("==================================================\n")

        número_buscado = int(input("Introduce el número que deseas buscar en la tabla Hash: "))
        
        inicio_búsqueda = time.time()
        encontrado = tabla_hash.buscar(número_buscado)
        fin_búsqueda = time.time()
        
        tiempo_búsqueda_ms = (fin_búsqueda - inicio_búsqueda) * 1000
        
        print("\n--------------------------------------------------")
        if encontrado:
            print(f"¡Resultado! El número {número_buscado} SÍ se encuentra en la tabla.")
        else:
            print(f"¡Resultado! El número {número_buscado} NO existe en los datos.")
            
        print(f"Tiempo empleado en la búsqueda: {tiempo_búsqueda_ms:.6f} ms")
        print("--------------------------------------------------")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo_entrada}'.")
    except ValueError:
        print("Error: Por favor introduce un número entero válido.")

ejecutar_proceso_hash('datos.txt', 'resultado_hash.txt')