# Sistema de Registro de Permisos del Personal

**Sistema de gestión de permisos laborales desarrollado en Python con arquitectura de mini-framework que aplica los cuatro pilares de la Programación Orientada a Objetos.**

---

## Integrantes del Equipo

| N° | Nombre Completo |
|:---:|---|
| 1 | Fiorella Naomi Solis Garcia | 
| 2 | Katherine Michelle Jara Plasencia |
| 3 | Melany Anahis Parra Potes | 
| 4 | Jamile Waleska Parra Avila | 
| 5 | Tiffany Andrea Arroyo Cevillano | 

**Materia:** Programación Orientada a Objetos  
**Fecha:** Mayo 2026

---

## Repositorio GitHub

```[
https://github.com/Fiorella-Uni/sistema-permisos-personal.git
```

---

## Objetivo del Proyecto

### Objetivo General

Desarrollar un **Sistema de Gestión de Permisos Laborales** en Python que aplique de manera integral los cuatro pilares de la **Programación Orientada a Objetos** (Abstracción, Herencia, Encapsulamiento y Polimorfismo), mediante la implementación de un mini-framework con arquitectura **Modelo-Vista-Controlador (MVC)**, que permita registrar, consultar, actualizar y eliminar permisos del personal de una empresa, calculando automáticamente descuentos salariales según el tipo de permiso, y demostrando el uso de clases abstractas, herencia múltiple, decoradores, mixins, funciones de orden superior y validaciones avanzadas como el algoritmo Módulo 10 para cédulas ecuatorianas.

### Objetivos Específicos

- Implementar **clases abstractas** con el módulo `abc` de Python para definir contratos CRUD que obliguen a los repositorios concretos a implementar los cinco métodos base.
- Aplicar **herencia múltiple** mediante Mixins (`LoggerMixin`, `ValidationMixin`) en los controladores, aprovechando el MRO (Method Resolution Order) de Python.
- Demostrar **encapsulamiento** con atributos privados (convención `_`), propiedades `@property` y métodos de acceso controlado en entidades y controladores.
- Usar **polimorfismo** a través de la cadena de herencia `CRUDBase → Repositorio → {EmpleadoRepositorio, TipoPermisoRepositorio, PermisoRepositorio}`.
- Implementar **decoradores de función** (`@manejar_errores`, `@registrar_accion`, `@validar_id_positivo`, `@confirmar_operacion`, `@cronometrar`) para separar responsabilidades transversales.
- Aplicar **programación funcional** con `map()`, `filter()` y `reduce()` en el cálculo de estadísticas del sistema.
- Validar cédulas ecuatorianas usando el **algoritmo Módulo 10**, verificando provincia, tipo de persona y dígito verificador.
- Crear una interfaz de consola interactiva y colorida usando **códigos de escape ANSI**, con funciones de posicionamiento de cursor (`gotoxy`).

---

## Estructura del Proyecto

```
sistema_permisos_2/
├── core/
│   ├── base.py              → Clases abstractas CRUD (CRUDBase, Repositorio)
│   ├── decoradores.py       → Decoradores y funciones de orden superior
│   ├── mixins.py            → Mixins reutilizables (LoggerMixin, ValidationMixin)
│   └── json_manager.py      → Gestión de persistencia en archivos JSON
├── models/
│   ├── entidades.py         → Modelos de dominio (Empleado, TipoPermiso, Permiso)
│   └── repositorios.py      → Repositorios concretos por entidad
├── controllers/
│   ├── empleado_controller.py   → Lógica de negocio de Empleados
│   └── permiso_controller.py   → Lógica de negocio de Permisos y Tipos
├── data/
│   ├── empleados.json       → Persistencia de empleados
│   ├── permisos.json        → Persistencia de permisos
│   ├── tipos_permiso.json   → Tipos de permiso disponibles
│   ├── entidades.json       → Datos de entidades
│   └── repositorios.json    → Datos de repositorios
├── docs/
│   ├── arquitectura_codigo.excalidraw  → Diagrama de arquitectura
│   └── diagrama_clases.excalidraw      → Diagrama de clases UML
├── utils/
│   ├── funciones.py         → Funciones de orden superior y cálculos
│   └── test_json.py         → Pruebas de persistencia JSON
└── main.py                  → Punto de entrada del sistema
```

---

## Arquitectura: Patrón MVC

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| **Modelo** | `models/` | Datos y persistencia en memoria / JSON |
| **Vista** | `views/` | Presentación en consola con colores ANSI |
| **Controlador** | `controllers/` | Lógica de negocio y validaciones |
| **Core** | `core/` | Base del mini-framework (abstractas, mixins, decoradores) |
| **Utils** | `utils/` | Funciones de orden superior y cálculos estadísticos |

---

## Pilares de la POO Aplicados

