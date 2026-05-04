# Sistema de Registro de Permisos del Personal

Sistema de gestión de permisos laborales desarrollado en Python con una arquitectura de **mini-framework** que aplica los pilares de la **Programación Orientada a Objetos (POO)**.

---

## Estructura del Proyecto

```
permisos_personal/
├── core/
│   ├── base.py           → Clases abstractas CRUD
│   ├── decoradores.py    → Decoradores y funciones de orden superior
│   └── mixins.py         → Mixins reutilizables (Logger, Validation)
├── models/
│   ├── entidades.py      → Modelos de dominio (Empleado, TipoPermiso, Permiso)
│   └── repositorios.py   → Repositorios concretos por entidad
├── controllers/
│   ├── empleado_controller.py  → Lógica de negocio de Empleados
│   └── permiso_controller.py  → Lógica de negocio de Permisos
├── views/
│   └── consola.py        → Interfaz de usuario por consola
├── utils/
│   └── funciones.py      → Funciones de utilidad y cálculos
└── main.py               → Punto de entrada del sistema
```

---

## Arquitectura: Patrón MVC

El proyecto sigue el patrón **Modelo-Vista-Controlador**:

| Capa | Carpeta | Responsabilidad |
|---|---|---|
| Modelo | `models/` | Datos y persistencia en memoria |
| Vista | `views/` | Presentación en consola con colores ANSI |
| Controlador | `controllers/` | Lógica de negocio y validaciones |
| Core | `core/` | Base del mini-framework (abstractas, mixins, decoradores) |
| Utils | `utils/` | Funciones de orden superior y cálculos |

---

## POO: Pilares Aplicados en el Proyecto

### 1. Abstracción — `core/base.py`

La abstracción se aplica mediante la clase abstracta `CRUDBase`, que define **qué operaciones deben existir** sin especificar **cómo** se implementan. Utiliza el módulo `abc` de Python.

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

`CRUDBase` establece el **contrato** que toda clase de repositorio debe cumplir. Ningún repositorio puede ser instanciado sin implementar estos 5 métodos.

La clase `Repositorio` hereda de `CRUDBase` y provee una **implementación genérica** de persistencia en memoria usando un diccionario interno (`_almacen`).

---

### 2. Herencia — Cadena de herencia completa

El proyecto tiene una cadena de herencia de tres niveles:

```
CRUDBase (abstracta)
    └── Repositorio (implementación base)
            ├── EmpleadoRepositorio
            ├── TipoPermisoRepositorio
            └── PermisoRepositorio
```

Los repositorios concretos heredan todo el CRUD de `Repositorio` y solo agregan **métodos de búsqueda específicos** del dominio:

- `EmpleadoRepositorio.buscar_por_cedula()` — Búsqueda por cédula
- `EmpleadoRepositorio.buscar_por_nombre()` — Búsqueda parcial por nombre
- `TipoPermisoRepositorio.obtener_remunerados()` — Filtro por tipo remunerado
- `PermisoRepositorio.obtener_por_empleado()` — Permisos de un empleado
- `PermisoRepositorio.obtener_por_rango_fechas()` — Filtro por rango de fechas

---

### 3. Encapsulamiento — Atributos y acceso controlado

El encapsulamiento se aplica en varias clases:

**En `Repositorio`:** los atributos internos son privados (convención `_`):
```python
self._almacen: Dict[int, Any] = {}
self._contador_id: int = 0
```

**En los controladores:** el repositorio se inyecta y se accede solo a través de métodos públicos:
```python
class EmpleadoController(LoggerMixin, ValidationMixin):
    def __init__(self, repositorio):
        self._repo = repositorio   # acceso privado
```

**En las entidades:** `TipoPermiso` usa una `@property` para encapsular la lógica de interpretación:
```python
@property
def es_remunerado(self) -> bool:
    return self.remunerado == "S"
```

**En `Permiso`:** la propiedad `duracion_dias` calcula el valor sin exponer la lógica directamente:
```python
@property
def duracion_dias(self) -> int:
    return (self.fecha_hasta - self.fecha_desde).days + 1
```

---

### 4. Polimorfismo — Herencia múltiple con Mixins

El polimorfismo se aplica a través de **herencia múltiple**. Los controladores combinan comportamientos de dos Mixins independientes:

```python
class EmpleadoController(LoggerMixin, ValidationMixin):
    ...

class PermisoController(LoggerMixin, ValidationMixin):
    ...
```

Ambos controladores usan los mismos métodos `log_info()`, `validar_no_vacio()`, `validar_fecha()`, etc., sin duplicar código. Python resuelve la herencia múltiple mediante el **MRO (Method Resolution Order)**.

