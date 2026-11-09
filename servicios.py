
"""
Archivo: servicios.py
Descripción: Define la clase abstracta Servicio y los servicios
especializados del sistema Software FJ.

"""

# Importamos las herramientas para crear clases abstractas
from abc import ABC, abstractmethod

# Importamos la clase abstracta Entidad
from entidades import Entidad

# Importamos las excepciones personalizadas
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError
)

# Importamos la función para registrar eventos
from logger import registrar_evento

# Se crea la clase abstracta Servicio que hereda de Entidad y ABC.
class Servicio(Entidad, ABC):

    def __init__(self, id_entidad, nombre, descripcion):
        # Inicializamos los datos heredados de Entidad.
        super().__init__(id_entidad)

        # Validamos que el nombre sea correcto
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError(
                "El nombre del servicio no puede estar vacío."
            )

        # Validamos que la descripción sea correcta
        if not isinstance(descripcion, str) or not descripcion.strip():
            raise DatosInvalidosError(
                "La descripción del servicio no puede estar vacía."
            )

        # Se guardan los datos como atributos privados
        self.__nombre = nombre.strip()
        self.__descripcion = descripcion.strip()
        self.__disponible = True
        
    # Cambia la disponibilidad del servicio
    def cambiar_disponibilidad(self, disponible):
        if not isinstance(disponible, bool):
            raise DatosInvalidosError(
                "La disponibilidad debe ser True o False."
            )

        self.__disponible = disponible

        registrar_evento(
            "INFO",
            f"Disponibilidad de {self.__nombre}: {disponible}"
        )

    @property
    def nombre(self):
        # Permite consultar el nombre del servicio
        return self.__nombre

    @property
    def descripcion(self):
        # Permite consultar la descripción del servicio
        return self.__descripcion

    @property
    def disponible(self):
        # Permite consultar si el servicio está disponible
        return self.__disponible

    # Cada servicio debe implementar su propio cálculo de costo
    @abstractmethod
    def calcular_costo(self, descuento=0, impuesto=0):
        pass

    # Cada servicio debe proporcionar su propia descripción
    @abstractmethod
    def describir_servicio(self):
        pass

    # Cada servicio debe validar sus propios parámetros
    @abstractmethod
    def validar_parametros(self):
        pass

# Se crea la clase ReservaSala que representa el servicio de reserva de salas
class ReservaSala(Servicio):

    # Constructor de la clase ReservaSala
    def __init__(self, id_entidad, nombre, descripcion, nombre_sala, horas):
        # Inicializamos los atributos de la clase padre
        super().__init__(id_entidad, nombre, descripcion)

        # Se valida que el nombre de la sala sea correcto
        if not isinstance(nombre_sala, str) or not nombre_sala.strip():
            raise DatosInvalidosError(
                "El nombre de la sala no puede estar vacío"
            )

        # Se valida que las horas sean un número positivo
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError(
                "La cantidad de horas debe ser mayor que cero"
            )

        # Se guardan los datos como atributos privados
        self.__nombre_sala = nombre_sala.strip()
        self.__horas = horas
        self.__valor_hora = 30000

        # Se registra la creación de la reserva de sala
        registrar_evento(
            "INFO",
            f"Reserva de sala creada: {self.__nombre_sala}"
        )


    # Calcula el costo total de la reserva
    def calcular_costo(self, descuento=0, impuesto=0):
        # Validamos el porcentaje de descuento
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or descuento < 0
            or descuento > 100
        ):
            error = DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )
            registrar_evento("ERROR", error)
            raise error

        # Validamos el porcentaje de impuesto
        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or impuesto < 0
            or impuesto > 100
        ):
            error = DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )
            registrar_evento("ERROR", error)
            raise error

        # Calculamos el costo inicial
        costo = self.__horas * self.__valor_hora

        # Comprobamos que el costo inicial sea válido
        if costo <= 0:
            error = CalculoInconsistenteError(
                "El costo de la reserva debe ser mayor que cero."
            )
            registrar_evento("ERROR", error)
            raise error

        # Aplicamos el descuento
        costo -= costo * (descuento / 100)

        # Aplicamos el impuesto al costo con descuento
        costo += costo * (impuesto / 100)

        return round(costo, 2)

    # Muestra la información del servicio
    def describir_servicio(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Sala: {self.__nombre_sala}\n"
            f"Horas reservadas: {self.__horas}\n"
            f"Valor por hora: ${self.__valor_hora:,.0f}"
        )
    
    # Describe la entidad y el servicio
    def describir(self):
        return self.describir_servicio()
    
    # Valida los parámetros de la reserva
    def validar_parametros(self):
        if not self.disponible:
            error = ServicioNoDisponibleError(
                "La sala no se encuentra disponible."
            )
            registrar_evento("ERROR", error)
            raise error

        # Se validan que las horas sean un número positivo
        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            error = DatosInvalidosError(
                "Las horas de reserva deben ser mayores que cero."
            )
            registrar_evento("ERROR", error)
            raise error

        return True
    
