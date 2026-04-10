# Proyecto-Final.-Kit-Multifuncional-de-Automatizacion-de-Archivos
# Descripcion del Proyecto
Sistema desarrollado en Python para la automatización de tasks de gestion de archivos mediante linea de comandos, permite organizar, analizar, auditar y generar reportes sobre carpetas del sistema, aplicando principios de programacion estructurada y modular.
# Funcionalidades de los modulos
# main.py
- Menu principal unificado con interfaz CLI
- Gestion de flujo entre modulos
- Control centralizado de operaciones
# modulo_de_utilidades.py
- Sistema de logging: Registro automatico en audit.log
- Busqueda con regex: Deteccion de emails y números telefonicos
- Gestión de archivos: Lectura, validacion y conversion de formatos
- Utilidades de interfaz: Menus y entrada de usuario
# modulo_de_reportes.py
- Reportes de organizacion: Analisis de estructura de carpetas (TXT + CSV)
- Reportes de analisis: Extraccion de informacion especifica de contenido
- Reportes de auditoria: Documentacion de actividades del sistema
- Exportacion multiple: Formatos legibles y procesables
# modulo_organizador.py
- Clasificacion automatica: Por extension, tamaño y fecha
- Organizacion inteligente: Movimiento a carpetas categorizadas
- Modo simulacion: Previsualización sin aplicar cambios
- Renombrado con regex: Patrones personalizables
# modulo_de_analisis.py
- Analisis de contenido: Busqueda de patrones en archivos de texto
- Extraccion de datos: Emails, telefonos, fechas, palabras clave
- Generacion de resumenes: Frecuencias y estadisticas
- Procesamiento eficiente: Lectura de archivos grandes con generadores
# modulo_de_auditoria.py
- Deteccion de cambios: Comparacion mediante snapshots
- Registro historico: Actividades en registro_auditoria.csv
- Monitoreo en tiempo real: Seguimiento de operaciones del sistema
- Decoradores de auditoria: Registro automatico de funciones criticas
