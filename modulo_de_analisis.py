import os
import hashlib
import mimetypes

class Analizador:
    def __init__(self):
        # Inicializamos mimetypes para adivinar tipos de archivo
        mimetypes.init()

    def _calcular_hash(self, ruta_archivo):
        """Genera la huella digital SHA-256 para verificar integridad."""
        sha256 = hashlib.sha256()
        try:
            with open(ruta_archivo, 'rb') as f:
                # Leemos en bloques de 64kb para no saturar la memoria RAM
                while True:
                    bloque = f.read(65536)
                    if not bloque: break
                    sha256.update(bloque)
            return sha256.hexdigest()
        except PermissionError:
            return "ERROR_PERMISO"
        except Exception as e:
            return f"ERROR_{str(e)}"

    def escanear(self, ruta_archivo):
        """Devuelve un diccionario completo con los signos vitales del archivo."""
        if not os.path.exists(ruta_archivo):
            return {"existe": False, "error": "No encontrado"}

        stats = os.stat(ruta_archivo)
        nombre = os.path.basename(ruta_archivo)
        tipo_mime, _ = mimetypes.guess_type(ruta_archivo)

        datos = {
            "existe": True,
            "nombre": nombre,
            "ruta_absoluta": os.path.abspath(ruta_archivo),
            "extension": os.path.splitext(nombre)[1].lower(),
            "tipo_mime": tipo_mime or "desconocido",
            "peso_bytes": stats.st_size,
            "hash_sha256": self._calcular_hash(ruta_archivo)
        }
        return datos


def iniciar_menu():
    """
    Función de enlace para que el main.py pueda ejecutar la interfaz de este módulo.
    """
    analizador = Analizador()
    ejecutando = True
    
    while ejecutando:
        print("\n" + "="*40)
        print("          MÓDULO DE ANÁLISIS")
        print("="*40)
        print("1. Analizar un archivo específico")
        print("0. Volver al menú principal")
        print("-" * 40)
        
        try:
            opcion = int(input("Ingrese su opción: "))
            
            if opcion == 1:
                ruta = input("\nIngrese la ruta exacta del archivo a analizar: ")
                # Eliminamos posibles comillas si el usuario arrastra el archivo a la consola
                ruta = ruta.strip('"').strip("'") 
                
                print("[INFO] Analizando...")
                resultados = analizador.escanear(ruta)
                
                print("\n--- Resultados del Análisis ---")
                if not resultados.get("existe"):
                    print(f"[ERROR] El archivo no existe o la ruta es incorrecta: {ruta}")
                else:
                    for clave, valor in resultados.items():
                        # Imprimimos el diccionario de forma limpia
                        print(f"{clave.upper()}: {valor}")
            
            elif opcion == 0:
                print("\n[INFO] Volviendo al menú principal...")
                ejecutando = False
            else:
                print("\n[ADVERTENCIA] Opción NO válida.")
                
        except ValueError:
            print("\n[ERROR] Por favor, ingrese un número entero.")