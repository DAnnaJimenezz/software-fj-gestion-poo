""" Archivo: simulacion.py
Proyecto: Sistema Integral de Gestion - Software FJ

Descripcion:
Ejecuta diez operaciones de ejemplo sobre las clases del proyecto.
Incluye escenarios correctos y escenarios que deben generar excepciones.

Ejecucion:
    python simulacion.py

Nota:
Este modulo utiliza las clases y excepciones definidas en los demas
archivos del proyecto Software FJ para ejecutar y demostrar diez
escenarios de funcionamiento del sistema."""

from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from reservas import Reserva
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


def ejecutar_operacion(numero, descripcion, funcion):
    """Ejecuta una operacion, muestra su resultado y controla errores."""
    print(f"\n{numero}. {descripcion}")
    print("-" * 60)

    try:
        resultado = funcion()
        if resultado is not None:
            print(resultado)
        print("Resultado: operacion ejecutada correctamente.")
    except (DatosInvalidosError, ServicioNoDisponibleError) as error:
        print(f"Resultado esperado: se controlo la excepcion: {error}")
    except Exception as error:
        print(f"Error no previsto: {type(error).__name__}: {error}")


def simulacion():
    """Realiza diez operaciones de simulacion del sistema Software FJ."""

    print("=" * 60)
    print("SIMULACION DE 10 OPERACIONES - SOFTWARE FJ")
    print("=" * 60)

    datos = {}

    # Operacion 1: registrar un cliente valido.
    def op1():
        datos["cliente"] = Cliente(
            "C100", "Laura Gomez", "laura@gmail.com", "3001234567"
        )
        return datos["cliente"].describir()

    ejecutar_operacion(1, "Registro de un cliente valido", op1)

    # Operacion 2: intentar registrar un cliente con correo invalido.
    def op2():
        try:
            Cliente("C101", "Carlos Perez", "correo_invalido", "3101234567")
        except DatosInvalidosError as error:
            print(f"Validacion correcta: {error}")
            return "El sistema rechazo los datos incorrectos."
        raise AssertionError("Se esperaba una excepcion por correo invalido.")

    ejecutar_operacion(2, "Validacion de un correo electronico incorrecto", op2)

    # Operación 3: crear un servicio de reserva de sala.
    def op3():
        datos["sala"] = ReservaSala(
            "S100", "Sala principal", "Sala para reuniones", "Sala A", 3
        )
        return datos["sala"].describir_servicio()

    ejecutar_operacion(3, "Creación de un servicio de reserva de sala", op3)

    # Operación 4: crear un servicio de alquiler de equipo.
    def op4():
        datos["equipo"] = AlquilerEquipo(
            "S101", "Alquiler de portatil", "Equipo para trabajo",
            "Portatil", 2
        )
        return datos["equipo"].describir_servicio()

    ejecutar_operacion(4, "Creacion de un servicio de alquiler de equipo", op4)

    # Operacion 5: crear un servicio de asesoria especializada.
    def op5():
        datos["asesoria"] = Asesoria(
            "S102", "Asesoria tecnologica", "Orientacion especializada",
            "Desarrollo de software", 2
        )
        return datos["asesoria"].describir_servicio()

    ejecutar_operacion(5, "Creacion de un servicio de asesoria", op5)

    # Operacion 6: crear una reserva valida para el cliente.
    def op6():
        datos["reserva"] = Reserva(
            "R100", datos["cliente"], datos["sala"]
        )
        return (
            f"Reserva: {datos['reserva'].id_reserva}\n"
            f"Cliente: {datos['reserva'].cliente.nombre}\n"
            f"Estado inicial: {datos['reserva'].estado}"
        )

    ejecutar_operacion(6, "Creacion de una reserva valida", op6)

    # Operacion 7: calcular el costo aplicando descuento e impuesto.
    def op7():
        costo = datos["reserva"].calcular_costo(descuento=10, impuesto=19)
        return f"Costo de la reserva con descuento e impuesto: ${costo:,.0f}"

    ejecutar_operacion(7, "Calculo del costo de la reserva", op7)

    # Operacion 8: confirmar la reserva.
    def op8():
        estado = datos["reserva"].confirmar()
        return f"Estado actual de la reserva: {estado}"

    ejecutar_operacion(8, "Confirmacion de la reserva", op8)

    # Operacion 9: procesar la reserva confirmada.
    def op9():
        estado = datos["reserva"].procesar()
        return f"Estado final de la reserva: {estado}"

    ejecutar_operacion(9, "Procesamiento de la reserva confirmada", op9)

    # Operacion 10: intentar reservar un servicio no disponible.
    def op10():
        servicio_no_disponible = ReservaSala(
            "S103", "Sala ocupada", "Sala temporalmente no disponible",
            "Sala B", 2
        )
        servicio_no_disponible.cambiar_disponibilidad(False)

        try:
            Reserva("R101", datos["cliente"], servicio_no_disponible)
        except ServicioNoDisponibleError as error:
            print(f"Validacion correcta: {error}")
            return "El sistema impidio reservar un servicio no disponible."

        raise AssertionError(
            "Se esperaba una excepcion por servicio no disponible."
        )

    ejecutar_operacion(10, "Intento de reserva de un servicio no disponible", op10)

    print("\n" + "=" * 60)
    print("SIMULACION FINALIZADA")
    print("Se ejecutaron los diez escenarios definidos.")
    print("Los eventos y errores tambien se registran mediante logger.py.")
    print("=" * 60)


if __name__ == "__main__":
    simulacion()
