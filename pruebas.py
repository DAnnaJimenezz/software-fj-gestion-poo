"""
pruebas.py
Pruebas generales del sistema Software FJ (excepciones, logger, Cliente,
Servicios, Reserva y estabilidad del conjunto).

Cómo ejecutarlo (desde la carpeta del repositorio):
    python3 -m unittest pruebas.py -v
Requiere que clientes.py, servicios.py, reservas.py, excepciones.py,
logger.py y entidades.py estén en la misma carpeta.
"""

import os  # Módulo estándar para revisar si existe el archivo de logs
import unittest  # Módulo estándar de pruebas unitarias

from excepciones import (  # Importa todas las excepciones personalizadas
    ErrorSoftwareFJ, DatosInvalidosError, ServicioNoDisponibleError,
    ReservaInvalidaError, OperacionNoPermitidaError, CalculoInconsistenteError,
)
from logger import registrar_evento, ARCHIVO_LOG  # Función de registro y ruta del log
from clientes import Cliente  # Clase Cliente
from servicios import Servicio, ReservaSala, AlquilerEquipo, Asesoria  # Servicios
from reservas import Reserva  # Clase Reserva


def leer_log():  # Función auxiliar: devuelve el contenido actual del log
    """Lee el archivo de logs; si no existe devuelve texto vacío."""
    if not os.path.exists(ARCHIVO_LOG):  # Si el archivo todavía no existe...
        return ""  # ...se devuelve un texto vacío
    with open(ARCHIVO_LOG, encoding="utf-8") as archivo:  # Abre el log para lectura
        return archivo.read()  # Devuelve todo el contenido


def cliente_valido():  # Función auxiliar: crea un cliente correcto
    return Cliente("C1", "Ana Pérez", "ana@correo.com", "3001234567")  # Cliente válido


def servicios_validos():  # Función auxiliar: crea uno de cada servicio
    sala = ReservaSala("S1", "Sala A", "Sala de reuniones", "Sala A", 3)  # 3 horas de sala
    equipo = AlquilerEquipo("S2", "Portátil", "Alquiler de portátil", "Portátil", 2)  # 2 días
    asesoria = Asesoria("S3", "Asesoría TI", "Asesoría en redes", "Redes", 2)  # 2 horas
    return sala, equipo, asesoria  # Devuelve los tres servicios


class PruebasExcepciones(unittest.TestCase):  # Pruebas del módulo excepciones.py
    def test_todas_heredan_de_la_base(self):  # Verifica la herencia
        for clase in (DatosInvalidosError, ServicioNoDisponibleError, ReservaInvalidaError,
                      OperacionNoPermitidaError, CalculoInconsistenteError):  # Cada excepción
            self.assertTrue(issubclass(clase, ErrorSoftwareFJ))  # Debe heredar de la base

    def test_mensaje_incluye_codigo(self):  # Verifica el formato del mensaje
        error = DatosInvalidosError("dato malo")  # Crea una excepción
        self.assertIn("ERR_DATOS_INVALIDOS", str(error))  # El texto trae el código
        self.assertIn("dato malo", str(error))  # El texto trae el mensaje

    def test_encadenamiento(self):  # Verifica raise ... from ...
        try:  # Bloque externo
            try:  # Bloque interno
                int("abc")  # Provoca ValueError
            except ValueError as causa:  # Captura el error original
                raise DatosInvalidosError("no numérico") from causa  # Lo encadena
        except ErrorSoftwareFJ as error:  # Captura el error propio
            self.assertIsInstance(error.__cause__, ValueError)  # Conserva la causa original


class PruebasLogger(unittest.TestCase):  # Pruebas del módulo logger.py
    def test_escribe_en_el_log(self):  # Verifica que se escriba el evento
        registrar_evento("INFO", "prueba-logger-unica-123")  # Registra un evento
        self.assertIn("prueba-logger-unica-123", leer_log())  # Debe aparecer en el log

    def test_nivel_invalido_no_lanza_error(self):  # El logger nunca debe romper el sistema
        registrar_evento("NIVEL_RARO", "nivel raro de prueba")  # Nivel inválido
        self.assertIn("nivel raro de prueba", leer_log())  # Se registra igual como INFO


