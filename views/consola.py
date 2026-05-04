import os
import sys
import datetime
from typing import List, Any


def _habilitar_ansi_windows() -> None:
    if os.name == "nt":
        try:
            import ctypes
            kernel = ctypes.windll.kernel32
            handle = kernel.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel.GetConsoleMode(handle, ctypes.byref(mode))
            kernel.SetConsoleMode(handle, mode.value | 0x0004)
        except Exception:
            pass

_habilitar_ansi_windows()


class C:
    RESET       = "\033[0m"
    NEGRITA     = "\033[1m"
    DIM         = "\033[2m"
    SUBRAYADO   = "\033[4m"
    NEGRO       = "\033[30m"
    ROJO        = "\033[31m"
    VERDE       = "\033[32m"
    AMARILLO    = "\033[33m"
    AZUL        = "\033[34m"
    MAGENTA     = "\033[35m"
    CYAN        = "\033[36m"
    BLANCO      = "\033[37m"
    ROJO_B      = "\033[91m"
    VERDE_B     = "\033[92m"
    AMARILLO_B  = "\033[93m"
    AZUL_B      = "\033[94m"
    MAGENTA_B   = "\033[95m"
    CYAN_B      = "\033[96m"
    BLANCO_B    = "\033[97m"
    BG_NEGRO    = "\033[40m"
    BG_ROJO     = "\033[41m"
    BG_VERDE    = "\033[42m"
    BG_AZUL     = "\033[44m"
    BG_CYAN     = "\033[46m"
    BG_BLANCO   = "\033[47m"
    TITULO      = NEGRITA + CYAN_B
    SUBTITULO   = NEGRITA + AZUL_B
    EXITO       = NEGRITA + VERDE_B
    ERROR       = NEGRITA + ROJO_B
    ADVERTENCIA = NEGRITA + AMARILLO_B
    INFO        = CYAN
    PROMPT      = AMARILLO
    TABLA_HDR   = NEGRITA + AZUL_B
    TABLA_ALT   = DIM
    DATO        = BLANCO_B
    ACENTO      = MAGENTA_B


def color(texto: str, *estilos: str) -> str:
    return "".join(estilos) + texto + C.RESET


def gotoxy(x: int, y: int) -> None:
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()


def ocultar_cursor() -> None:
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()


def mostrar_cursor() -> None:
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()


def guardar_cursor() -> None:
    sys.stdout.write("\033[s")
    sys.stdout.flush()


def restaurar_cursor() -> None:
    sys.stdout.write("\033[u")
    sys.stdout.flush()


LINEA_SIMPLE = "─" * 68
LINEA_DOBLE  = "═" * 68
LINEA_TITULO = "━" * 68

HEADER_SISTEMA = (
    color("\n╔══════════════════════════════════════════════════════════════════════╗", C.TITULO) + "\n" +
    color("║        SISTEMA DE REGISTRO DE PERMISOS DEL PERSONAL                 ║", C.TITULO) + "\n" +
    color("║        Mini-Framework Python · POO · Módulo 10 · v2.0               ║", C.TITULO) + "\n" +
    color("╚══════════════════════════════════════════════════════════════════════╝", C.TITULO)
)


def limpiar_pantalla() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def imprimir_titulo(titulo: str, subtitulo: str = "") -> None:
    print(color(f"\n{LINEA_DOBLE}", C.TITULO))
    print(color(f"  {titulo.upper()}", C.TITULO))
    if subtitulo:
        print(color(f"  {subtitulo}", C.SUBTITULO))
    print(color(f"{LINEA_DOBLE}", C.TITULO))


def imprimir_seccion(titulo: str) -> None:
    print(color(f"\n  {LINEA_SIMPLE}", C.SUBTITULO))
    print(color(f"  {titulo}", C.SUBTITULO))
    print(color(f"  {LINEA_SIMPLE}", C.SUBTITULO))


def imprimir_exito(mensaje: str) -> None:
    print(color(f"\n  ✔  {mensaje}", C.EXITO))


def imprimir_error(mensaje: str) -> None:
    print(color(f"\n  ✗  {mensaje}", C.ERROR))


