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

    def procesar(self, impuesto=0, descuento=0):
        if self.estado != "Confirmada":
            raise ReservaInvalida("Primero debe confirmar la reserva.")
        total = self.servicio.calcular_costo(
            self.duracion, impuesto, descuento
        )
        logging.info("Reserva %s procesada. Total: %.2f", self.numero, total)
        return total

    def mostrar(self):
        return f"Reserva {self.numero}: {self.cliente.nombre}, {self.servicio.describir()}, {self.estado}"


# Administración del sistema mediante listas
class SoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.numero = 1

    def registrar_cliente(self, cliente):
        try:
            if any(c._codigo == cliente._codigo for c in self.clientes):
                raise DatoInvalido("El cliente ya está registrado.")
        except ErrorSistema as error:
            logging.error("Registro de cliente: %s", error)
            print("Error:", error)
            return False
        else:
            self.clientes.append(cliente)
            logging.info("Cliente registrado: %s", cliente.nombre)
            print("Cliente registrado:", cliente.nombre)
            return True

    def agregar_servicio(self, servicio):
        try:
            if any(s.codigo == servicio.codigo for s in self.servicios):
                raise DatoInvalido("El servicio ya existe.")
            self.servicios.append(servicio)
            logging.info("Servicio agregado: %s", servicio.nombre)
            print("Servicio agregado:", servicio.nombre)
            return True
        except ErrorSistema as error:
            logging.error("Registro de servicio: %s", error)
            print("Error:", error)
            return False

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            if cliente not in self.clientes:
                raise ReservaInvalida("El cliente no está registrado.")
            if servicio not in self.servicios:
                raise ReservaInvalida("El servicio no está disponible.")
            reserva = Reserva(self.numero, cliente, servicio, duracion)
            self.reservas.append(reserva)
            self.numero += 1
            logging.info("Reserva %s creada.", reserva.numero)
            print("Reserva creada:", reserva.numero)
            return reserva
        except ErrorSistema as error:
            logging.error("Creación de reserva: %s", error)
            print("Error:", error)
            return None
        finally:
            print("Fin del intento de reserva.")


def ejecutar():
    sistema = SoftwareFJ()
    print("\n=== SISTEMA SOFTWARE FJ ===")

    # 1 y 2: registro de clientes válido e inválido
    cliente1 = Cliente("C01", "Carlos Pérez", "carlos@gmail.com")
    sistema.registrar_cliente(cliente1)
    try:
        Cliente("C02", "Ana", "correo incorrecto")
    except DatoInvalido as error:
        logging.error("Cliente inválido: %s", error)
        print("Error de cliente:", error)

    # 3: segundo cliente válido
    cliente2 = Cliente("C03", "Laura Gómez", "laura@gmail.com")
    sistema.registrar_cliente(cliente2)

    # 4, 5 y 6: registro de los tres tipos de servicio
    sala = Sala("S01", "Sala de reuniones", 50000)
    equipo = Equipo("E01", "Computador", 80000)
    asesoria = Asesoria("A01", "Asesoría de programación", 60000)
    sistema.agregar_servicio(sala)
    sistema.agregar_servicio(equipo)
    sistema.agregar_servicio(asesoria)

    # 7: intento de crear un servicio con tarifa inválida
    try:
        Sala("S02", "Sala incorrecta", 0)
    except DatoInvalido as error:
        logging.error("Servicio inválido: %s", error)
        print("Error de servicio:", error)

    # 8: reserva correcta, confirmación y cálculo con impuesto/descuento
    reserva1 = sistema.crear_reserva(cliente1, sala, 2)
    if reserva1:
        reserva1.confirmar()
        print("Total con impuesto y descuento:",
              reserva1.procesar(impuesto=19, descuento=10))

    # 9: segunda reserva y cálculo sin impuesto ni descuento
    reserva2 = sistema.crear_reserva(cliente2, equipo, 3)
    if reserva2:
        reserva2.confirmar()
        print("Total normal:", reserva2.procesar())

    # 10: reserva con duración inválida
    sistema.crear_reserva(cliente1, asesoria, 0)

    # 11: reserva con cliente no registrado
    cliente3 = Cliente("C99", "Pedro Ruiz", "pedro@gmail.com")
    sistema.crear_reserva(cliente3, sala, 1)

    # 12: cancelar una reserva
    if reserva2:
        reserva2.cancelar()
        print("Reserva cancelada.")

    print("\n--- Reservas registradas ---")
    for reserva in sistema.reservas:
        print(reserva.mostrar())

    print("\nProceso terminado. Revise software_fj.log para ver los registros.")


if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as error:
        logging.exception("Error inesperado: %s", error)
        print("Ocurrió un error inesperado:", error)