Los Mixins llaman a `super().__init__()` cooperativamente para funcionar bien en herencia múltiple:
```python
class LoggerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_historial: list = []
```

---

## Descripción Detallada de Clases y Métodos

### `core/base.py`

#### `CRUDBase` (abstracta)
Define la interfaz CRUD estándar que todo repositorio debe implementar.

| Método | Descripción |
|---|---|
| `crear(datos)` | Crea y persiste una nueva entidad |
| `obtener_por_id(id)` | Retorna una entidad por ID o `None` |
| `obtener_todos()` | Retorna lista de todas las entidades |
| `actualizar(id, datos)` | Actualiza una entidad existente |
| `eliminar(id)` | Elimina una entidad, retorna `bool` |
| `contar()` | Método concreto: cuenta total de entidades |

#### `Repositorio` (implementación base)
Implementa `CRUDBase` usando un diccionario en memoria.

| Atributo/Método | Descripción |
|---|---|
| `_almacen` | Diccionario `{id: entidad}` de persistencia |
| `_contador_id` | Contador auto-incremental para IDs |
| `_generar_id()` | Genera un nuevo ID único |

---

### `core/mixins.py`

#### `LoggerMixin`
Agrega capacidad de logging con historial a cualquier clase.

| Método | Descripción |
|---|---|
| `log(nivel, mensaje)` | Registra con timestamp y nivel |
| `log_info(mensaje)` | Atajo para nivel INFO |
| `log_error(mensaje)` | Atajo para nivel ERROR |
| `log_advertencia(mensaje)` | Atajo para nivel ADVERTENCIA |
| `obtener_historial()` | Retorna copia del historial |
| `mostrar_historial()` | Imprime las últimas 20 entradas |

#### `ValidationMixin`
Provee métodos estáticos de validación reutilizables que lanzan `ValueError` con mensajes descriptivos.

| Método | Descripción |
|---|---|
| `validar_no_vacio(valor, campo)` | Valida string no vacío |
| `validar_numero_positivo(valor, campo)` | Valida número > 0 |
| `validar_opcion(valor, opciones, campo)` | Valida que valor esté en lista permitida |
| `validar_fecha(fecha_str, campo)` | Convierte string a `datetime.date` (acepta DD/MM/YYYY y YYYY-MM-DD) |
| `validar_rango_fechas(inicio, fin)` | Valida que inicio ≤ fin |
| `validar_cedula_ecuatoriana(cedula)` | Implementa algoritmo Módulo 10 para validar cédulas ecuatorianas |

##### Algoritmo Módulo 10 (validación de cédula):
1. Exactamente 10 dígitos
2. Primeros 2 dígitos = provincia (01–24)
3. Tercer dígito < 6 (persona natural)
4. Multiplica dígitos 1–9 por coeficientes `[2,1,2,1,2,1,2,1,2]`; si producto ≥ 10, resta 9
5. Suma todos los productos; dígito verificador = `(10 - suma % 10) % 10`
6. Compara con el dígito 10 de la cédula

---

### `core/decoradores.py`

Los decoradores son funciones que **envuelven** a otras funciones, añadiendo comportamiento antes/después sin modificar el código original.

| Decorador | Tipo | Descripción |
|---|---|---|
| `@manejar_errores` | Simple | Captura `ValueError` y `Exception`, imprime mensaje amigable |
| `@registrar_accion(desc)` | Fábrica | Registra en el log la ejecución con timestamp |
| `@validar_id_positivo` | Simple | Valida que el primer argumento sea entero positivo |
| `@confirmar_operacion(msg)` | Fábrica | Solicita confirmación `s/n` antes de ejecutar |
| `@cronometrar` | Simple | Mide tiempo de ejecución (muestra si > 0.5s) |

**Función `entrada_requerida(prompt, tipo, validador)`:** función de orden superior que repite la solicitud de entrada hasta obtener un valor válido del tipo especificado.

#### Ejemplo de apilamiento de decoradores:
```python
@manejar_errores          # 1° captura excepciones
@registrar_accion(...)    # 2° registra en log
@validar_id_positivo      # 3° valida el ID
def eliminar(self, id_empleado):
    ...
```
Los decoradores se aplican de abajo hacia arriba en la pila.

---

### `models/entidades.py`

Modelos de datos del dominio (equivalentes a entidades de base de datos).

#### `Empleado`
| Atributo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Asignado automáticamente por el repositorio |
| `nombre` | `str` | Nombre completo |
| `cedula` | `str` | Cédula validada con Módulo 10 |
| `sueldo` | `float` | Sueldo mensual |
| `valor_hora` | `float` | Calculado: `sueldo / 240` |

Métodos: `to_dict()`, `__str__()`, `__repr__()`

