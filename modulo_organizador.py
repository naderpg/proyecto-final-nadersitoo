import os
import shutil
from datetime import datetime
from functools import wraps

# ============================
# DECORADOR PARA AUDITAR ACCIONES
# ============================
def auditor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            resultado = func(*args, **kwargs)
            log_action(f"SUCCESS: {func.__name__} ejecutada correctamente.")
            return resultado
        except Exception as e:
            log_action(f"ERROR: {func.__name__} falló -> {str(e)}")
            raise
    return wrapper

# ============================
# FUNCIÓN PARA REGISTRAR AUDITORÍA
# ============================
def log_action(message: str, logfile: str = "audit.log"):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(logfile, "a", encoding="utf-8") as log:
        log.write(f"{timestamp} {message}\n")

# ============================
# GENERADOR DE ARCHIVOS
# ============================
def generar_archivos(path):
    """Genera rutas de archivos dentro de un directorio (no recursivo)."""
    try:
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    yield entry.path
    except FileNotFoundError:
        raise
    except PermissionError as e:
        raise e

# ============================
# CLASIFICADOR DE ARCHIVOS
# ============================
CATEGORIAS = {
    "imagenes": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"],
    "documentos": [".pdf", ".docx", ".doc", ".txt", ".odt", ".xlsx", ".pptx"],
    "videos": [".mp4", ".mov", ".avi", ".mkv"],
    "audio": [".mp3", ".wav", ".flac"],
    "comprimidos": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "python": [".py"],
}


def _unique_dest(path):
    """Genera una ruta única si ya existe el archivo destino."""
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base} ({counter}){ext}"
        counter += 1
    return new_path


@auditor
def clasificar_archivos(directorio: str):
    """Clasifica archivos en carpetas según su extensión dentro del directorio dado."""
    if not os.path.exists(directorio):
        raise FileNotFoundError("El directorio no existe.")

    directorio = os.path.abspath(directorio)

    for ruta_archivo in generar_archivos(directorio):
        extension = os.path.splitext(ruta_archivo)[1].lower()
        nombre_archivo = os.path.basename(ruta_archivo)

        categoria_destino = None

        # Buscar la categoría correspondiente
        for categoria, extensiones in CATEGORIAS.items():
            if extension in extensiones:
                categoria_destino = categoria
                break

        # Si no hay categoría, va a 'otros'
        if categoria_destino is None:
            categoria_destino = "otros"

        carpeta_destino = os.path.join(directorio, categoria_destino)

        # Crear carpeta si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        destino = os.path.join(carpeta_destino, nombre_archivo)

        # Evitar mover si ya está en la carpeta correcta
        if os.path.dirname(ruta_archivo) == carpeta_destino:
            continue

        # Asegurar destino único
        destino_unico = _unique_dest(destino)

        # Mover archivo
        shutil.move(ruta_archivo, destino_unico)

    print("[ÉXITO] Archivos clasificados exitosamente.")


# ============================
# MENÚ PRINCIPAL (ENLACE CON MAIN.PY)
# ============================
def iniciar_menu():
    """Interfaz iterativa del módulo de organización."""
    ejecutando = True
    while ejecutando:
        print("\n" + "="*40)
        print("  MÓDULO DE ORGANIZACIÓN DE ARCHIVOS")
        print("="*40)
        print("1. Organizar una carpeta por extensiones")
        print("0. Volver al menú principal")
        print("-" * 40)
        
        try:
            opcion = input("Ingrese su opción: ")
            
            if opcion == '1':
                ruta = input("\nIngresa la ruta de la carpeta a organizar (Enter para usar la actual): ").strip()
                # Limpiamos las comillas en caso de drag and drop en la consola
                ruta = ruta.strip('"').strip("'")
                
                if not ruta:
                    ruta = "."
                
                print(f"[INFO] Procesando el directorio: {os.path.abspath(ruta)}")
                try:
                    clasificar_archivos(ruta)
                except Exception as e:
                    print(f"[ERROR] Ocurrió un problema durante la clasificación: {e}")
            
            elif opcion == '0':
                print("\n[INFO] Volviendo al menú principal...")
                ejecutando = False
            else:
                print("\n[ADVERTENCIA] Opción NO válida.")
                
        except KeyboardInterrupt:
            print("\n[INFO] Operación cancelada por el usuario. Volviendo...")
            ejecutando = False

if __name__ == "__main__":
    iniciar_menu()