# Se crea la clase AlquilerEquipo que representa el servicio de alquiler de equipos
class AlquilerEquipo(Servicio):

    # Constructor de la clase AlquilerEquipo
    def __init__(self, id_entidad, nombre, descripcion, nombre_equipo, dias):
        # Inicializamos los atributos de la clase padre.
        super().__init__(id_entidad, nombre, descripcion)

        # Se validan que el nombre del equipo sea correcto
        if not isinstance(nombre_equipo, str) or not nombre_equipo.strip():
            raise DatosInvalidosError(
                "El nombre del equipo no puede estar vacío."
            )

        # Se validan que los días sean un número positivo
        if isinstance(dias, bool) or not isinstance(dias, (int, float)) or dias <= 0:
            raise DatosInvalidosError(
                "La cantidad de días debe ser mayor que cero."
            )

        # Guardamos los datos como atributos privados
        self.__nombre_equipo = nombre_equipo.strip()
        self.__dias = dias
        self.__valor_dia = 50000

        # Se registra la creación del alquiler
        registrar_evento(
            "INFO",
            f"Alquiler de equipo creado: {self.__nombre_equipo}"
        )

    # Calcula el costo total del alquiler
    def calcular_costo(self, descuento=0, impuesto=0):
        # Validamos el porcentaje de descuento
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or descuento < 0
            or descuento > 100
        ):
            error = DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )
            registrar_evento("ERROR", error)
            raise error

        # Validamos el porcentaje de impuesto
        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or impuesto < 0
            or impuesto > 100
        ):
            error = DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )
            registrar_evento("ERROR", error)
            raise error

        # Calculamos el costo inicial
        costo = self.__dias * self.__valor_dia

        # Comprobamos que el costo inicial sea válido
        if costo <= 0:
            error = CalculoInconsistenteError(
                "El costo del alquiler debe ser mayor que cero."
            )
            registrar_evento("ERROR", error)
            raise error

        # Aplicamos el descuento
        costo -= costo * (descuento / 100)

        # Aplicamos el impuesto al costo con descuento
        costo += costo * (impuesto / 100)

        return round(costo, 2)

    # Muestra la información del servicio
    def describir_servicio(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Equipo: {self.__nombre_equipo}\n"
            f"Días de alquiler: {self.__dias}\n"
            f"Valor por día: ${self.__valor_dia:,.0f}"
        )

    # Describe la entidad y su servicio
    def describir(self):
        return self.describir_servicio()

    # Se validan los parámetros del alquiler
    def validar_parametros(self):
        if not self.disponible:
            error = ServicioNoDisponibleError(
                "El equipo no se encuentra disponible."
            )
            registrar_evento("ERROR", error)
            raise error

        # Validamos que los días sean un número positivo
        if (
            isinstance(self.__dias, bool)
            or not isinstance(self.__dias, (int, float))
            or self.__dias <= 0
        ):
            error = DatosInvalidosError(
                "Los días de alquiler deben ser mayores que cero."
            )
            registrar_evento("ERROR", error)
            raise error

        return True

# Se crea la clase Asesoria que representa el servicio de asesorías especializadas.
class Asesoria(Servicio):

    # Constructor de la clase Asesoria
    def __init__(self, id_entidad, nombre, descripcion, especialidad, horas):
        # Inicializamos los atributos de la clase padre.
        super().__init__(id_entidad, nombre, descripcion)

        # Se valida que la especialidad sea correcta
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError(
                "La especialidad de la asesoría no puede estar vacía."
            )

        # Se valida que las horas sean un número positivo
        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError(
                "La cantidad de horas debe ser mayor que cero."
            )

        # Guardamos los datos como atributos privados
        self.__especialidad = especialidad.strip()
        self.__horas = horas
        self.__valor_hora = 60000

        # Registramos la creación de la asesoría
        registrar_evento(
            "INFO",
            f"Asesoría creada: {self.__especialidad}"
        )

    # Calcula el costo total de la asesoría
    def calcular_costo(self, descuento=0, impuesto=0):
        # Validamos el porcentaje de descuento
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or descuento < 0
            or descuento > 100
        ):
            error = DatosInvalidosError(
                "El descuento debe estar entre 0 y 100."
            )
            registrar_evento("ERROR", error)
            raise error

        # Validamos el porcentaje de impuesto
        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or impuesto < 0
            or impuesto > 100
        ):
            error = DatosInvalidosError(
                "El impuesto debe estar entre 0 y 100."
            )
            registrar_evento("ERROR", error)
            raise error

        # Calculamos el costo inicial
        costo = self.__horas * self.__valor_hora

        # Se comprueba que el costo inicial sea válido
        if costo <= 0:
            error = CalculoInconsistenteError(
                "El costo de la asesoría debe ser mayor que cero."
            )
            registrar_evento("ERROR", error)
            raise error

        # Aplicamos el descuento
        costo -= costo * (descuento / 100)

        # Aplicamos el impuesto al costo con descuento
        costo += costo * (impuesto / 100)

        return round(costo, 2)

    # Muestra la información del servicio
    def describir_servicio(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Especialidad: {self.__especialidad}\n"
            f"Horas de asesoría: {self.__horas}\n"
            f"Valor por hora: ${self.__valor_hora:,.0f}"
        )

    # Describe la entidad y su servicio
    def describir(self):
        return self.describir_servicio()

    # Se validan los parámetros de la asesoría
    def validar_parametros(self):
        if not self.disponible:
            error = ServicioNoDisponibleError(
                "La asesoría no se encuentra disponible."
            )
            registrar_evento("ERROR", error)
            raise error

        # Se valida que las horas sean un número positivo
        if (
            isinstance(self.__horas, bool)
            or not isinstance(self.__horas, (int, float))
            or self.__horas <= 0
        ):
            error = DatosInvalidosError(
                "Las horas de asesoría deben ser mayores que cero."
            )
            registrar_evento("ERROR", error)
            
            raise error

        return True