#### `TipoPermiso`
| Atributo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Auto-asignado |
| `descripcion` | `str` | Nombre del tipo (ej: "Enfermedad") |
| `remunerado` | `str` | `'S'` o `'N'` |
| `es_remunerado` | `@property bool` | Computed: `remunerado == "S"` |

#### `Permiso`
| Atributo | Tipo | Descripción |
|---|---|---|
| `id_empleado` | `int` | FK al empleado |
| `id_tipo_permiso` | `int` | FK al tipo de permiso |
| `fecha_desde` | `date` | Inicio del permiso |
| `fecha_hasta` | `date` | Fin del permiso |
| `tipo` | `str` | `'D'` (días) o `'H'` (horas) |
| `tiempo` | `float` | Cantidad de días u horas |
| `descuento` | `float` | Calculado por el controlador |
| `duracion_dias` | `@property int` | Diferencia calendario entre fechas |

---

### `models/repositorios.py`

Repositorios concretos que extienden `Repositorio` con búsquedas específicas.

#### `EmpleadoRepositorio`
| Método | Descripción |
|---|---|
| `buscar_por_cedula(cedula)` | Búsqueda exacta por cédula |
| `buscar_por_nombre(nombre)` | Búsqueda parcial case-insensitive |
| `cedula_existe(cedula, excluir_id)` | Verifica duplicados (con soporte para update) |

#### `TipoPermisoRepositorio`
| Método | Descripción |
|---|---|
| `buscar_por_descripcion(texto)` | Búsqueda parcial en descripción |
| `obtener_remunerados()` | Filtro: solo remunerados |
| `obtener_no_remunerados()` | Filtro: solo no remunerados |

#### `PermisoRepositorio`
| Método | Descripción |
|---|---|
| `obtener_por_empleado(id_empleado)` | Todos los permisos de un empleado |
| `obtener_por_tipo_permiso(id_tipo)` | Permisos de un tipo específico |
| `obtener_por_rango_fechas(inicio, fin)` | Permisos dentro de un rango de fechas |
| `obtener_por_tipo(tipo)` | Filtro por `'D'` o `'H'` |

Todos usan `filter()` con funciones lambda sobre la colección en memoria.

---

### `controllers/empleado_controller.py`

#### `EmpleadoController(LoggerMixin, ValidationMixin)`
Orquesta la lógica de negocio para la gestión de empleados.

| Método | Decoradores | Descripción |
|---|---|---|
| `registrar(nombre, cedula, sueldo_str)` | `@manejar_errores`, `@registrar_accion` | Valida y crea un empleado |
| `obtener(id_empleado)` | `@manejar_errores`, `@validar_id_positivo` | Obtiene empleado por ID |
| `listar_todos()` | — | Lista todos los empleados |
| `actualizar(id, nombre, cedula, sueldo_str)` | Los tres decoradores | Actualiza campos no-nulos |
| `eliminar(id_empleado)` | Los tres decoradores | Elimina un empleado |
| `buscar_por_cedula(cedula)` | — | Delegación al repositorio |
| `buscar_por_nombre(nombre)` | — | Delegación al repositorio |
| `total()` | — | Cuenta total de empleados |

---

### `controllers/permiso_controller.py`

#### `TipoPermisoController(LoggerMixin, ValidationMixin)`
Gestiona tipos/categorías de permisos. Misma estructura que `EmpleadoController`.

#### `PermisoController(LoggerMixin, ValidationMixin)`
El controlador más complejo: orquesta validaciones **cruzadas** entre tres entidades y calcula descuentos.

El constructor recibe los **tres repositorios** como dependencias (inyección de dependencias):
```python
def __init__(self, repo_permisos, repo_empleados, repo_tipos):
    self._repo = repo_permisos
    self._repo_emp = repo_empleados
    self._repo_tipos = repo_tipos
```

| Método | Descripción |
|---|---|
| `registrar(...)` | Valida empleado, tipo permiso, fechas, tipo y tiempo; calcula descuento |
| `obtener(id)` | Busca permiso por ID |
| `actualizar(id, ...)` | Actualiza y recalcula descuento |
| `eliminar(id)` | Elimina permiso |
| `obtener_por_empleado(id)` | Permisos de un empleado |

---

### `utils/funciones.py`

Funciones puras que aplican programación funcional con `map`, `filter` y `reduce`.

#### `calcular_descuento(empleado, permiso, tipo_permiso)`
Reglas de negocio para el cálculo de descuento:

| Condición | Fórmula |
|---|---|
| Permiso remunerado | `descuento = 0` |
| Tipo `'H'` (horas), no remunerado | `descuento = valor_hora × tiempo` |
| Tipo `'D'` (días), no remunerado | `descuento = (sueldo / 30) × tiempo` |