def imprimir_advertencia(mensaje: str) -> None:
    print(color(f"\n  ⚠  {mensaje}", C.ADVERTENCIA))


def imprimir_info(mensaje: str) -> None:
    print(color(f"\n  ℹ  {mensaje}", C.INFO))


def pausar(mensaje: str = "\n  Presione ENTER para continuar...") -> None:
    input(color(mensaje, C.DIM))


def solicitar_entrada(prompt: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(color(f"  {prompt}", C.PROMPT)).strip()
        if obligatorio and not valor:
            print(color("    ⚠  Este campo es obligatorio. Intente nuevamente.", C.ADVERTENCIA))
            continue
        return valor


def solicitar_confirmacion(mensaje: str = "¿Confirma?") -> bool:
    respuesta = input(color(f"\n  {mensaje} (s/n): ", C.ADVERTENCIA)).strip().lower()
    return respuesta == "s"


def tabla_empleados(empleados: list) -> None:
    if not empleados:
        imprimir_advertencia("No hay empleados registrados.")
        return

    print(color(
        f"\n  {'ID':<5} {'Nombre':<28} {'Cédula':<13} {'Sueldo':>10} {'Valor/Hora':>12}",
        C.TABLA_HDR
    ))
    print(color(f"  {LINEA_SIMPLE}", C.TABLA_HDR))

    for i, emp in enumerate(empleados):
        estilo = C.RESET if i % 2 == 0 else C.TABLA_ALT
        print(
            color(
                f"  {emp.id:<5} {emp.nombre:<28} {emp.cedula:<13} "
                f"${emp.sueldo:>9.2f} ${emp.valor_hora:>11.4f}",
                estilo
            )
        )

    print(color(f"  {LINEA_SIMPLE}", C.TABLA_HDR))
    print(color(f"  Total: {len(empleados)} empleado(s)", C.INFO))


def tabla_tipos_permiso(tipos: list) -> None:
    if not tipos:
        imprimir_advertencia("No hay tipos de permiso registrados.")
        return

    print(color(
        f"\n  {'ID':<5} {'Descripción':<35} {'Remunerado':<12}",
        C.TABLA_HDR
    ))
    print(color(f"  {LINEA_SIMPLE}", C.TABLA_HDR))

    for i, tp in enumerate(tipos):
        estilo = C.RESET if i % 2 == 0 else C.TABLA_ALT
        rem = color("✔ Sí", C.EXITO) if tp.es_remunerado else color("✗ No", C.ERROR)
        print(color(f"  {tp.id:<5} {tp.descripcion:<35} ", estilo) + rem)

    print(color(f"  {LINEA_SIMPLE}", C.TABLA_HDR))
    print(color(f"  Total: {len(tipos)} tipo(s)", C.INFO))


def tabla_permisos(permisos: list, empleados: list, tipos: list) -> None:
    if not permisos:
        imprimir_advertencia("No hay permisos registrados.")
        return

    emp_idx = {e.id: e for e in empleados}
    tip_idx = {t.id: t for t in tipos}

    print(color(
        f"\n  {'ID':<5} {'Empleado':<22} {'Tipo Permiso':<20} "
        f"{'Desde':<12} {'Hasta':<12} {'T':<3} {'Tiempo':>6} {'Descuento':>10}",
        C.TABLA_HDR
    ))
    print(color(f"  {'─'*97}", C.TABLA_HDR))

    for i, p in enumerate(permisos):
        emp_nombre = emp_idx.get(p.id_empleado,  type('', (), {'nombre': '?'})()).nombre
        tip_desc   = tip_idx.get(p.id_tipo_permiso, type('', (), {'descripcion': '?'})()).descripcion
        estilo     = C.RESET if i % 2 == 0 else C.TABLA_ALT

        desc_str = f"${p.descuento:>9.2f}"
        desc_col = color(desc_str, C.ROJO_B) if p.descuento > 0 else color(desc_str, C.VERDE_B)

        print(
            color(
                f"  {p.id:<5} {emp_nombre[:21]:<22} {tip_desc[:19]:<20} "
                f"{str(p.fecha_desde):<12} {str(p.fecha_hasta):<12} "
                f"{p.tipo:<3} {p.tiempo:>6.1f} ",
                estilo
            ) + desc_col
        )

    print(color(f"  {'─'*97}", C.TABLA_HDR))
    print(color(f"  Total: {len(permisos)} permiso(s)", C.INFO))


def ficha_empleado(empleado) -> None:
    imprimir_seccion("FICHA DEL EMPLEADO")
    etq = C.ACENTO + C.NEGRITA
    val = C.BLANCO_B
    print(color("  ID          : ", etq) + color(str(empleado.id),          val))
    print(color("  Nombre      : ", etq) + color(empleado.nombre,           val))
    print(color("  Cédula      : ", etq) + color(empleado.cedula,           val))
    print(color("  Sueldo      : ", etq) + color(f"${empleado.sueldo:,.2f}", C.VERDE_B))
    print(color("  Valor/Hora  : ", etq) + color(f"${empleado.valor_hora:.4f}", C.VERDE_B))


def ficha_permiso(permiso, empleado=None, tipo_permiso=None) -> None:
    imprimir_seccion("RESUMEN DEL PERMISO")
    etq = C.ACENTO + C.NEGRITA
    val = C.BLANCO_B

    print(color("  ID Permiso      : ", etq) + color(str(permiso.id), val))

    if empleado:
        print(color("  Empleado        : ", etq) +
              color(f"[{empleado.id}] {empleado.nombre}", val))
        print(color("  Sueldo          : ", etq) +
              color(f"${empleado.sueldo:,.2f}", C.VERDE_B))
        print(color("  Valor/Hora      : ", etq) +
              color(f"${empleado.valor_hora:.4f}", C.VERDE_B))

    if tipo_permiso:
        rem_txt = color("Sí (Remunerado)", C.EXITO) if tipo_permiso.es_remunerado else color("No (No Remunerado)", C.ERROR)
        print(color("  Tipo de Permiso : ", etq) +
              color(f"[{tipo_permiso.id}] {tipo_permiso.descripcion} — ", val) + rem_txt)

    print(color("  Fecha Desde     : ", etq) +
          color(permiso.fecha_desde.strftime("%d/%m/%Y"), val))
    print(color("  Fecha Hasta     : ", etq) +
          color(permiso.fecha_hasta.strftime("%d/%m/%Y"), val))
    print(color("  Días calendario : ", etq) +
          color(f"{permiso.duracion_dias} día(s)", val))

    tipo_label = "Días" if permiso.tipo == "D" else "Horas"
    print(color("  Tipo / Tiempo   : ", etq) +
          color(f"{tipo_label} / {permiso.tiempo}", val))

    if permiso.descuento > 0:
        print(color(f"  ⚠  DESCUENTO    : ${permiso.descuento:.2f}", C.ERROR))
    else:
        print(color("  ✔  Descuento    : $0.00 (permiso remunerado)", C.EXITO))


def panel_estadisticas(stats: dict, empleado_mas: tuple) -> None:
    imprimir_titulo("ESTADÍSTICAS DEL SISTEMA", "Calculado con funciones de orden superior")

    print(color(f"\n  {'INDICADOR':<40} {'VALOR':>15}", C.TABLA_HDR))
    print(color(f"  {LINEA_SIMPLE}", C.TABLA_HDR))

    filas = [
        ("Total de empleados registrados",   str(stats["total_empleados"])),
        ("Total de permisos registrados",    str(stats["total_permisos"])),
        ("Permisos remunerados",             str(stats["permisos_remunerados"])),
        ("Permisos no remunerados",          str(stats["permisos_no_remunerados"])),
        ("Total tiempo solicitado (días)",   f"{stats['total_tiempo_dias']:.1f}d"),
        ("Total tiempo solicitado (horas)",  f"{stats['total_tiempo_horas']:.1f}h"),
        ("Total descuentos aplicados",       f"${stats['total_descuentos']:.2f}"),
        ("Sueldo promedio empleados",        f"${stats['sueldo_promedio']:.2f}"),
    ]

    for i, (indicador, valor) in enumerate(filas):
        estilo = C.RESET if i % 2 == 0 else C.TABLA_ALT
        print(
            color(f"  {indicador:<40} ", estilo) +
            color(f"{valor:>15}", C.DATO)
        )

    print(color(f"\n  {'─'*55}", C.SUBTITULO))
    emp, qty = empleado_mas
    if emp:
        print(
            color("  ★  Empleado con más permisos: ", C.ACENTO + C.NEGRITA) +
            color(f"[{emp.id}] {emp.nombre} ({qty} permiso(s))", C.BLANCO_B)
        )
    else:
        print(color("  ★  Empleado con más permisos: N/A", C.DIM))

    print(color(f"  {LINEA_SIMPLE}", C.TITULO))


def _opcion_menu(num: str, texto: str) -> str:
    return color(f"  [{num}]", C.ACENTO + C.NEGRITA) + color(f"  {texto}", C.BLANCO_B)


def mostrar_menu_principal() -> str:
    print(HEADER_SISTEMA)
    print(color(f"\n  {LINEA_SIMPLE}", C.TITULO))
    print(color("  MENÚ PRINCIPAL", C.TITULO))
    print(color(f"  {LINEA_SIMPLE}", C.TITULO))
    print(_opcion_menu("1", "Gestión de Empleados"))
    print(_opcion_menu("2", "Gestión de Tipos de Permiso"))
    print(_opcion_menu("3", "Gestión de Permisos"))
    print(_opcion_menu("4", "Estadísticas del Sistema"))
    print(_opcion_menu("5", "Historial de Acciones"))
    print(_opcion_menu("0", "Salir del Sistema"))
    print(color(f"  {LINEA_SIMPLE}", C.TITULO))
    return input(color("  Seleccione una opción: ", C.PROMPT)).strip()


def mostrar_menu_empleados() -> str:
    imprimir_titulo("GESTIÓN DE EMPLEADOS")
    print(_opcion_menu("1", "Registrar nuevo empleado"))
    print(_opcion_menu("2", "Listar todos los empleados"))
    print(_opcion_menu("3", "Buscar empleado por ID"))
    print(_opcion_menu("4", "Buscar empleado por nombre"))
    print(_opcion_menu("5", "Buscar empleado por cédula"))
    print(_opcion_menu("6", "Actualizar empleado"))
    print(_opcion_menu("7", "Eliminar empleado"))
    print(_opcion_menu("0", "Volver al menú principal"))
    print(color(f"  {LINEA_SIMPLE}", C.TITULO))
    return input(color("  Seleccione una opción: ", C.PROMPT)).strip()


def mostrar_menu_tipos() -> str:
    imprimir_titulo("GESTIÓN DE TIPOS DE PERMISO")
    print(_opcion_menu("1", "Registrar nuevo tipo de permiso"))
    print(_opcion_menu("2", "Listar todos los tipos"))
    print(_opcion_menu("3", "Buscar tipo por ID"))
    print(_opcion_menu("4", "Actualizar tipo de permiso"))
    print(_opcion_menu("5", "Eliminar tipo de permiso"))
    print(_opcion_menu("0", "Volver al menú principal"))
    print(color(f"  {LINEA_SIMPLE}", C.TITULO))
    return input(color("  Seleccione una opción: ", C.PROMPT)).strip()


def mostrar_menu_permisos() -> str:
    imprimir_titulo("GESTIÓN DE PERMISOS")
    print(_opcion_menu("1", "Registrar nuevo permiso"))
    print(_opcion_menu("2", "Listar todos los permisos"))
    print(_opcion_menu("3", "Buscar permiso por ID"))
    print(_opcion_menu("4", "Listar permisos por empleado"))
    print(_opcion_menu("5", "Actualizar permiso"))
    print(_opcion_menu("6", "Eliminar permiso"))
    print(_opcion_menu("0", "Volver al menú principal"))
    print(color(f"  {LINEA_SIMPLE}", C.TITULO))
    return input(color("  Seleccione una opción: ", C.PROMPT)).strip()
