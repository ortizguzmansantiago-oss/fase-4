"""
Sistema de gestión de clientes, servicios y reservas - Software FJ
Proyecto académico de Programación Orientada a Objetos.
No utiliza bases de datos: guarda la información en listas.
"""

from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Excepciones personalizadas
class ErrorSistema(Exception):
    pass


class DatoInvalido(ErrorSistema):
    pass


class ReservaInvalida(ErrorSistema):
    pass


# Clase abstracta general
class Entidad(ABC):
    def __init__(self, codigo):
        if not codigo:
            raise DatoInvalido("El código es obligatorio.")
        self._codigo = codigo

    @abstractmethod
    def mostrar(self):
        pass


# Cliente con datos encapsulados y validados
class Cliente(Entidad):
    def __init__(self, codigo, nombre, correo):
        super().__init__(codigo)
        if not nombre.strip() or "@" not in correo:
            raise DatoInvalido("Nombre o correo no válido.")
        self._nombre = nombre
        self._correo = correo

    @property
    def nombre(self):
        return self._nombre

    def mostrar(self):
        return f"{self._nombre} - {self._correo}"


# Clase abstracta Servicio
class Servicio(ABC):
    def __init__(self, codigo, nombre, tarifa):
        if not codigo or not nombre or tarifa <= 0:
            raise DatoInvalido("Datos del servicio no válidos.")
        self.codigo = codigo
        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def validar(self, duracion):
        pass

    @abstractmethod
    def describir(self):
        pass

    # Los parámetros opcionales permiten calcular con impuesto y descuento.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self.validar(duracion)
        subtotal = self.tarifa * duracion
        return subtotal + subtotal * impuesto / 100 - subtotal * descuento / 100


class Sala(Servicio):
    def validar(self, duracion):
        if not 1 <= duracion <= 12:
            raise DatoInvalido("La sala se reserva de 1 a 12 horas.")

    def describir(self):
        return "Reserva de sala"


class Equipo(Servicio):
    def validar(self, duracion):
        if not 1 <= duracion <= 30:
            raise DatoInvalido("El equipo se alquila de 1 a 30 días.")

    def describir(self):
        return "Alquiler de equipo"


class Asesoria(Servicio):
    def validar(self, duracion):
        if not 1 <= duracion <= 8:
            raise DatoInvalido("La asesoría dura de 1 a 8 horas.")

    def describir(self):
        return "Asesoría especializada"


# Reserva que relaciona cliente y servicio
class Reserva:
    def __init__(self, numero, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalida("Cliente o servicio incorrecto.")
        try:
            servicio.validar(duracion)
        except DatoInvalido as error:
            raise ReservaInvalida("No se pudo crear la reserva.") from error

        self.numero = numero
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        if self.estado != "Pendiente":
            raise ReservaInvalida("La reserva no está pendiente.")
        self.estado = "Confirmada"
        logging.info("Reserva %s confirmada.", self.numero)

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaInvalida("La reserva ya está cancelada.")
        self.estado = "Cancelada"
        logging.info("Reserva %s cancelada.", self.numero)


