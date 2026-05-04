from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class CRUDBase(ABC):

    @abstractmethod
    def crear(self, datos: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def obtener_por_id(self, id_entidad: int) -> Optional[Any]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Any]:
        pass

    @abstractmethod
    def actualizar(self, id_entidad: int, datos: Dict[str, Any]) -> Optional[Any]:
        pass

    @abstractmethod
    def eliminar(self, id_entidad: int) -> bool:
        pass

    def contar(self) -> int:
        return len(self.obtener_todos())


class Repositorio(CRUDBase):

    def __init__(self):
        self._almacen: Dict[int, Any] = {}
        self._contador_id: int = 0

    def _generar_id(self) -> int:
        self._contador_id += 1
        return self._contador_id

    def crear(self, entidad: Any) -> Any:
        entidad.id = self._generar_id()
        self._almacen[entidad.id] = entidad
        return entidad

    def obtener_por_id(self, id_entidad: int) -> Optional[Any]:
        return self._almacen.get(id_entidad)

    def obtener_todos(self) -> List[Any]:
        return list(self._almacen.values())

    def actualizar(self, id_entidad: int, entidad: Any) -> Optional[Any]:
        if id_entidad in self._almacen:
            self._almacen[id_entidad] = entidad
            return entidad
        return None

    def eliminar(self, id_entidad: int) -> bool:
        if id_entidad in self._almacen:
            del self._almacen[id_entidad]
            return True
        return False
