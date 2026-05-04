import functools
import datetime
from typing import Callable, Any


def manejar_errores(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            print(f"\n  ⚠  Validación: {ve}")
            return None
        except KeyboardInterrupt:
            print("\n\n  Operación cancelada por el usuario.")
            return None
        except Exception as e:
            print(f"\n  ✗  Error inesperado en '{func.__name__}': {e}")
            return None
    return wrapper


def registrar_accion(descripcion: str = "") -> Callable:
    def decorador(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre = descripcion or func.__name__
            instancia = args[0] if args else None
            if hasattr(instancia, 'log_info'):
                instancia.log_info(f"Ejecutando: {nombre}")
            resultado = func(*args, **kwargs)
            if resultado is not None and hasattr(instancia, 'log_info'):
                instancia.log_info(f"Completado: {nombre} [{timestamp}]")
            return resultado
        return wrapper
    return decorador


def validar_id_positivo(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(self, id_entidad, *args, **kwargs) -> Any:
        try:
            id_val = int(id_entidad)
            if id_val <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            print(f"\n  ⚠  El ID debe ser un número entero positivo. Se recibió: '{id_entidad}'")
            return None
        return func(self, id_val, *args, **kwargs)
    return wrapper


def confirmar_operacion(mensaje: str = "¿Confirma la operación?") -> Callable:
    def decorador(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            respuesta = input(f"\n  {mensaje} (s/n): ").strip().lower()
            if respuesta == 's':
                return func(*args, **kwargs)
            else:
                print("  Operación cancelada.")
                return None
        return wrapper
    return decorador


def cronometrar(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        inicio = datetime.datetime.now()
        resultado = func(*args, **kwargs)
        fin = datetime.datetime.now()
        duracion = (fin - inicio).total_seconds()
        if duracion > 0.5:
            print(f"  [⏱] '{func.__name__}' tardó {duracion:.3f}s")
        return resultado
    return wrapper


def entrada_requerida(prompt: str, tipo=str, validador: Callable = None) -> Any:
    while True:
        try:
            valor_raw = input(f"  {prompt}").strip()
            if not valor_raw:
                raise ValueError("Este campo es obligatorio.")
            valor = tipo(valor_raw)
            if validador:
                valor = validador(valor)
            return valor
        except ValueError as e:
            print(f"    ⚠  {e} Intente nuevamente.")
        except KeyboardInterrupt:
            print("\n  Entrada cancelada.")
            raise
