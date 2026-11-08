import re  # Modulo para validar formatos de texto
from entidades import Entidad  # Clase abstracta base
from excepciones import DatosInvalidosError  # Excepcion para datos invalidos
from logger import registrar_evento  # Funcion para registrar eventos

class Cliente(Entidad):
    """Representa un cliente dentro del sistema Software."""

    def __init__(self, id_cliente, nombre, correo, telefono):
        # Inicializamos el identificador heredado de Entidad.
        super().__init__(id_cliente)

        # Definimos los atributos privados del cliente.
        self.__nombre = None
        self.__correo = None
        self.__telefono = None

        # Asignamos los datos utilizando sus propiedades.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

        # Registramos la creacion exitosa del cliente.
        registrar_evento(
            "INFO",
            f"Cliente creado correctamente: {self.id_cliente}")

    @property
    def id_cliente(self):
        # Retornamos el identificador heredado de Entidad.
        return self.id_entidad

    @property
    def nombre(self):
        # Permitimos consultar el nombre del cliente.
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Validamos que el nombre sea texto y no este vacio.
        if not isinstance(valor, str) or not valor.strip():
            error = DatosInvalidosError(
                "El nombre del cliente no puede estar vacio.")
            registrar_evento("ERROR", str(error))
            raise error

        # Guardamos el nombre sin espacios innecesarios.
        self.__nombre = valor.strip()

    @property
    def correo(self):
        # Permitimos consultar el correo del cliente.
        return self.__correo

    @correo.setter
    def correo(self, valor):
        # Validamos que el correo sea texto y no este vacio.
        if not isinstance(valor, str) or not valor.strip():
            error = DatosInvalidosError(
                "El correo electronico no puede estar vacio.")
            registrar_evento("ERROR", str(error))
            raise error

        # Eliminamos los espacios al inicio y al final.
        correo_limpio = valor.strip()

        # Definimos un patrón básico para validar el correo.
        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        # Verificamos que el correo tenga un formato valido.
        if not re.match(patron, correo_limpio):
            error = DatosInvalidosError(
                "El correo electronico ingresado no es valido.")
            registrar_evento("ERROR", str(error))
            raise error

        # Guardamos el correo validado.
        self.__correo = correo_limpio

    @property
    def telefono(self):
        # Permitimos consultar el telefono del cliente.
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        # Validamos que el telefono sea texto y no este vacio.
        if not isinstance(valor, str) or not valor.strip():
            error = DatosInvalidosError(
                "El telefono del cliente no puede estar vacio.")
            registrar_evento("ERROR", str(error))
            raise error

        # Eliminamos los espacios al inicio y al final.
        telefono_limpio = valor.strip()

        # Permitimos números y formatos telefonicos comunes.
        patron = r"^\+?[0-9\s()-]+$"

        # Verificamos que no existan caracteres no permitidos.
        if not re.match(patron, telefono_limpio):
            error = DatosInvalidosError(
                "El telefono contiene caracteres no permitidos.")
            registrar_evento("ERROR", str(error))
            raise error

        # Contamos unicamente los digitos del telefono.
        cantidad_digitos = sum(
            caracter.isdigit()
            for caracter in telefono_limpio)

        # Validamos que tenga entre 7 y 15 digitos.
        if cantidad_digitos < 7 or cantidad_digitos > 15:
            error = DatosInvalidosError(
                "El teléfono debe contener entre 7 y 15 digitos.")
            registrar_evento("ERROR", str(error))
            raise error

        # Guardamos el telefono validado.
        self.__telefono = telefono_limpio

    def describir(self):
        # Retornamos una descripcion completa del cliente.
        return (
            f"Cliente: {self.nombre} | "
            f"ID: {self.id_cliente} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}")

    def __str__(self):
        # Definimos como se representa el cliente como texto.
        return self.describir()
