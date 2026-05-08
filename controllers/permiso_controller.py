from core.mixins import LoggerMixin, ValidationMixin
from core.decoradores import registrar_accion, validar_id_positivo, manejar_errores
from models.entidades import TipoPermiso, Permiso
from models.repositorios import TipoPermisoRepositorio, PermisoRepositorio, EmpleadoRepositorio
from utils.funciones import calcular_descuento
from typing import List, Optional


class TipoPermisoController(LoggerMixin, ValidationMixin):

    def __init__(self, repositorio: TipoPermisoRepositorio):
        super().__init__()
        self._repo = repositorio
        self.log_info("TipoPermisoController inicializado.")

    @manejar_errores
    @registrar_accion("Registrar tipo de permiso")
    def registrar(self, descripcion: str, remunerado_str: str) -> Optional[TipoPermiso]:
        descripcion = self.validar_no_vacio(descripcion, "Descripción")
        remunerado = self.validar_opcion(remunerado_str, ["S", "N"], "Remunerado")

        tipo = TipoPermiso(descripcion=descripcion, remunerado=remunerado)
        self._repo.crear(tipo)
        self.log_info(f"TipoPermiso creado: ID={tipo.id}, descripcion='{tipo.descripcion}'")
        return tipo

    @manejar_errores
    @validar_id_positivo
    def obtener(self, id_tipo: int) -> Optional[TipoPermiso]:
        tipo = self._repo.obtener_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"No existe ningún tipo de permiso con ID={id_tipo}.")
        return tipo

    def listar_todos(self) -> List[TipoPermiso]:
        return self._repo.obtener_todos()

    @manejar_errores
    @registrar_accion("Actualizar tipo de permiso")
    @validar_id_positivo
    def actualizar(
        self,
        id_tipo: int,
        descripcion: str = None,
        remunerado_str: str = None
    ) -> Optional[TipoPermiso]:
        tipo = self._repo.obtener_por_id(id_tipo)
        if not tipo:
            raise ValueError(f"No existe ningún tipo de permiso con ID={id_tipo}.")

        if descripcion is not None:
            tipo.descripcion = self.validar_no_vacio(descripcion, "Descripción")

        if remunerado_str is not None:
            tipo.remunerado = self.validar_opcion(remunerado_str, ["S", "N"], "Remunerado")

        self._repo.actualizar(id_tipo, tipo)
        self.log_info(f"TipoPermiso actualizado: ID={id_tipo}")
        return tipo

    @manejar_errores
    @registrar_accion("Eliminar tipo de permiso")
    @validar_id_positivo
    def eliminar(self, id_tipo: int) -> bool:
        if not self._repo.obtener_por_id(id_tipo):
            raise ValueError(f"No existe ningún tipo de permiso con ID={id_tipo}.")
        resultado = self._repo.eliminar(id_tipo)
        if resultado:
            self.log_info(f"TipoPermiso eliminado: ID={id_tipo}")
        return resultado

    def total(self) -> int:
        return self._repo.contar()


