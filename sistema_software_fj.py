"""
Sistema de gestión de clientes, servicios y reservas - Software FJ
Proyecto académico de Programación Orientada a Objetos.
No utiliza bases de datos: guarda la información en listas.
"""

from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)


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

# 1. solicitar cantidad de productos a registrar
num_productos = int(input("ingrese el numero de productos a registrar: "))
productos = []
valor_total_inventario = 0
# 2. registrar datos de cada producto 
for i in range(num_productos) : 
    print(f"\n--- producto {i+1} ---")
    nombre = input("nombre del producto:")
    cantidad = int(input("cantidad de inventario: "))
    cantidad_minima = int(input("cantidad minima requerida: "))
    precio = float(input("precio por unidad: "))
    #Guardar producto 
    producto = {
        "nombre": nombre,
        "cantidad" : cantidad,
        "cantidad minima": cantidad_minima,
        "precio": precio
    }
    productos.append(producto)
    #sumar al valor total del invetario 
    valor_total_inventario += cantidad * precio 
    #3. mostrar resultados
    print("\n========================================")
    print(" RESULTADOS DEL INVENTARIO")
    print("========================================")
    print(f"\nValor total del invetarion: $ {valor_total_inventario:, .2f}")
    #productos que necesitan rebastecimiento 
    print("\nProductos que necesitan rebastecimiento:")
    necesitan_rebastecer = false
    for p in producto :
        if p["cantidad"] < p["cantidad_minima"]:
             necesitan_reabastecer = True
             print(f"- {p['nombre']} (cantidad actual: {p['cantidad']}, minima: {p['cantidad_minima']})")
             if not necesitan_reabastecer:
                print("Todos los productos tienen inventario sufuciente.")

    print("\nProceso terminado. Revise software_fj.log para ver los registros.")


if __name__ == "__main__":
    try:
        ejecutar()
    except Exception as error:
        logging.exception("Error inesperado: %s", error)
        print("Ocurrió un error inesperado:", error)

