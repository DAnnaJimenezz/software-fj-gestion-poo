"""Archivo: entidades.py
Descripción: Define la clase abstracta Entidad, que funciona como una estructura
base para las clases del sistema Software FJ.
Las clases que hereden de Entidad deberán implementar el método
describir(), con el fin de proporcionar una representación propia
de cada tipo de entidad."""

# Importamos las herramientas para crear una clase abstracta.
from abc import ABC, abstractmethod

# Importamos la excepción personalizada del sistema.
from excepciones import DatosInvalidosError

class Entidad(ABC):
    """Clase base para las entidades del sistema Software."""

    def __init__(self, id_entidad):
        # Validamos que el identificador no sea nulo.
        if id_entidad is None:
            raise DatosInvalidosError(
                "El identificador no puede ser None."
            )

        # Convertimos el identificador a texto y quitamos espacios.
        identificador = str(id_entidad).strip()

        # Evitamos que el identificador quede vacío.
        if not identificador:
            raise DatosInvalidosError(
                "El identificador no puede estar vacío."
            )

        # Guardamos el identificador como atributo privado.
        self.__id_entidad = identificador

    @property
    def id_entidad(self):
        # Permitimos consultar el identificador de forma controlada.
        return self.__id_entidad

    @abstractmethod
    def describir(self):
        # Las clases hijas deben implementar este método.
        pass