class PruebasCliente(unittest.TestCase):  # Pruebas de clientes.py
    def test_cliente_valido(self):  # Caso correcto
        cliente = cliente_valido()  # Crea el cliente
        self.assertEqual(cliente.nombre, "Ana Pérez")  # El nombre se guarda bien
        self.assertIn("ana@correo.com", cliente.describir())  # describir() muestra el correo

    def test_nombre_vacio(self):  # Nombre inválido
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Cliente("C2", "   ", "a@b.com", "3001234567")  # Nombre en blanco

    def test_correo_invalido(self):  # Correo sin formato válido
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Cliente("C3", "Luis", "luis.correo", "3001234567")  # Correo sin @

    def test_telefono_con_letras(self):  # Teléfono inválido
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Cliente("C4", "Luis", "l@m.com", "abc123")  # Teléfono con letras

    def test_telefono_muy_corto(self):  # Teléfono con pocos dígitos
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Cliente("C5", "Luis", "l@m.com", "12345")  # Solo 5 dígitos

    def test_id_vacio(self):  # Identificador inválido
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Cliente("", "Luis", "l@m.com", "3001234567")  # ID vacío


class PruebasServicios(unittest.TestCase):  # Pruebas de servicios.py
    def test_servicio_es_abstracto(self):  # No se puede instanciar la clase abstracta
        with self.assertRaises(TypeError):  # Python lanza TypeError
            Servicio("X", "n", "d")  # Intento de instanciar una abstracta

    def test_costo_de_los_tres_servicios(self):  # Todos calculan un costo positivo
        for servicio in servicios_validos():  # Recorre los tres servicios (polimorfismo)
            self.assertGreater(servicio.calcular_costo(), 0)  # El costo es mayor que cero

    def test_descuento_reduce_e_impuesto_aumenta(self):  # Sobrecarga con parámetros opcionales
        for servicio in servicios_validos():  # Recorre los tres servicios
            base = servicio.calcular_costo()  # Costo sin descuento ni impuesto
            self.assertLess(servicio.calcular_costo(descuento=10), base)  # Con descuento baja
            self.assertGreater(servicio.calcular_costo(impuesto=19), base)  # Con impuesto sube

    def test_descuento_fuera_de_rango(self):  # Parámetros inválidos
        sala = servicios_validos()[0]  # Toma la sala
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            sala.calcular_costo(descuento=150)  # Descuento mayor a 100

    def test_impuesto_negativo(self):  # Parámetros inválidos
        sala = servicios_validos()[0]  # Toma la sala
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            sala.calcular_costo(impuesto=-5)  # Impuesto negativo

    def test_horas_negativas(self):  # Creación incorrecta de un servicio
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            ReservaSala("S9", "Sala", "desc", "Sala", -1)  # Horas negativas

    def test_describir_devuelve_texto(self):  # Método sobrescrito en cada hija
        for servicio in servicios_validos():  # Recorre los tres servicios
            self.assertIsInstance(servicio.describir_servicio(), str)  # Devuelve texto

    def test_disponibilidad_debe_ser_booleana(self):  # Validación del cambio de estado
        sala = servicios_validos()[0]  # Toma la sala
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            sala.cambiar_disponibilidad("si")  # Valor que no es bool