#### `calcular_estadisticas_permisos(permisos, empleados, tipos_permiso)`
Calcula métricas completas usando exclusivamente funciones de orden superior:
- `map()` para transformar colecciones
- `filter()` para filtrar subconjuntos
- `reduce()` para acumular totales

Retorna un diccionario con: total empleados, total permisos, permisos por tipo, tiempos totales, total descuentos, sueldo promedio y empleado con más permisos.

#### Funciones auxiliares
| Función | Descripción |
|---|---|
| `aplicar_a_lista(col, fn)` | Wrapper de `map()` |
| `filtrar_lista(col, fn)` | Wrapper de `filter()` |
| `acumular(col, fn, inicial)` | Wrapper de `reduce()` |
| `formatear_fecha(fecha)` | Convierte `date` a `DD/MM/YYYY` |
| `calcular_dias_habiles(inicio, fin)` | Cuenta días de lunes a viernes |

---

### `views/consola.py`

Capa de presentación completa con colores ANSI.

#### `C` (clase de constantes)
Centraliza todos los códigos de escape ANSI: colores de texto, colores de fondo, estilos (negrita, subrayado) y alias semánticos (`C.EXITO`, `C.ERROR`, `C.TITULO`, etc.).

#### Funciones de posicionamiento
| Función | Descripción |
|---|---|
| `gotoxy(x, y)` | Mueve cursor a posición (x, y) |
| `ocultar_cursor()` | Oculta el cursor de la terminal |
| `mostrar_cursor()` | Muestra el cursor |
| `guardar_cursor()` / `restaurar_cursor()` | Guarda y restaura posición |

#### Funciones de presentación
| Función | Descripción |
|---|---|
| `imprimir_titulo(titulo, subtitulo)` | Encabezado con línea doble |
| `imprimir_exito/error/advertencia/info(msg)` | Mensajes con icono y color |
| `solicitar_entrada(prompt, obligatorio)` | Input coloreado con reintento |
| `solicitar_confirmacion(msg)` | Confirmación `s/n` |

#### Funciones de tabla
| Función | Descripción |
|---|---|
| `tabla_empleados(empleados)` | Tabla con ID, nombre, cédula, sueldo, valor/hora |
| `tabla_tipos_permiso(tipos)` | Tabla con ID, descripción, indicador remunerado |
| `tabla_permisos(permisos, empleados, tipos)` | Tabla con nombres resueltos y descuento en color |
| `ficha_empleado(empleado)` | Ficha detallada de un empleado |
| `ficha_permiso(permiso, empleado, tipo)` | Ficha detallada de un permiso con cálculo |
| `panel_estadisticas(stats, empleado_mas)` | Panel completo de métricas |

---

### `main.py`

Punto de entrada. Instancia los repositorios y controladores, carga datos de muestra y lanza el menú interactivo.

```python
repo_empleados  = EmpleadoRepositorio()
repo_tipos      = TipoPermisoRepositorio()
repo_permisos   = PermisoRepositorio()

ctrl_empleados  = EmpleadoController(repo_empleados)
ctrl_tipos      = TipoPermisoController(repo_tipos)
ctrl_permisos   = PermisoController(repo_permisos, repo_empleados, repo_tipos)
```

Módulos del menú:
- `modulo_empleados()` — CRUD completo de empleados
- `modulo_tipos_permiso()` — CRUD de tipos de permiso
- `modulo_permisos()` — CRUD de permisos con cálculo de descuento
- `modulo_estadisticas()` — Panel de métricas
- `modulo_historial()` — Log de acciones de todos los controladores

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

## Conceptos POO Adicionales Aplicados

| Concepto | Dónde | Cómo |
|---|---|---|
| **Clases abstractas** | `CRUDBase` | `ABC` + `@abstractmethod` |
| **Herencia múltiple** | Controladores | `(LoggerMixin, ValidationMixin)` |
| **Propiedades** | `TipoPermiso`, `Permiso` | `@property` |
| **Métodos estáticos** | `ValidationMixin` | `@staticmethod` |
| **Inyección de dependencias** | `PermisoController` | Repositorios como parámetros |
| **Decoradores de función** | `core/decoradores.py` | `functools.wraps` |
| **Funciones de orden superior** | `utils/funciones.py` | `map`, `filter`, `reduce`, lambdas |
| **Dunder methods** | Entidades | `__str__`, `__repr__` |
| **Type hints** | Todo el proyecto | `List`, `Optional`, `Dict`, `Any` |

---

## Cómo ejecutar

```bash
cd permisos_personal
python main.py
```

Requiere Python 3.8 o superior. No tiene dependencias externas.
