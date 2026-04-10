import os
import csv
from datetime import datetime

# Cambiamos la importación a utilidades, ya que las funciones llamadas (como convertir_bytes_a_legible) 
# seguramente residen en ese módulo, no en el de análisis.
try:
    import modulo_de_utilidades as ut
except ImportError:
    print("[ADVERTENCIA] No se encontró modulo_de_utilidades.py. Algunas funciones podrían fallar.")


def reporte_carpeta(carpeta="."):
    """Crea reporte TXT y CSV de una carpeta"""
    print(f"\n[INFO] Reporte de: {carpeta}")
    
    # Asumiendo que ut.carpeta_existe está en tu módulo de utilidades
    if not ut.carpeta_existe(carpeta):
        print("[ERROR] La carpeta no existe.")
        return False
    
    # Crear carpeta reportes
    os.makedirs("reportes", exist_ok=True)
    
    # Leer archivos
    archivos = []
    for nombre in os.listdir(carpeta):
        ruta = os.path.join(carpeta, nombre)
        if os.path.isfile(ruta):
            tam = os.path.getsize(ruta)
            archivos.append({
                'nombre': nombre,
                'tamano': ut.convertir_bytes_a_legible(tam),
                'tipo': f".{nombre.split('.')[-1]}" if '.' in nombre else "sin_ext"
            })
    
    # TXT
    fecha = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"reportes/reporte_{fecha}.txt", "w", encoding='utf-8') as f:
        f.write(f"CARPETA: {carpeta}\nArchivos: {len(archivos)}\n\n")
        # Guardamos solo los primeros 10 en el TXT como resumen
        for a in archivos[:10]:
            f.write(f"{a['nombre']} - {a['tamano']} - {a['tipo']}\n")
    
    # CSV
    with open(f"reportes/reporte_{fecha}.csv", "w", newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['Nombre', 'Tamano', 'Tipo'])
        for a in archivos:
            w.writerow([a['nombre'], a['tamano'], a['tipo']])
    
    print(f"[ÉXITO] Creados: reporte_{fecha}.txt y .csv")
    ut.guardar_log_accion("reporte_carpeta")
    return True


def reporte_analisis(ruta):
    """Analiza archivos .txt extrayendo emails y teléfonos."""
    print(f"\n[INFO] Analizando: {ruta}")
    
    emails = []
    telefonos = []
    
    if os.path.isfile(ruta) and ruta.endswith('.txt'):
        texto = ut.leer_archivo_completo(ruta)
        emails = ut.buscar_emails_en_texto(texto)
        telefonos = ut.buscar_telefonos_en_texto(texto)
        
    elif os.path.isdir(ruta):
        for nombre in os.listdir(ruta):
            if nombre.endswith('.txt'):
                texto = ut.leer_archivo_completo(os.path.join(ruta, nombre))
                emails.extend(ut.buscar_emails_en_texto(texto))
                telefonos.extend(ut.buscar_telefonos_en_texto(texto))
    else:
        print("[ERROR] Ruta no válida o no es un archivo .txt")
        return False
    
    # Crear carpeta reportes si no existe
    os.makedirs("reportes", exist_ok=True)
    
    # Crear reporte
    fecha = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"reportes/analisis_{fecha}.txt", "w", encoding='utf-8') as f:
        f.write(f"EMAILS ({len(emails)}):\n")
        for e in emails:
            f.write(f"{e}\n")
        f.write(f"\nTELEFONOS ({len(telefonos)}):\n")
        for t in telefonos:
            f.write(f"{t}\n")
            
    print("[ÉXITO] Reporte de análisis creado.")
    ut.guardar_log_accion("reporte_analisis")
    return True


def reporte_auditoria():
    """Genera un reporte extrayendo las últimas actividades del audit.log"""
    print("\n[INFO] Generando reporte de auditoría...")
    
    actividades = []
    if os.path.exists("audit.log"):
        with open("audit.log", "r", encoding='utf-8') as f:
            # Leemos todas las líneas y tomamos las últimas 10
            actividades = f.readlines()[-10:]
    else:
        print("[ADVERTENCIA] No se encontró el archivo audit.log")
        return False
        
    # Crear carpeta reportes si no existe
    os.makedirs("reportes", exist_ok=True)
        
    fecha = datetime.now().strftime("%Y%m%d_%H%M")
    with open(f"reportes/auditoria_{fecha}.txt", "w", encoding='utf-8') as f:
        f.write(f"ÚLTIMAS ACTIVIDADES ({len(actividades)}):\n")
        for a in actividades:
            f.write(a)
            
    print("[ÉXITO] Reporte de auditoría creado.")
    ut.guardar_log_accion("reporte_auditoria")
    return True


def iniciar_menu():
    """
    Función de enlace renombrada para que el main.py la reconozca.
    """
    # Crear carpeta reportes si no existe desde el inicio
    os.makedirs("reportes", exist_ok=True)
    
    ejecutando = True
    while ejecutando:
        print("\n" + "="*40)
        print("          MÓDULO DE REPORTES")
        print("="*40)
        print("1. Reporte de carpeta")
        print("2. Reporte de análisis de texto")
        print("3. Reporte de auditoría")
        print("0. Volver al menú principal")
        print("-" * 40)
        
        try:
            opcion = input("Ingrese su opción: ")
            
            if opcion == '1':
                carpeta = input("Ingrese la ruta de la carpeta (Enter para la actual): ")
                if carpeta.strip() == "":
                    carpeta = "."
                reporte_carpeta(carpeta)
            elif opcion == '2':
                ruta = input("Ingrese el archivo o carpeta a analizar: ")
                # Limpiamos las comillas en caso de drag and drop
                ruta = ruta.strip('"').strip("'")
                reporte_analisis(ruta)
            elif opcion == '3':
                reporte_auditoria()
            elif opcion == '0':
                print("\n[INFO] Volviendo al menú principal...")
                ejecutando = False
            else:
                print("\n[ADVERTENCIA] Opción NO válida.")
        
        except KeyboardInterrupt:
            print("\n[INFO] Operación cancelada por el usuario. Volviendo al menú...")
            ejecutando = False
        except Exception as e:
            print(f"\n[ERROR] Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    iniciar_menu()