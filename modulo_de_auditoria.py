import os
import csv
import datetime
from typing import Optional, Dict

class Auditor:
    def __init__(self, archivo_log: str = 'registro_auditoria.csv'):
        self.archivo_log = archivo_log
        self._verificar_inicio()

    def _verificar_inicio(self):
        """Crea el archivo CSV con encabezados si no existe."""
        if not os.path.exists(self.archivo_log):
            try:
                with open(self.archivo_log, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['FECHA_HORA', 'EVENTO', 'ARCHIVO', 'HASH', 'DETALLE'])
            except IOError as e:
                print(f"CRITICO: No se puede crear el archivo de log. {e}")

    def registrar_evento(self, evento: str, datos_archivo: Optional[Dict] = None, mensaje_extra: str = "") -> bool:
        """
        Escribe una línea en el historial.
        Args:
            evento (str): Ej. "ANALISIS_OK", "ARCHIVO_MOVIDO", "ERROR".
            datos_archivo (dict|None): El diccionario que viene del Analizador.
            mensaje_extra (str): Notas adicionales.
        Returns:
            bool: True si se registró correctamente, False en caso contrario.
        """
        datos_archivo = datos_archivo or {}
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        fila = [
            fecha_actual,
            evento,
            datos_archivo.get('nombre', 'DESCONOCIDO'),
            datos_archivo.get('hash_sha256', 'N/A'),
            f"{datos_archivo.get('peso_bytes', 0)} bytes | {mensaje_extra}"
        ]

        try:
            with open(self.archivo_log, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(fila)
            return True
        except Exception as e:
            print(f"FALLO DE AUDITORIA: No se pudo registrar el evento. {e}")
            return False


def iniciar_menu():
    """
    Función de enlace para que el main.py pueda ejecutar la interfaz de este módulo.
    """
    # Instanciamos el auditor para que esté listo para usarse
    auditor = Auditor()
    
    ejecutando = True
    while ejecutando:
        print("\n" + "="*40)
        print("          MÓDULO DE AUDITORÍA")
        print("="*40)
        print("1. Ver la ruta del archivo de registro")
        print("2. Registrar un evento de prueba")
        print("0. Volver al menú principal")
        print("-" * 40)
        
        try:
            opcion = int(input("Ingrese su opción: "))
            
            if opcion == 1:
                ruta_absoluta = os.path.abspath(auditor.archivo_log)
                print(f"\n[INFO] El archivo de auditoría se guarda en:\n{ruta_absoluta}")
            elif opcion == 2:
                # Prueba de la lógica de registro
                exito = auditor.registrar_evento("PRUEBA_MANUAL", None, "Este es un evento generado por el usuario.")
                if exito:
                    print("\n[ÉXITO] Evento de prueba registrado en el CSV.")
            elif opcion == 0:
                print("\n[INFO] Volviendo al menú principal...")
                ejecutando = False
            else:
                print("\n[ADVERTENCIA] Opción NO válida.")
                
        except ValueError:
            print("\n[ERROR] Por favor, ingrese un número entero.")