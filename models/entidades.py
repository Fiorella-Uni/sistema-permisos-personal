import datetime
from typing import Optional


class Empleado:

    def __init__(self, nombre: str, cedula: str, sueldo: float):
        self.id: Optional[int] = None
        self.nombre: str = nombre
        self.cedula: str = cedula
        self.sueldo: float = sueldo
        self.valor_hora: float = round(sueldo / 240, 4)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cedula": self.cedula,
            "sueldo": self.sueldo,
            "valor_hora": self.valor_hora,
        }

    def __str__(self) -> str:
        return (
            f"Empleado(id={self.id}, nombre='{self.nombre}', "
            f"cédula={self.cedula}, sueldo=${self.sueldo:.2f}, "
            f"valor_hora=${self.valor_hora:.4f})"
        )

    def __repr__(self) -> str:
        return self.__str__()


class TipoPermiso:

    def __init__(self, descripcion: str, remunerado: str):
        self.id: Optional[int] = None
        self.descripcion: str = descripcion
        self.remunerado: str = remunerado.upper()

    @property
    def es_remunerado(self) -> bool:
        return self.remunerado == "S"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "remunerado": self.remunerado,
        }

    def __str__(self) -> str:
        rem = "Remunerado" if self.es_remunerado else "No Remunerado"
        return f"TipoPermiso(id={self.id}, descripcion='{self.descripcion}', {rem})"

    def __repr__(self) -> str:
        return self.__str__()


class Permiso:

    def __init__(
        self,
        id_empleado: int,
        id_tipo_permiso: int,
        fecha_desde: datetime.date,
        fecha_hasta: datetime.date,
        tipo: str,
        tiempo: float,
    ):
        self.id: Optional[int] = None
        self.id_empleado: int = id_empleado
        self.id_tipo_permiso: int = id_tipo_permiso
        self.fecha_desde: datetime.date = fecha_desde
        self.fecha_hasta: datetime.date = fecha_hasta
        self.tipo: str = tipo.upper()
        self.tiempo: float = tiempo
        self.descuento: float = 0.0

    @property
    def duracion_dias(self) -> int:
        return (self.fecha_hasta - self.fecha_desde).days + 1

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "id_empleado": self.id_empleado,
            "id_tipo_permiso": self.id_tipo_permiso,
            "fecha_desde": str(self.fecha_desde),
            "fecha_hasta": str(self.fecha_hasta),
            "tipo": self.tipo,
            "tiempo": self.tiempo,
            "descuento": self.descuento,
        }

    def __str__(self) -> str:
        tipo_label = "Días" if self.tipo == "D" else "Horas"
        return (
            f"Permiso(id={self.id}, empleado_id={self.id_empleado}, "
            f"tipo_permiso_id={self.id_tipo_permiso}, "
            f"desde={self.fecha_desde}, hasta={self.fecha_hasta}, "
            f"tipo={tipo_label}, tiempo={self.tiempo}, "
            f"descuento=${self.descuento:.2f})"
        )

    def __repr__(self) -> str:
        return self.__str__()
