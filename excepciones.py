"""
excepciones.py
Excepciones personalizadas del sistema Software FJ.

Todas heredan de ErrorSoftwareFJ, de modo que cualquier error propio del
sistema puede capturarse con un solo bloque ``except ErrorSoftwareFJ``.
Cada excepción tiene un código que se usa al registrar el error en el log.
"""


class ErrorSoftwareFJ(Exception):  # Excepción base de todo el sistema
    """Excepción base de la que heredan todas las demás del proyecto."""

    codigo = "ERR_GENERAL"  # Código de error por defecto (se sobrescribe en las hijas)

    def __init__(self, mensaje="Error en el sistema Software FJ"):  # Recibe el mensaje descriptivo
        super().__init__(mensaje)  # Llama al constructor de Exception con el mensaje
        self.mensaje = mensaje  # Guarda el mensaje como atributo para usarlo después

    def __str__(self):  # Define cómo se muestra el error al imprimirlo
        return f"[{self.codigo}] {self.mensaje}"  # Formato uniforme: [CODIGO] mensaje


class DatosInvalidosError(ErrorSoftwareFJ):  # Error de validación de datos
    """Se lanza cuando un dato de entrada es inválido o falta (nombre, correo, etc.)."""

    codigo = "ERR_DATOS_INVALIDOS"  # Código propio de los errores de validación


class ServicioNoDisponibleError(ErrorSoftwareFJ):  # Error de disponibilidad
    """Se lanza cuando se intenta usar o reservar un servicio no disponible."""

    codigo = "ERR_SERVICIO_NO_DISPONIBLE"  # Código propio de servicios no disponibles


class ReservaInvalidaError(ErrorSoftwareFJ):  # Error en el proceso de reserva
    """Se lanza ante un intento de reserva incorrecto (duración, datos faltantes, etc.)."""

    codigo = "ERR_RESERVA_INVALIDA"  # Código propio de reservas inválidas


class OperacionNoPermitidaError(ErrorSoftwareFJ):  # Error por estado incorrecto
    """Se lanza cuando una operación no está permitida en el estado actual."""

    codigo = "ERR_OPERACION_NO_PERMITIDA"  # Código propio de operaciones no permitidas


class CalculoInconsistenteError(ErrorSoftwareFJ):  # Error en cálculos de costos
    """Se lanza cuando un cálculo da un resultado incoherente (por ejemplo, costo negativo)."""

    codigo = "ERR_CALCULO_INCONSISTENTE"  # Código propio de cálculos inconsistentes


if __name__ == "__main__":  # Pruebas rápidas: solo corren si se ejecuta este archivo directamente
    # Prueba 1: lanzar una excepción propia y capturarla con la clase base
    try:  # Bloque donde se produce el error
        raise DatosInvalidosError("El correo no tiene formato válido")  # Se lanza el error
    except ErrorSoftwareFJ as error:  # Se captura con la excepción base
        print("Prueba 1 OK ->", error)  # Muestra: [ERR_DATOS_INVALIDOS] mensaje

    # Prueba 2: verificar que las demás excepciones heredan de la base
    for clase in (ServicioNoDisponibleError, ReservaInvalidaError,
                  OperacionNoPermitidaError, CalculoInconsistenteError):  # Recorre las demás clases
        assert issubclass(clase, ErrorSoftwareFJ)  # Comprueba la herencia
    print("Prueba 2 OK -> todas heredan de ErrorSoftwareFJ")  # Confirma la herencia

    # Prueba 3: encadenamiento de excepciones (raise ... from ...)
    try:  # Bloque externo
        try:  # Bloque interno que produce un error del sistema
            int("abc")  # Provoca un ValueError
        except ValueError as causa:  # Se captura el error original
            raise DatosInvalidosError("La edad debe ser numérica") from causa  # Se encadena
    except ErrorSoftwareFJ as error:  # Se captura el error propio
        print("Prueba 3 OK ->", error, "| causa:", repr(error.__cause__))  # Muestra la causa
