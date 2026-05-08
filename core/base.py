import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class CRUDBase(ABC):
    @abstractmethod
    def crear(self, entidad: Any) -> Any:
        pass

    @abstractmethod
    def obtener_por_id(self, id_entidad: int) -> Optional[Any]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Any]:
        pass

    @abstractmethod
    def actualizar(self, id_entidad: int, entidad: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def eliminar(self, id_entidad: int) -> bool:
        pass

    @abstractmethod
    def contar(self) -> int:
        pass
class Repositorio(CRUDBase):

    archivo_json: str = ""  

    def __init__(self):
        self._almacen: Dict[int, Any] = {}
        self._contador_id: int = 0
        self._cargar()  

    def _generar_id(self) -> int:
        self._contador_id += 1
        return self._contador_id

    

    def _desde_dict(self, data: dict) -> Any:
        """Cada subclase DEBE implementar esto para reconstruir el objeto."""
        raise NotImplementedError

    def _cargar(self):
        """Lee el JSON y llena el almacén al iniciar."""
        if not self.archivo_json or not os.path.exists(self.archivo_json):
            return
        with open(self.archivo_json, "r", encoding="utf-8") as f:
            registros = json.load(f)
        for data in registros:
            obj = self._desde_dict(data)
            self._almacen[obj.id] = obj
        if self._almacen:
            self._contador_id = max(self._almacen.keys())  
    def _guardar(self):
        """Serializa todo el almacén al JSON."""
        if not self.archivo_json:
            return
        os.makedirs(os.path.dirname(self.archivo_json), exist_ok=True)
        with open(self.archivo_json, "w", encoding="utf-8") as f:
            json.dump(
                [obj.to_dict() for obj in self._almacen.values()],
                f, indent=4, ensure_ascii=False
            )

    

    def crear(self, entidad: Any) -> Any:
        entidad.id = self._generar_id()
        self._almacen[entidad.id] = entidad
        self._guardar()  

    def obtener_por_id(self, id_entidad: int) -> Optional[Any]:
        return self._almacen.get(id_entidad)

    def obtener_todos(self) -> List[Any]:
        return list(self._almacen.values())

    def actualizar(self, id_entidad: int, entidad: Any) -> Optional[Any]:
        if id_entidad in self._almacen:
            self._almacen[id_entidad] = entidad
            self._guardar()  
            return entidad
        return None

    def eliminar(self, id_entidad: int) -> bool:
        if id_entidad in self._almacen:
            del self._almacen[id_entidad]
            self._guardar()  
            return True
        return False

    def contar(self) -> int:
        return len(self._almacen)