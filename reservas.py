"""
Archivo: reservas.py

Descripción:
Define la clase Reserva, encargada de gestionar las reservas
de clientes para los diferentes servicios de Software FJ.

Incluye validaciones, control de estados, cálculo de costos
y manejo de excepciones personalizadas.
"""

# Importamos la clase Cliente.
from clientes import Cliente

# Importamos la clase abstracta Servicio.
from servicios import Servicio

# Importamos las excepciones personalizadas.
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError
)

# Importamos la función para registrar eventos.
from logger import registrar_evento
import math

class Reserva:
    """
    Representa una reserva realizada por un cliente
    para utilizar uno de los servicios de Software FJ.
    """

    # Estados permitidos para una reserva.
    ESTADOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    # Constructor de la clase Reserva.
    def __init__(self, id_reserva, cliente, servicio):

        try:
            # Validar que el identificador sea un texto no vacío.
            if not isinstance(id_reserva, str) or not id_reserva.strip():
                raise DatosInvalidosError(
                    "El identificador de la reserva es obligatorio."
                )

            # Validar que el cliente sea un objeto de tipo Cliente.
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError(
                    "La reserva debe estar asociada a un cliente válido."
                )

            # Validar que el servicio sea un objeto de tipo Servicio.
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError(
                    "La reserva debe estar asociada a un servicio válido."
                )
                
            # Validar los parámetros y la disponibilidad del servicio.
            servicio.validar_parametros()
            
            # Obtener la duración y su unidad desde el servicio.
            duracion = servicio.duracion
            unidad = servicio.unidad_duracion

            # Validar que la duración sea un número positivo.
            if (
                isinstance(duracion, bool)
                or not isinstance(duracion, (int, float))
                or not math.isfinite(duracion)
                or duracion <= 0
            ):
    
                raise DatosInvalidosError(
                    "La duración del servicio debe ser un número positivo."
                )

            # Validar que la unidad de duración sea correcta.
            if unidad not in ("horas", "días"):
                raise DatosInvalidosError(
                    "La unidad de duración del servicio no es válida."
                )

            # Encapsular los atributos de la reserva.
            self.__id_reserva = id_reserva.strip()
            self.__cliente = cliente
            self.__servicio = servicio
            self.__duracion = duracion
            self.__unidad_duracion = unidad
            self.__estado = "PENDIENTE"

            # Registrar la creación de la reserva.
            registrar_evento(
                "INFO",
                f"Reserva {self.__id_reserva} creada correctamente."
            )

        except DatosInvalidosError as error:
            registrar_evento(
                "ERROR",
                f"Error al crear la reserva: {error}"
            )
            raise
        except ServicioNoDisponibleError as error:
            registrar_evento(
                "ERROR",
                f"No se pudo crear la reserva: {error}"
            )
            raise
        except Exception as error:
            registrar_evento(
                "ERROR",
                f"Error inesperado al crear la reserva: {error}"
            )
            raise ReservaInvalidaError(
                "No fue posible crear la reserva."
            ) from error

    # Propiedad para consultar el identificador de la reserva.
    @property
    def id_reserva(self):
        return self.__id_reserva

    # Propiedad para consultar el cliente asociado.
    @property
    def cliente(self):
        return self.__cliente

    # Propiedad para consultar el servicio reservado.
    @property
    def servicio(self):
        return self.__servicio

    # Propiedad para consultar la duración.
    @property
    def duracion(self):
        return self.__duracion

    # Propiedad para consultar la unidad de duración.
    @property
    def unidad_duracion(self):
        return self.__unidad_duracion

    # Propiedad para consultar el estado actual.
    @property
    def estado(self):
        return self.__estado


    # Método para confirmar una reserva.
    def confirmar(self):

        try:
            # Verificar que la reserva esté pendiente.
            if self.__estado != "PENDIENTE":
                raise OperacionNoPermitidaError(
                    f"No se puede confirmar una reserva con estado {self.__estado}."
                )

            # Cambiar el estado de la reserva.
            self.__estado = "CONFIRMADA"

            # Registrar la confirmación.
            registrar_evento(
                "INFO",
                f"Reserva {self.__id_reserva} confirmada correctamente."
            )

        except OperacionNoPermitidaError as error:
            registrar_evento(
                "ERROR",
                f"Error al confirmar la reserva: {error}"
            )
            raise

        return self.__estado

    # Método para cancelar una reserva.
    def cancelar(self):

        try:
            # Verificar que la reserva pueda ser cancelada.
            if self.__estado not in ("PENDIENTE", "CONFIRMADA"):
                raise OperacionNoPermitidaError(
                    f"No se puede cancelar una reserva con estado {self.__estado}."
                )

            # Cambiar el estado de la reserva.
            self.__estado = "CANCELADA"

            # Registrar la cancelación.
            registrar_evento(
                "INFO",
                f"Reserva {self.__id_reserva} cancelada correctamente."
            )

        except OperacionNoPermitidaError as error:
            registrar_evento(
                "ERROR",
                f"Error al cancelar la reserva: {error}"
            )
            raise

        return self.__estado


    # Método para procesar una reserva.
    def procesar(self):

        try:
            # Verificar que la reserva esté confirmada.
            if self.__estado != "CONFIRMADA":
                raise OperacionNoPermitidaError(
                    f"No se puede procesar una reserva con estado {self.__estado}."
                )

            # Cambiar el estado de la reserva.
            self.__estado = "PROCESADA"

            # Registrar el procesamiento.
            registrar_evento(
                "INFO",
                f"Reserva {self.__id_reserva} procesada correctamente."
            )

        except OperacionNoPermitidaError as error:
            registrar_evento(
                "ERROR",
                f"Error al procesar la reserva: {error}"
            )
            raise

        return self.__estado

    # Método para calcular el costo de la reserva.
    def calcular_costo(self, descuento=0, impuesto=0):

        try:
            # Validar que el descuento y el impuesto sean numéricos.
            if (
                isinstance(descuento, bool)
                or not isinstance(descuento, (int, float))
                or not math.isfinite(descuento)
                or descuento < 0
                or descuento > 100
            ):
                raise DatosInvalidosError(
                    "El descuento debe ser un porcentaje entre 0 y 100."
                )

            if (
                isinstance(impuesto, bool)
                or not isinstance(impuesto, (int, float))
                or not math.isfinite(impuesto)
                or impuesto < 0
                or impuesto > 100
            ): 
                raise DatosInvalidosError(
                    "El impuesto debe ser un porcentaje entre 0 y 100."
                )

            # Obtener el costo calculado por el servicio.
            costo = self.__servicio.calcular_costo(
                descuento=descuento,
                impuesto=impuesto
            )

            # Verificar que el resultado sea válido.
            if (
                isinstance(costo, bool)
                or not isinstance(costo, (int, float))
                or not math.isfinite(costo)
                or costo < 0
            ):
                raise CalculoInconsistenteError(
                    "El servicio generó un costo inválido."
                )

            # Registrar el cálculo realizado.
            registrar_evento(
                "INFO",
                f"Costo de la reserva {self.__id_reserva} calculado: {costo}."
            )

            return costo

        except (DatosInvalidosError, CalculoInconsistenteError) as error:
            registrar_evento(
                "ERROR",
                f"Error al calcular el costo de la reserva: {error}"
            )
            raise
            
        except Exception as error:
            registrar_evento(
                "ERROR",
                f"Error inesperado al calcular el costo: {error}"
            )
            raise CalculoInconsistenteError(
                "No fue posible calcular el costo de la reserva."
            ) from error

    # Método para mostrar la información completa de la reserva.
    def mostrar_informacion(self):

        try:
            # Obtener la descripción del servicio.
            descripcion = self.__servicio.describir_servicio()

            # Calcular el costo de la reserva.
            costo = self.calcular_costo()

            # Construir la información de la reserva.
            informacion = (
                f"\n--- INFORMACIÓN DE LA RESERVA ---\n"
                f"Identificador: {self.__id_reserva}\n"
                f"Cliente: {self.__cliente.nombre}\n"
                f"Correo: {self.__cliente.correo}\n"
                f"Servicio: {descripcion}\n"
                f"Duración: {self.__duracion} {self.__unidad_duracion}\n"
                f"Estado: {self.__estado}\n"
                f"Costo: ${costo:,.2f}\n"
            )

            # Registrar la consulta de información.
            registrar_evento(
                "INFO",
                f"Información de la reserva {self.__id_reserva} consultada."
            )

            return informacion

        except Exception as error:
            registrar_evento(
                "ERROR",
                f"Error al mostrar la reserva: {error}"
            )
            raise ReservaInvalidaError(
                "No fue posible mostrar la información de la reserva."
            ) from error
