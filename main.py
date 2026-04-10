# main.py
"""
Módulo principal del Kit Multifuncional de Automatización de Archivos.
Implementa el menú interactivo CLI (Command Line Interface) y gestiona las
llamadas a los módulos de organización, análisis, auditoría y reportes.
"""
import sys

# Importamos los módulos del equipo
try:
    import modulo_organizador
    import modulo_de_analisis
    import modulo_de_auditoria
    import modulo_de_reportes
    import modulo_de_utilidades
except ImportError as e:
    print(f"[ERROR] No se pudo encontrar el módulo {e.name}. Verifique los archivos .py.")
    # sys.exit(1) # Te recomiendo comentar esta línea temporalmente para probar el menú principal aunque no tengas los otros archivos creados.


def mostrar_menu_principal():
    """Muestra el menú principal con las funcionalidades requeridas."""
    print("\n" + "="*50)
    print("      KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN")
    print("="*50)
    print("1. Gestor de Organización de Archivos") 
    print("2. Analizador de Contenido") 
    print("3. Auditor de Cambios")
    print("4. Generador de Reportes")
    print("0. Salir")
    print("-" * 50)


def ejecutar_opcion(opcion):
    """
    Gestiona la opción elegida y llama a la función principal del módulo correspondiente.
    """
    if opcion == 1:
        print("[INFO] Iniciando Módulo de Organización...")
        # modulo_organizador.iniciar_menu() 
    elif opcion == 2:
        print("[INFO] Iniciando Módulo de Análisis de Contenido...")
        # modulo_de_analisis.iniciar_menu()
    elif opcion == 3:
        print("[INFO] Iniciando Módulo de Auditoría...")
        # modulo_de_auditoria.iniciar_menu()
    elif opcion == 4:
        print("[INFO] Iniciando Generador de Reportes...")
        # modulo_de_reportes.iniciar_menu()
    elif opcion == 0:
        print("Saliendo del Kit Multifuncional.")
        return False
    else:
        print("[ADVERTENCIA] Opción NO válida. Selecciona un número del 0 al 4.")
    
    return True


def main():
    """Función principal del programa. Contiene el bucle de ejecución."""
    ejecutando = True
    while ejecutando:
        mostrar_menu_principal()
        
        try:
            entrada = input("Ingrese su opción: ")
            opcion = int(entrada)
            ejecutando = ejecutar_opcion(opcion)
        except ValueError:
            print("[ERROR] La entrada debe ser un número entero.")
        except KeyboardInterrupt:
            # Maneja la interrupción si el usuario presiona Ctrl+C
            print("\n[SALIDA] Interrupción detectada. Saliendo.")
            sys.exit(0)
        except Exception as e:
            print(f"[ERROR] Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    main()