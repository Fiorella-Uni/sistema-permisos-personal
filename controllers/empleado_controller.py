from core.mixins import LoggerMixin, ValidationMixin
from core.decoradores import registrar_accion, validar_id_positivo, manejar_errores
from models.entidades import Empleado
from models.repositorios import EmpleadoRepositorio
from typing import List, Optional


class EmpleadoController(LoggerMixin, ValidationMixin):

    def __init__(self, repositorio: EmpleadoRepositorio):
        super().__init__()
        self._repo = repositorio
        self.log_info("EmpleadoController inicializado.")

    @manejar_errores
    @registrar_accion("Registrar empleado")
    def registrar(self, nombre: str, cedula: str, sueldo_str: str) -> Optional[Empleado]:
        nombre = self.validar_no_vacio(nombre, "Nombre")
        cedula = self.validar_cedula_ecuatoriana(cedula)

        if self._repo.cedula_existe(cedula):
            raise ValueError(f"Ya existe un empleado registrado con la cédula '{cedula}'.")

        sueldo = self.validar_numero_positivo(sueldo_str, "Sueldo")

        empleado = Empleado(nombre=nombre, cedula=cedula, sueldo=sueldo)
        self._repo.crear(empleado)
        self.log_info(f"Empleado creado: ID={empleado.id}, nombre='{empleado.nombre}'")
        return empleado

    @manejar_errores
    @validar_id_positivo
    def obtener(self, id_empleado: int) -> Optional[Empleado]:
        empleado = self._repo.obtener_por_id(id_empleado)
        if not empleado:
            raise ValueError(f"No existe ningún empleado con ID={id_empleado}.")
        return empleado

    def listar_todos(self) -> List[Empleado]:
        return self._repo.obtener_todos()

    @manejar_errores
    @registrar_accion("Actualizar empleado")
    @validar_id_positivo
    def actualizar(
        self,
        id_empleado: int,
        nombre: str = None,
        cedula: str = None,
        sueldo_str: str = None
    ) -> Optional[Empleado]:
        empleado = self._repo.obtener_por_id(id_empleado)
        if not empleado:
            raise ValueError(f"No existe ningún empleado con ID={id_empleado}.")

        if nombre is not None:
            empleado.nombre = self.validar_no_vacio(nombre, "Nombre")

        if cedula is not None:
            cedula = self.validar_cedula_ecuatoriana(cedula)
            if self._repo.cedula_existe(cedula, excluir_id=id_empleado):
                raise ValueError(f"Ya existe otro empleado con la cédula '{cedula}'.")
            empleado.cedula = cedula

        if sueldo_str is not None:
            sueldo = self.validar_numero_positivo(sueldo_str, "Sueldo")
            empleado.sueldo = sueldo
            empleado.valor_hora = round(sueldo / 240, 4)

        self._repo.actualizar(id_empleado, empleado)
        self.log_info(f"Empleado actualizado: ID={id_empleado}")
        return empleado

    @manejar_errores
    @registrar_accion("Eliminar empleado")
    @validar_id_positivo
    def eliminar(self, id_empleado: int) -> bool:
        if not self._repo.obtener_por_id(id_empleado):
            raise ValueError(f"No existe ningún empleado con ID={id_empleado}.")
        resultado = self._repo.eliminar(id_empleado)
        if resultado:
            self.log_info(f"Empleado eliminado: ID={id_empleado}")
        return resultado

    def buscar_por_cedula(self, cedula: str) -> Optional[Empleado]:
        return self._repo.buscar_por_cedula(cedula)

    def buscar_por_nombre(self, nombre: str) -> List[Empleado]:
        return self._repo.buscar_por_nombre(nombre)

    def total(self) -> int:
        return self._repo.contar()