### 1. Abstracción — `core/base.py`

La abstracción se aplica mediante la clase abstracta `CRUDBase`, que define **qué operaciones deben existir** sin especificar **cómo** se implementan:

```python
from abc import ABC, abstractmethod

class CRUDBase(ABC):
    @abstractmethod
    def crear(self, datos): pass

    @abstractmethod
    def obtener_por_id(self, id_entidad): pass

    @abstractmethod
    def obtener_todos(self): pass

    @abstractmethod
    def actualizar(self, id_entidad, datos): pass

    @abstractmethod
    def eliminar(self, id_entidad): pass
```

### 2. Herencia — Cadena completa de herencia

```
CRUDBase (abstracta)
    └── Repositorio (implementación base)
            ├── EmpleadoRepositorio
            ├── TipoPermisoRepositorio
            └── PermisoRepositorio
```

### 3. Encapsulamiento — Atributos y acceso controlado

```python
class Repositorio(CRUDBase):
    def __init__(self):
        self._almacen: Dict[int, Any] = {}   # privado
        self._contador_id: int = 0            # privado

class Permiso:
    @property
    def duracion_dias(self) -> int:
        return (self.fecha_hasta - self.fecha_desde).days + 1
```

### 4. Polimorfismo — Herencia múltiple con Mixins

```python
class EmpleadoController(LoggerMixin, ValidationMixin):
    ...

class PermisoController(LoggerMixin, ValidationMixin):
    ...
```

---

## Conceptos POO Adicionales

| Concepto | Dónde | Cómo |
|---|---|---|
| Clases abstractas | `CRUDBase` | `ABC` + `@abstractmethod` |
| Herencia múltiple | Controladores | `(LoggerMixin, ValidationMixin)` |
| Propiedades | `TipoPermiso`, `Permiso` | `@property` |
| Métodos estáticos | `ValidationMixin` | `@staticmethod` |
| Inyección de dependencias | `PermisoController` | Repositorios como parámetros |
| Decoradores de función | `core/decoradores.py` | `functools.wraps` |
| Funciones de orden superior | `utils/funciones.py` | `map`, `filter`, `reduce`, lambdas |
| Dunder methods | Entidades | `__str__`, `__repr__` |
| Type hints | Todo el proyecto | `List`, `Optional`, `Dict`, `Any` |

---

## Descripción de Clases y Módulos

### `core/mixins.py`

#### `LoggerMixin`
| Método | Descripción |
|---|---|
| `log(nivel, mensaje)` | Registra con timestamp y nivel |
| `log_info(mensaje)` | Atajo para nivel INFO |
| `log_error(mensaje)` | Atajo para nivel ERROR |
| `log_advertencia(mensaje)` | Atajo para nivel ADVERTENCIA |
| `obtener_historial()` | Retorna copia del historial |
| `mostrar_historial()` | Imprime las últimas 20 entradas |

#### `ValidationMixin`
| Método | Descripción |
|---|---|
| `validar_no_vacio(valor, campo)` | Valida string no vacío |
| `validar_numero_positivo(valor, campo)` | Valida número > 0 |
| `validar_opcion(valor, opciones, campo)` | Valida que valor esté en lista permitida |
| `validar_fecha(fecha_str, campo)` | Convierte string a `date` (DD/MM/YYYY o YYYY-MM-DD) |
| `validar_rango_fechas(inicio, fin)` | Valida que inicio ≤ fin |
| `validar_cedula_ecuatoriana(cedula)` | Algoritmo Módulo 10 para cédulas ecuatorianas |

### `core/decoradores.py`

| Decorador | Tipo | Descripción |
|---|---|---|
| `@manejar_errores` | Simple | Captura `ValueError` y `Exception` |
| `@registrar_accion(desc)` | Fábrica | Registra ejecución con timestamp |
| `@validar_id_positivo` | Simple | Valida primer argumento entero positivo |
| `@confirmar_operacion(msg)` | Fábrica | Solicita confirmación `s/n` |
| `@cronometrar` | Simple | Mide tiempo de ejecución |

### `models/entidades.py`

#### `Empleado`
| Atributo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Asignado por el repositorio |
| `nombre` | `str` | Nombre completo |
| `cedula` | `str` | Validada con Módulo 10 |
| `sueldo` | `float` | Sueldo mensual |
| `valor_hora` | `@property float` | `sueldo / 240` |

#### `TipoPermiso`
| Atributo | Tipo | Descripción |
|---|---|---|
| `descripcion` | `str` | Nombre del tipo (ej: "Enfermedad") |
| `remunerado` | `str` | `'S'` o `'N'` |
| `es_remunerado` | `@property bool` | `remunerado == "S"` |

