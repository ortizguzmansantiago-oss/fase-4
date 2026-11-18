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
        # Una reserva solo puede procesarse cuando ya fue confirmada.
        if self.estado == "Confirmada":
            total = self.servicio.calcular_costo(
                self.duracion,
                impuesto,
                descuento
            )
            logging.info(
                "Reserva %s procesada. Total: %.2f",
                self.numero,
                total
            )
            return total

        raise ReservaInvalida("Primero debe confirmar la reserva.")

    def mostrar(self):
        datos_cliente = self.cliente.nombre
        tipo_servicio = self.servicio.describir()
        return (
            f"Reserva {self.numero}: {datos_cliente}, "
            f"{tipo_servicio}, {self.estado}"
        )


# Clase encargada de administrar clientes, servicios y reservas.
class SoftwareFJ:
    def __init__(self):
        self.clientes = list()
        self.servicios = list()
        self.reservas = list()
        self.numero = 1

    def registrar_cliente(self, cliente):
        try:
            cliente_repetido = any(
                registrado._codigo == cliente._codigo
                for registrado in self.clientes
            )

            if cliente_repetido:
                raise DatoInvalido("El cliente ya está registrado.")

            self.clientes.append(cliente)

        except ErrorSistema as error:
            logging.error("Registro de cliente: %s", error)
            print("Error:", error)
            return False

        logging.info("Cliente registrado: %s", cliente.nombre)
        print("Cliente registrado:", cliente.nombre)
        return True

    def agregar_servicio(self, servicio):
        try:
            servicio_repetido = any(
                registrado.codigo == servicio.codigo
                for registrado in self.servicios
            )

            if servicio_repetido:
                raise DatoInvalido("El servicio ya existe.")

            self.servicios.append(servicio)

        except ErrorSistema as error:
            logging.error("Registro de servicio: %s", error)
            print("Error:", error)
            return False

        logging.info("Servicio agregado: %s", servicio.nombre)
        print("Servicio agregado:", servicio.nombre)
        return True

    def crear_reserva(self, cliente, servicio, duracion):
        try:
            # Se comprueba que ambos elementos pertenezcan al sistema.
            if cliente not in self.clientes:
                raise ReservaInvalida("El cliente no está registrado.")

            if servicio not in self.servicios:
                raise ReservaInvalida("El servicio no está disponible.")

            nueva_reserva = Reserva(
                self.numero,
                cliente,
                servicio,
                duracion
            )

            self.reservas.append(nueva_reserva)
            logging.info("Reserva %s creada.", nueva_reserva.numero)
            print("Reserva creada:", nueva_reserva.numero)

            self.numero += 1
            return nueva_reserva

        except ErrorSistema as error:
            logging.error("Creación de reserva: %s", error)
            print("Error:", error)
            return None

        finally:
            print("Fin del intento de reserva.")


def ejecutar():
    sistema = SoftwareFJ()
    print("\\n=== SISTEMA SOFTWARE FJ ===")

    # Registro de clientes.
    cliente1 = Cliente("C01", "Carlos Pérez", "carlos@gmail.com")
    sistema.registrar_cliente(cliente1)

    try:
        Cliente("C02", "Ana", "correo incorrecto")
    except DatoInvalido as error:
        logging.error("Cliente inválido: %s", error)
        print("Error de cliente:", error)

    cliente2 = Cliente("C03", "Laura Gómez", "laura@gmail.com")
    sistema.registrar_cliente(cliente2)

    # Creación y registro de los servicios disponibles.
    sala = Sala("S01", "Sala de reuniones", 50000)
    equipo = Equipo("E01", "Computador", 80000)
    asesoria = Asesoria("A01", "Asesoría de programación", 60000)

    for servicio in (sala, equipo, asesoria):
        sistema.agregar_servicio(servicio)

    # Comprobación de una tarifa incorrecta.
    try:
        Sala("S02", "Sala incorrecta", 0)
    except DatoInvalido as error:
        logging.error("Servicio inválido: %s", error)
        print("Error de servicio:", error)

    # Primera reserva: se confirma y se calcula con impuesto y descuento.
    reserva1 = sistema.crear_reserva(cliente1, sala, 2)

    if reserva1 is not None:
        reserva1.confirmar()
        total_reserva1 = reserva1.procesar(impuesto=19, descuento=10)
        print("Total con impuesto y descuento:", total_reserva1)

    # Segunda reserva: se confirma y se calcula sin ajustes.
    reserva2 = sistema.crear_reserva(cliente2, equipo, 3)

    if reserva2 is not None:
        reserva2.confirmar()
        print("Total normal:", reserva2.procesar())

    # Pruebas de validación de reservas.
    sistema.crear_reserva(cliente1, asesoria, 0)

    cliente3 = Cliente("C99", "Pedro Ruiz", "pedro@gmail.com")
    sistema.crear_reserva(cliente3, sala, 1)

    # Se cancela la segunda reserva.
    if reserva2 is not None:
        reserva2.cancelar()
        print("Reserva cancelada.")

    print("\\n--- Reservas registradas ---")
    for elemento in sistema.reservas:
        print(elemento.mostrar())

    print(
        "\\nProceso terminado. Revise software_fj.log "
        "para ver los registros."
    )


if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as error:
        logging.exception("Error inesperado: %s", error)
        print("Ocurrió un error inesperado:", error)
        
