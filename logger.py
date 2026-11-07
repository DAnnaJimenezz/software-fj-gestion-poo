"""
logger.py
Registro de eventos y errores del sistema Software FJ.

Es el ÚNICO módulo que escribe en el archivo de logs (logs/sistema.log).
El resto del proyecto solo debe llamar a registrar_evento(nivel, mensaje).
"""

import logging  # Módulo estándar de Python para registrar eventos
import os  # Módulo estándar para manejar rutas y carpetas
import sys  # Módulo estándar, se usa para mostrar un aviso si el log falla

NIVELES_VALIDOS = ("INFO", "WARNING", "ERROR")  # Niveles aceptados por el sistema
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")  # Carpeta junto a este archivo
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "sistema.log")  # Ruta completa del archivo de logs
_logger = logging.getLogger("software_fj")  # Logger propio del proyecto (único para todo el sistema)


def _configurar_logger():  # Prepara el logger una sola vez
    """Crea la carpeta de logs y conecta el archivo, evitando líneas duplicadas."""
    if _logger.handlers:  # Si ya fue configurado antes...
        return  # ...no se vuelve a configurar (evita duplicar cada línea)
    os.makedirs(CARPETA_LOGS, exist_ok=True)  # Crea la carpeta logs/ si no existe
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Abre el archivo de logs
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")  # Fecha | Nivel | Mensaje
    manejador.setFormatter(formato)  # Aplica el formato al manejador
    _logger.addHandler(manejador)  # Conecta el manejador al logger
    _logger.setLevel(logging.INFO)  # Registra desde el nivel INFO hacia arriba
    _logger.propagate = False  # Evita que el mensaje se imprima también en consola


def registrar_evento(nivel, mensaje):  # Función pública acordada en el contrato
    """
    Registra un evento en logs/sistema.log.

    nivel: "INFO", "WARNING" o "ERROR". Si llega otro valor se usa "INFO".
    mensaje: texto (o cualquier objeto, como una excepción) que se desea registrar.
    Esta función nunca lanza excepciones: si el log falla, el sistema sigue funcionando.
    """
    try:  # Protege al sistema de cualquier falla del propio logger
        _configurar_logger()  # Se asegura de que el logger esté listo
        nivel_texto = str(nivel).upper()  # Normaliza el nivel a mayúsculas
        if nivel_texto not in NIVELES_VALIDOS:  # Si el nivel no es válido...
            nivel_texto = "INFO"  # ...se usa INFO por defecto, sin lanzar error
        getattr(_logger, nivel_texto.lower())(str(mensaje))  # Llama a _logger.info / .warning / .error
    except Exception as falla:  # Si ocurre cualquier problema al escribir el log
        print(f"[logger] No se pudo escribir en el log: {falla}", file=sys.stderr)  # Aviso en consola


if __name__ == "__main__":  # Pruebas rápidas: solo corren si se ejecuta este archivo directamente
    registrar_evento("INFO", "Sistema iniciado correctamente")  # Prueba 1: evento informativo
    registrar_evento("WARNING", "Servicio con poca disponibilidad")  # Prueba 2: advertencia
    registrar_evento("ERROR", "[ERR_DATOS_INVALIDOS] Correo inválido")  # Prueba 3: error
    registrar_evento("NIVEL_RARO", "Nivel inválido: se registra como INFO")  # Prueba 4: nivel inválido
    print(f"Pruebas OK -> revisa el archivo: {ARCHIVO_LOG}")  # Indica dónde quedó el log