#### `Permiso`
| Atributo | Tipo | Descripción |
|---|---|---|
| `id_empleado` | `int` | FK al empleado |
| `id_tipo_permiso` | `int` | FK al tipo de permiso |
| `fecha_desde` / `fecha_hasta` | `date` | Rango del permiso |
| `tipo` | `str` | `'D'` (días) o `'H'` (horas) |
| `tiempo` | `float` | Cantidad de días u horas |
| `descuento` | `float` | Calculado por el controlador |
| `duracion_dias` | `@property int` | Diferencia entre fechas + 1 |

---

## Lógica de Negocio — Cálculo de Descuento

| Condición | Fórmula |
|---|---|
| Permiso remunerado | `descuento = 0` |
| Tipo `'H'` (horas), no remunerado | `descuento = valor_hora × tiempo` |
| Tipo `'D'` (días), no remunerado | `descuento = (sueldo / 30) × tiempo` |

---

## Flujo de Ejecución

```
main()
  ├── cargar_datos_muestra()
  └── bucle menú principal
        ├── modulo_empleados()
        │     └── ctrl_empleados.registrar(nombre, cedula, sueldo)
        │           ├── ValidationMixin.validar_cedula_ecuatoriana()
        │           ├── EmpleadoRepositorio.cedula_existe()
        │           └── EmpleadoRepositorio.crear(empleado)
        │
        ├── modulo_permisos()
        │     └── ctrl_permisos.registrar(id_emp, id_tipo, ...)
        │           ├── Valida empleado y tipo existen
        │           ├── ValidationMixin.validar_fecha()
        │           ├── calcular_descuento(empleado, permiso, tipo)
        │           └── PermisoRepositorio.crear(permiso)
        │
        └── modulo_estadisticas()
              └── calcular_estadisticas_permisos()
                    └── map + filter + reduce sobre colecciones
```

---

## Prompts Utilizados con la IA

### Estructura y Arquitectura
- *"Ayúdame a estructurar un proyecto Python con patrón MVC para gestión de permisos laborales."*
- *"¿Cómo organizo las carpetas de un mini-framework en Python?"*
- *"Necesito una arquitectura limpia que separe modelos, controladores y vistas en consola."*
- *"¿Cómo implemento inyección de dependencias en Python sin usar un framework externo?"*

### Programación Orientada a Objetos
- *"¿Cómo creo una clase abstracta en Python que obligue a implementar métodos CRUD?"*
- *"Explícame cómo funciona la herencia múltiple con Mixins en Python."*
- *"¿Cómo uso @property para encapsular lógica en mis entidades?"*
- *"¿Cómo apilo decoradores en métodos de una clase sin perder el nombre original de la función?"*
- *"¿Qué es el MRO en Python y cómo afecta a super().__init__() en herencia múltiple?"*
- *"¿Cómo implemento el patrón Repositorio genérico con herencia en Python?"*

### Lógica de Negocio y Validaciones
- *"¿Cómo valido una cédula ecuatoriana con el algoritmo Módulo 10 en Python?"*
- *"Necesito calcular el descuento de un permiso según si es remunerado, por horas o por días."*
- *"¿Cómo hago búsquedas parciales case-insensitive sobre una lista de objetos?"*
- *"¿Cómo valido que una fecha de inicio sea menor o igual a la fecha de fin?"*
- *"¿Cómo convierto un string de fecha en formato DD/MM/YYYY a un objeto date en Python?"*

### Programación Funcional
- *"¿Cómo uso map, filter y reduce para calcular estadísticas sobre una lista de objetos?"*
- *"¿Cómo paso funciones como parámetro en Python usando lambdas?"*
- *"¿Cómo creo una función de orden superior que repita un input hasta recibir un valor válido?"*
- *"Muéstrame cómo implementar wrappers de map() y filter() que sean reutilizables."*

### Interfaz de Consola
- *"¿Cómo uso códigos ANSI para darle color a la terminal en Python?"*
- *"¿Cómo muevo el cursor a una posición específica en consola con gotoxy?"*
- *"Ayúdame a crear una función que imprima tablas formateadas en la terminal."*
- *"¿Cómo oculto y muestro el cursor del terminal en Python?"*
- *"¿Cómo creo menús interactivos con colores en consola usando Python puro?"*

### Documentación
- *"Genera un README completo para mi proyecto Python con estructura MVC y POO."*
- *"Realiza el README completo con carátula, integrantes, objetivo del proyecto, link del repositorio e incluye todos los prompts que hemos utilizado."*
- *"Pídele a la IA que te genere un PDF colorido del README."*

---

## Cómo Ejecutar

```bash
cd sistema_permisos_2
python main.py
```

> Requiere **Python 3.8 o superior**. No tiene dependencias externas — utiliza únicamente la biblioteca estándar de Python.

---

<div align="center">

Desarrollado con dedicación por el equipo  •  Programación Orientada a Objetos  •  2026

</div>
