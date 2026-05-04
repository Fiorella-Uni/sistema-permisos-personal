from typing import List, Optional
from core.base import Repositorio
from models.entidades import Empleado, TipoPermiso, Permiso


class EmpleadoRepositorio(Repositorio):

    def buscar_por_cedula(self, cedula: str) -> Optional[Empleado]:
        resultado = list(filter(
            lambda e: e.cedula == cedula.strip(),
            self.obtener_todos()
        ))
        return resultado[0] if resultado else None

    def buscar_por_nombre(self, nombre: str) -> List[Empleado]:
        nombre_lower = nombre.lower()
        return list(filter(
            lambda e: nombre_lower in e.nombre.lower(),
            self.obtener_todos()
        ))

    def cedula_existe(self, cedula: str, excluir_id: int = None) -> bool:
        for emp in self.obtener_todos():
            if emp.cedula == cedula and emp.id != excluir_id:
                return True
        return False


class TipoPermisoRepositorio(Repositorio):

    def buscar_por_descripcion(self, texto: str) -> List[TipoPermiso]:
        texto_lower = texto.lower()
        return list(filter(
            lambda tp: texto_lower in tp.descripcion.lower(),
            self.obtener_todos()
        ))

    def obtener_remunerados(self) -> List[TipoPermiso]:
        return list(filter(lambda tp: tp.es_remunerado, self.obtener_todos()))

    def obtener_no_remunerados(self) -> List[TipoPermiso]:
        return list(filter(lambda tp: not tp.es_remunerado, self.obtener_todos()))


class PermisoRepositorio(Repositorio):

    def obtener_por_empleado(self, id_empleado: int) -> List[Permiso]:
        return list(filter(
            lambda p: p.id_empleado == id_empleado,
            self.obtener_todos()
        ))

    def obtener_por_tipo_permiso(self, id_tipo_permiso: int) -> List[Permiso]:
        return list(filter(
            lambda p: p.id_tipo_permiso == id_tipo_permiso,
            self.obtener_todos()
        ))

    def obtener_por_rango_fechas(self, fecha_inicio, fecha_fin) -> List[Permiso]:
        return list(filter(
            lambda p: fecha_inicio <= p.fecha_desde <= fecha_fin,
            self.obtener_todos()
        ))

    def obtener_por_tipo(self, tipo: str) -> List[Permiso]:
        tipo_upper = tipo.upper()
        return list(filter(lambda p: p.tipo == tipo_upper, self.obtener_todos()))
