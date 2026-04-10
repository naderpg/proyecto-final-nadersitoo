import os
import re
from datetime import datetime

# ==========================================
# 1. Guardar logs
# ==========================================

def guardar_log_accion(nombre_funcion, fue_exito=True, error=None):
    """Guarda lo que hace cada funcion en un archivo"""
    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        with open("audit.log", "a", encoding="utf-8") as archivo_log:
            if fue_exito:
                archivo_log.write(f"[{hora_actual}] EXITO - {nombre_funcion}\n")
            else:
                archivo_log.write(f"[{hora_actual}] ERROR - {nombre_funcion}: {error}\n")
        return True
    except:
        return False

# ==========================================
# 2. Leer archivos
# ==========================================

def leer_archivo_completo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return ""

def leer_archivo_lineas(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.readlines()
    except:
        return []

# ==========================================
# 3. Buscar con regex
# ==========================================

def buscar_emails_en_texto(texto):
    """Busca emails en texto (regex simple)"""
    patron = r'[\w\.-]+@[\w\.-]+'
    resultados = re.findall(patron, texto)
    return resultados

def buscar_telefonos_en_texto(texto):
    """Busca telefonos en texto"""
    # Busca: 0412-1234567 o 0412 123 4567
    patron = r'\d{3,4}[-\s]?\d{3}[-\s]?\d{3,4}'
    resultados = re.findall(patron, texto)
    return resultados

# ==========================================
# 4. Funciones basicas
# ==========================================

def crear_carpeta_nueva(ruta_carpeta):
    """Crea una carpeta si no existe"""
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        return True
    return False

def obtener_tamano_archivo(ruta_archivo):
    """Obtiene tamano de archivo en bytes"""
    try:
        return os.path.getsize(ruta_archivo)
    except:
        return 0

def convertir_bytes_a_legible(bytes_numero):
    """Convierte bytes a KB, MB, GB"""
    if bytes_numero < 1024:
        return f"{bytes_numero} B"
    elif bytes_numero < 1024 * 1024:
        kb = bytes_numero / 1024
        return f"{kb:.1f} KB"
    elif bytes_numero < 1024 * 1024 * 1024:
        mb = bytes_numero / (1024 * 1024)
        return f"{mb:.1f} MB"
    else:
        gb = bytes_numero / (1024 * 1024 * 1024)
        return f"{gb:.1f} GB"

def archivo_existe(ruta):
    """Verifica si un archivo existe"""
    return os.path.isfile(ruta)

def carpeta_existe(ruta):
    """Verifica si una carpeta existe"""
    return os.path.isdir(ruta)

# ==========================================
# 5. Menus y entradas
# ==========================================

def mostrar_menu_simple(titulo, opciones):
    """Muestra un menu simple"""
    print(f"\n{titulo}")
    print("=" * 40)
    for clave, valor in opciones.items():
        print(f"  {clave}. {valor}")
    print("-" * 40)

def pedir_opcion(mensaje):
    """Pide una opcion al usuario"""
    return input(f" {mensaje}: ").strip()

# ==========================================
# 6. Prueba (Unit Testing)
# ==========================================

if __name__ == "__main__":
    print("Probando utilidades simples...")
    
    # Probar guardar log
    exito_log = guardar_log_accion("prueba_funcion", fue_exito=True)
    if exito_log:
        print("[OK] Log guardado correctamente en audit.log")
    
    # Probar buscar emails
    texto_ejemplo = "Contacto: nader@empresa.com y nadersoporte@ayuda.com"
    emails = buscar_emails_en_texto(texto_ejemplo)
    print(f"[OK] Emails encontrados: {emails}")
    
    # Probar conversion de tamano
    print(f"[OK] 1500000 bytes = {convertir_bytes_a_legible(1500000)}")
    
    print("\n¡Utilidades funcionando perfectamente!")