class PruebasReserva(unittest.TestCase):  # Pruebas de reservas.py
    def test_flujo_completo(self):  # Pendiente -> Confirmada -> Procesada
        reserva = Reserva("R1", cliente_valido(), servicios_validos()[0])  # Crea la reserva
        self.assertEqual(reserva.estado, "PENDIENTE")  # Estado inicial
        self.assertEqual(reserva.confirmar(), "CONFIRMADA")  # Se confirma
        self.assertEqual(reserva.procesar(), "PROCESADA")  # Se procesa

    def test_cancelar_pendiente(self):  # Cancelación permitida
        reserva = Reserva("R2", cliente_valido(), servicios_validos()[1])  # Crea la reserva
        self.assertEqual(reserva.cancelar(), "CANCELADA")  # Se cancela

    def test_confirmar_dos_veces(self):  # Operación no permitida
        reserva = Reserva("R3", cliente_valido(), servicios_validos()[0])  # Crea la reserva
        reserva.confirmar()  # Primera confirmación (válida)
        with self.assertRaises(OperacionNoPermitidaError):  # La segunda debe fallar
            reserva.confirmar()  # Segunda confirmación

    def test_cancelar_dos_veces(self):  # Operación no permitida
        reserva = Reserva("R4", cliente_valido(), servicios_validos()[0])  # Crea la reserva
        reserva.cancelar()  # Primera cancelación (válida)
        with self.assertRaises(OperacionNoPermitidaError):  # La segunda debe fallar
            reserva.cancelar()  # Segunda cancelación

    def test_procesar_sin_confirmar(self):  # Operación no permitida
        reserva = Reserva("R5", cliente_valido(), servicios_validos()[0])  # Crea la reserva
        with self.assertRaises(OperacionNoPermitidaError):  # Debe fallar
            reserva.procesar()  # Procesar una reserva pendiente

    def test_cancelar_reserva_procesada(self):  # Operación no permitida
        reserva = Reserva("R6", cliente_valido(), servicios_validos()[0])  # Crea la reserva
        reserva.confirmar()  # Confirma
        reserva.procesar()  # Procesa
        with self.assertRaises(OperacionNoPermitidaError):  # Debe fallar
            reserva.cancelar()  # Cancelar una reserva ya procesada

    def test_servicio_no_disponible(self):  # Servicio fuera de servicio
        asesoria = servicios_validos()[2]  # Toma la asesoría
        asesoria.cambiar_disponibilidad(False)  # La marca como no disponible
        with self.assertRaises(ServicioNoDisponibleError):  # Debe lanzar el error propio
            Reserva("R7", cliente_valido(), asesoria)  # Intento de reserva

    def test_cliente_invalido(self):  # Reserva sin cliente
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Reserva("R8", None, servicios_validos()[0])  # Cliente None

    def test_id_de_reserva_vacio(self):  # Reserva sin identificador
        with self.assertRaises(DatosInvalidosError):  # Debe lanzar el error propio
            Reserva("", cliente_valido(), servicios_validos()[0])  # ID vacío

    def test_costo_de_la_reserva_coincide_con_el_servicio(self):  # Coherencia de cálculo
        sala = servicios_validos()[0]  # Toma la sala
        reserva = Reserva("R9", cliente_valido(), sala)  # Crea la reserva
        self.assertEqual(reserva.calcular_costo(), sala.calcular_costo())  # Mismo costo

    def test_errores_quedan_en_el_log(self):  # Los errores se registran
        try:  # Provoca un error controlado
            Reserva("R10", None, servicios_validos()[0])  # Cliente inválido
        except ErrorSoftwareFJ:  # Se captura el error propio
            pass  # No se hace nada más: solo interesa el log
        self.assertIn("ERROR", leer_log())  # Debe haber al menos una línea ERROR


class PruebaEstabilidad(unittest.TestCase):  # El programa debe seguir funcionando ante errores
    def test_el_sistema_continua_tras_errores(self):  # Mezcla de operaciones válidas e inválidas
        operaciones = [  # Lista de operaciones a ejecutar, una tras otra
            lambda: cliente_valido(),  # Válida
            lambda: Cliente("", "x", "x@x.com", "3001234567"),  # Inválida
            lambda: servicios_validos(),  # Válida
            lambda: ReservaSala("S0", "n", "d", "n", 0),  # Inválida
            lambda: Reserva("R11", cliente_valido(), servicios_validos()[0]).confirmar(),  # Válida
            lambda: Reserva("R12", None, None),  # Inválida
        ]  # Fin de la lista
        completadas = 0  # Cuenta cuántas operaciones terminaron (con o sin error)
        for operacion in operaciones:  # Ejecuta todas
            try:  # Intenta la operación
                operacion()  # Ejecuta
            except ErrorSoftwareFJ:  # Si falla con un error propio...
                pass  # ...se sigue con la siguiente
            completadas += 1  # Se cuenta como completada
        self.assertEqual(completadas, len(operaciones))  # Ninguna detuvo el programa


if __name__ == "__main__":  # Permite ejecutar este archivo directamente
    unittest.main(verbosity=2)  # Corre todas las pruebas mostrando el detalle