class PermisoController(LoggerMixin, ValidationMixin):

    def __init__(
        self,
        repo_permisos: PermisoRepositorio,
        repo_empleados: EmpleadoRepositorio,
        repo_tipos: TipoPermisoRepositorio,
    ):
        super().__init__()
        self._repo = repo_permisos
        self._repo_emp = repo_empleados
        self._repo_tipos = repo_tipos
        self.log_info("PermisoController inicializado.")

    @manejar_errores
    @registrar_accion("Registrar permiso")
    def registrar(
        self,
        id_empleado_str: str,
        id_tipo_str: str,
        fecha_desde_str: str,
        fecha_hasta_str: str,
        tipo_str: str,
        tiempo_str: str,
    ) -> Optional[Permiso]:
        id_empleado = int(self.validar_numero_positivo(id_empleado_str, "ID Empleado"))
        empleado = self._repo_emp.obtener_por_id(id_empleado)
        if not empleado:
            raise ValueError(f"No existe ningún empleado con ID={id_empleado}.")

        id_tipo = int(self.validar_numero_positivo(id_tipo_str, "ID Tipo Permiso"))
        tipo_permiso = self._repo_tipos.obtener_por_id(id_tipo)
        if not tipo_permiso:
            raise ValueError(f"No existe ningún tipo de permiso con ID={id_tipo}.")

        fecha_desde = self.validar_fecha(fecha_desde_str, "Fecha Desde")
        fecha_hasta = self.validar_fecha(fecha_hasta_str, "Fecha Hasta")
        self.validar_rango_fechas(fecha_desde, fecha_hasta)

        tipo = self.validar_opcion(tipo_str, ["D", "H"], "Tipo (D/H)")
        tiempo = self.validar_numero_positivo(tiempo_str, "Tiempo")

        permiso = Permiso(
            id_empleado=id_empleado,
            id_tipo_permiso=id_tipo,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            tipo=tipo,
            tiempo=tiempo,
        )

        permiso.descuento = calcular_descuento(empleado, permiso, tipo_permiso)

        self._repo.crear(permiso)
        self.log_info(
            f"Permiso creado: ID={permiso.id}, empleado='{empleado.nombre}', "
            f"descuento=${permiso.descuento:.2f}"
        )
        return permiso

    @manejar_errores
    @validar_id_positivo
    def obtener(self, id_permiso: int) -> Optional[Permiso]:
        permiso = self._repo.obtener_por_id(id_permiso)
        if not permiso:
            raise ValueError(f"No existe ningún permiso con ID={id_permiso}.")
        return permiso

    def listar_todos(self) -> List[Permiso]:
        return self._repo.obtener_todos()

    @manejar_errores
    @registrar_accion("Actualizar permiso")
    @validar_id_positivo
    def actualizar(
        self,
        id_permiso: int,
        fecha_desde_str: str = None,
        fecha_hasta_str: str = None,
        tipo_str: str = None,
        tiempo_str: str = None,
    ) -> Optional[Permiso]:
        permiso = self._repo.obtener_por_id(id_permiso)
        if not permiso:
            raise ValueError(f"No existe ningún permiso con ID={id_permiso}.")

        if fecha_desde_str is not None:
            permiso.fecha_desde = self.validar_fecha(fecha_desde_str, "Fecha Desde")

        if fecha_hasta_str is not None:
            permiso.fecha_hasta = self.validar_fecha(fecha_hasta_str, "Fecha Hasta")

        self.validar_rango_fechas(permiso.fecha_desde, permiso.fecha_hasta)

        if tipo_str is not None:
            permiso.tipo = self.validar_opcion(tipo_str, ["D", "H"], "Tipo (D/H)")

        if tiempo_str is not None:
            permiso.tiempo = self.validar_numero_positivo(tiempo_str, "Tiempo")

        empleado = self._repo_emp.obtener_por_id(permiso.id_empleado)
        tipo_permiso = self._repo_tipos.obtener_por_id(permiso.id_tipo_permiso)
        if empleado and tipo_permiso:
            permiso.descuento = calcular_descuento(empleado, permiso, tipo_permiso)

        self._repo.actualizar(id_permiso, permiso)
        self.log_info(f"Permiso actualizado: ID={id_permiso}")
        return permiso

    @manejar_errores
    @registrar_accion("Eliminar permiso")
    @validar_id_positivo
    def eliminar(self, id_permiso: int) -> bool:
        if not self._repo.obtener_por_id(id_permiso):
            raise ValueError(f"No existe ningún permiso con ID={id_permiso}.")
        resultado = self._repo.eliminar(id_permiso)
        if resultado:
            self.log_info(f"Permiso eliminado: ID={id_permiso}")
        return resultado

    def obtener_por_empleado(self, id_empleado: int) -> List[Permiso]:
        return self._repo.obtener_por_empleado(id_empleado)

    def total(self) -> int:
        return self._repo.contar()