import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.repositorios import EmpleadoRepositorio, TipoPermisoRepositorio, PermisoRepositorio
from controllers.empleado_controller import EmpleadoController
from controllers.permiso_controller import TipoPermisoController, PermisoController
from utils.funciones import calcular_estadisticas_permisos
from views.consola import (
    limpiar_pantalla, imprimir_titulo, imprimir_seccion,
    imprimir_exito, imprimir_error, imprimir_advertencia, imprimir_info,
    pausar, solicitar_entrada, solicitar_confirmacion,
    tabla_empleados, tabla_tipos_permiso, tabla_permisos,
    ficha_empleado, ficha_permiso, panel_estadisticas,
    mostrar_menu_principal, mostrar_menu_empleados,
    mostrar_menu_tipos, mostrar_menu_permisos,
    LINEA_SIMPLE,
)

repo_empleados  = EmpleadoRepositorio()
repo_tipos      = TipoPermisoRepositorio()
repo_permisos   = PermisoRepositorio()

ctrl_empleados  = EmpleadoController(repo_empleados)
ctrl_tipos      = TipoPermisoController(repo_tipos)
ctrl_permisos   = PermisoController(repo_permisos, repo_empleados, repo_tipos)


def cargar_datos_muestra() -> None:
    ctrl_empleados.registrar("Ana María Torres Vega",     "1710034065", "1500.00")
    ctrl_empleados.registrar("Carlos Eduardo Mora Lema",  "0926687856", "2200.00")
    ctrl_empleados.registrar("Lucía Fernanda Soto Navas", "1312539784", "1800.00")

    ctrl_tipos.registrar("Enfermedad / Salud",             "S")
    ctrl_tipos.registrar("Calamidad Doméstica",            "S")
    ctrl_tipos.registrar("Permiso Personal sin Sueldo",    "N")
    ctrl_tipos.registrar("Maternidad / Paternidad",        "S")
    ctrl_tipos.registrar("Estudios / Capacitación",        "N")

    ctrl_permisos.registrar("1", "1", "2025-01-10", "2025-01-12", "D", "3")
    ctrl_permisos.registrar("2", "3", "2025-02-05", "2025-02-05", "H", "4")
    ctrl_permisos.registrar("3", "2", "2025-03-15", "2025-03-16", "D", "2")
    ctrl_permisos.registrar("1", "5", "2025-04-01", "2025-04-03", "D", "3")


def modulo_empleados() -> None:
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_empleados()

        if opcion == "1":
            imprimir_titulo("REGISTRAR NUEVO EMPLEADO")
            nombre  = solicitar_entrada("Nombre completo    : ")
            cedula  = solicitar_entrada("Número de cédula   : ")
            sueldo  = solicitar_entrada("Sueldo mensual ($) : ")

            empleado = ctrl_empleados.registrar(nombre, cedula, sueldo)
            if empleado:
                imprimir_exito("Empleado registrado exitosamente.")
                ficha_empleado(empleado)

        elif opcion == "2":
            imprimir_titulo("LISTADO DE EMPLEADOS")
            tabla_empleados(ctrl_empleados.listar_todos())

        elif opcion == "3":
            imprimir_titulo("BUSCAR EMPLEADO POR ID")
            id_str = solicitar_entrada("ID del empleado : ")
            try:
                empleado = ctrl_empleados.obtener(int(id_str))
                if empleado:
                    ficha_empleado(empleado)
            except (ValueError, TypeError):
                imprimir_error("ID inválido.")

        elif opcion == "4":
            imprimir_titulo("BUSCAR EMPLEADO POR NOMBRE")
            nombre = solicitar_entrada("Texto a buscar : ")
            resultados = ctrl_empleados.buscar_por_nombre(nombre)
            if resultados:
                tabla_empleados(resultados)
            else:
                imprimir_advertencia("No se encontraron empleados con ese nombre.")

        elif opcion == "5":
            imprimir_titulo("BUSCAR EMPLEADO POR CÉDULA")
            cedula = solicitar_entrada("Número de cédula : ")
            empleado = ctrl_empleados.buscar_por_cedula(cedula)
            if empleado:
                ficha_empleado(empleado)
            else:
                imprimir_advertencia("No se encontró ningún empleado con esa cédula.")

        elif opcion == "6":
            imprimir_titulo("ACTUALIZAR EMPLEADO")
            tabla_empleados(ctrl_empleados.listar_todos())
            id_str = solicitar_entrada("\n  ID del empleado a actualizar : ")

            try:
                emp = ctrl_empleados.obtener(int(id_str))
            except (ValueError, TypeError):
                emp = None

            if emp:
                imprimir_info("Deje vacío el campo si no desea modificarlo.")
                nuevo_nombre = solicitar_entrada(f"Nombre [{emp.nombre}]: ", obligatorio=False)
                nueva_cedula = solicitar_entrada(f"Cédula [{emp.cedula}]: ", obligatorio=False)
                nuevo_sueldo = solicitar_entrada(f"Sueldo [{emp.sueldo}]: ", obligatorio=False)

                actualizado = ctrl_empleados.actualizar(
                    int(id_str),
                    nombre     = nuevo_nombre  or None,
                    cedula     = nueva_cedula  or None,
                    sueldo_str = nuevo_sueldo  or None,
                )
                if actualizado:
                    imprimir_exito("Empleado actualizado correctamente.")
                    ficha_empleado(actualizado)

        elif opcion == "7":
            imprimir_titulo("ELIMINAR EMPLEADO")
            tabla_empleados(ctrl_empleados.listar_todos())
            id_str = solicitar_entrada("\n  ID del empleado a eliminar : ")

            try:
                emp = ctrl_empleados.obtener(int(id_str))
            except (ValueError, TypeError):
                emp = None

            if emp:
                ficha_empleado(emp)
                if solicitar_confirmacion(f"¿Eliminar al empleado '{emp.nombre}'?"):
                    resultado = ctrl_empleados.eliminar(int(id_str))
                    if resultado:
                        imprimir_exito(f"Empleado '{emp.nombre}' eliminado correctamente.")
                    else:
                        imprimir_error("No se pudo eliminar el empleado.")

        elif opcion == "0":
            break
        else:
            imprimir_advertencia("Opción no válida. Seleccione una opción del menú.")

        pausar()


def modulo_tipos_permiso() -> None:
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_tipos()

        if opcion == "1":
            imprimir_titulo("REGISTRAR TIPO DE PERMISO")
            descripcion = solicitar_entrada("Descripción         : ")
            remunerado  = solicitar_entrada("¿Remunerado? (S/N)  : ")

            tipo = ctrl_tipos.registrar(descripcion, remunerado)
            if tipo:
                imprimir_exito("Tipo de permiso registrado exitosamente.")
                print(f"\n  ID          : {tipo.id}")
                print(f"  Descripción : {tipo.descripcion}")
                print(f"  Remunerado  : {'Sí' if tipo.es_remunerado else 'No'}")

        elif opcion == "2":
            imprimir_titulo("LISTADO DE TIPOS DE PERMISO")
            tabla_tipos_permiso(ctrl_tipos.listar_todos())

        elif opcion == "3":
            imprimir_titulo("BUSCAR TIPO DE PERMISO POR ID")
            id_str = solicitar_entrada("ID del tipo : ")
            try:
                tipo = ctrl_tipos.obtener(int(id_str))
                if tipo:
                    print(f"\n  ID          : {tipo.id}")
                    print(f"  Descripción : {tipo.descripcion}")
                    print(f"  Remunerado  : {'Sí' if tipo.es_remunerado else 'No'}")
            except (ValueError, TypeError):
                imprimir_error("ID inválido.")

        elif opcion == "4":
            imprimir_titulo("ACTUALIZAR TIPO DE PERMISO")
            tabla_tipos_permiso(ctrl_tipos.listar_todos())
            id_str = solicitar_entrada("\n  ID del tipo a actualizar : ")

            try:
                tipo = ctrl_tipos.obtener(int(id_str))
            except (ValueError, TypeError):
                tipo = None

            if tipo:
                imprimir_info("Deje vacío el campo si no desea modificarlo.")
                nueva_desc = solicitar_entrada(f"Descripción [{tipo.descripcion}]: ", obligatorio=False)
                nuevo_rem  = solicitar_entrada(f"Remunerado [{tipo.remunerado}] (S/N): ", obligatorio=False)

                actualizado = ctrl_tipos.actualizar(
                    int(id_str),
                    descripcion    = nueva_desc or None,
                    remunerado_str = nuevo_rem  or None,
                )
                if actualizado:
                    imprimir_exito("Tipo de permiso actualizado correctamente.")

        elif opcion == "5":
            imprimir_titulo("ELIMINAR TIPO DE PERMISO")
            tabla_tipos_permiso(ctrl_tipos.listar_todos())
            id_str = solicitar_entrada("\n  ID del tipo a eliminar : ")

            try:
                tipo = ctrl_tipos.obtener(int(id_str))
            except (ValueError, TypeError):
                tipo = None

            if tipo:
                if solicitar_confirmacion(f"¿Eliminar '{tipo.descripcion}'?"):
                    resultado = ctrl_tipos.eliminar(int(id_str))
                    if resultado:
                        imprimir_exito("Tipo de permiso eliminado correctamente.")

        elif opcion == "0":
            break
        else:
            imprimir_advertencia("Opción no válida.")

        pausar()


def modulo_permisos() -> None:
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_permisos()

        if opcion == "1":
            imprimir_titulo("REGISTRAR PERMISO DEL PERSONAL")

            imprimir_seccion("EMPLEADOS DISPONIBLES")
            tabla_empleados(ctrl_empleados.listar_todos())

            imprimir_seccion("TIPOS DE PERMISO DISPONIBLES")
            tabla_tipos_permiso(ctrl_tipos.listar_todos())

            if not ctrl_empleados.listar_todos():
                imprimir_error("Debe registrar al menos un empleado primero.")
                pausar()
                continue

            if not ctrl_tipos.listar_todos():
                imprimir_error("Debe registrar al menos un tipo de permiso primero.")
                pausar()
                continue

            print()
            id_emp  = solicitar_entrada("ID del empleado          : ")
            id_tipo = solicitar_entrada("ID del tipo de permiso   : ")
            f_desde = solicitar_entrada("Fecha desde (DD/MM/YYYY) : ")
            f_hasta = solicitar_entrada("Fecha hasta (DD/MM/YYYY) : ")
            tipo    = solicitar_entrada("Tipo (D=Días / H=Horas)  : ")
            tiempo  = solicitar_entrada("Cantidad de tiempo       : ")

            permiso = ctrl_permisos.registrar(id_emp, id_tipo, f_desde, f_hasta, tipo, tiempo)
            if permiso:
                imprimir_exito("Permiso registrado exitosamente.")
                empleado     = ctrl_empleados.obtener(permiso.id_empleado)
                tipo_permiso = ctrl_tipos.obtener(permiso.id_tipo_permiso)
                ficha_permiso(permiso, empleado, tipo_permiso)

        elif opcion == "2":
            imprimir_titulo("LISTADO DE PERMISOS")
            tabla_permisos(
                ctrl_permisos.listar_todos(),
                ctrl_empleados.listar_todos(),
                ctrl_tipos.listar_todos(),
            )

        elif opcion == "3":
            imprimir_titulo("BUSCAR PERMISO POR ID")
            id_str = solicitar_entrada("ID del permiso : ")
            try:
                permiso = ctrl_permisos.obtener(int(id_str))
                if permiso:
                    empleado     = ctrl_empleados.obtener(permiso.id_empleado)
                    tipo_permiso = ctrl_tipos.obtener(permiso.id_tipo_permiso)
                    ficha_permiso(permiso, empleado, tipo_permiso)
            except (ValueError, TypeError):
                imprimir_error("ID inválido.")

        elif opcion == "4":
            imprimir_titulo("PERMISOS POR EMPLEADO")
            tabla_empleados(ctrl_empleados.listar_todos())
            id_str = solicitar_entrada("\n  ID del empleado : ")
            try:
                id_emp   = int(id_str)
                empleado = ctrl_empleados.obtener(id_emp)
                if empleado:
                    permisos = ctrl_permisos.obtener_por_empleado(id_emp)
                    imprimir_seccion(f"Permisos de: {empleado.nombre}")
                    tabla_permisos(permisos, [empleado], ctrl_tipos.listar_todos())
            except (ValueError, TypeError):
                imprimir_error("ID inválido.")

        elif opcion == "5":
            imprimir_titulo("ACTUALIZAR PERMISO")
            tabla_permisos(
                ctrl_permisos.listar_todos(),
                ctrl_empleados.listar_todos(),
                ctrl_tipos.listar_todos(),
            )
            id_str = solicitar_entrada("\n  ID del permiso a actualizar : ")
            try:
                permiso = ctrl_permisos.obtener(int(id_str))
            except (ValueError, TypeError):
                permiso = None

            if permiso:
                imprimir_info("Deje vacío el campo si no desea modificarlo.")
                nueva_fd = solicitar_entrada(f"Fecha desde [{permiso.fecha_desde}]: ", obligatorio=False)
                nueva_fh = solicitar_entrada(f"Fecha hasta [{permiso.fecha_hasta}]: ", obligatorio=False)
                nuevo_tp = solicitar_entrada(f"Tipo [{permiso.tipo}] (D/H): ", obligatorio=False)
                nuevo_t  = solicitar_entrada(f"Tiempo [{permiso.tiempo}]: ", obligatorio=False)

                actualizado = ctrl_permisos.actualizar(
                    int(id_str),
                    fecha_desde_str = nueva_fd or None,
                    fecha_hasta_str = nueva_fh or None,
                    tipo_str        = nuevo_tp or None,
                    tiempo_str      = nuevo_t  or None,
                )
                if actualizado:
                    imprimir_exito("Permiso actualizado correctamente.")
                    emp = ctrl_empleados.obtener(actualizado.id_empleado)
                    tip = ctrl_tipos.obtener(actualizado.id_tipo_permiso)
                    ficha_permiso(actualizado, emp, tip)

        elif opcion == "6":
            imprimir_titulo("ELIMINAR PERMISO")
            tabla_permisos(
                ctrl_permisos.listar_todos(),
                ctrl_empleados.listar_todos(),
                ctrl_tipos.listar_todos(),
            )
            id_str = solicitar_entrada("\n  ID del permiso a eliminar : ")
            try:
                permiso = ctrl_permisos.obtener(int(id_str))
            except (ValueError, TypeError):
                permiso = None

            if permiso:
                if solicitar_confirmacion(f"¿Eliminar permiso ID={permiso.id}?"):
                    resultado = ctrl_permisos.eliminar(int(id_str))
                    if resultado:
                        imprimir_exito("Permiso eliminado correctamente.")

        elif opcion == "0":
            break
        else:
            imprimir_advertencia("Opción no válida.")

        pausar()


def modulo_estadisticas() -> None:
    limpiar_pantalla()
    stats = calcular_estadisticas_permisos(
        ctrl_permisos.listar_todos(),
        ctrl_empleados.listar_todos(),
        ctrl_tipos.listar_todos(),
    )
    emp_mas = stats.pop("empleado_mas_permisos")
    panel_estadisticas(stats, emp_mas)
    pausar()


def modulo_historial() -> None:
    limpiar_pantalla()
    imprimir_titulo("HISTORIAL DE ACCIONES DEL SISTEMA")

    imprimir_seccion("Controlador de Empleados")
    ctrl_empleados.mostrar_historial()

    imprimir_seccion("Controlador de Tipos de Permiso")
    ctrl_tipos.mostrar_historial()

    imprimir_seccion("Controlador de Permisos")
    ctrl_permisos.mostrar_historial()

    pausar()


def main() -> None:
    cargar_datos_muestra()

    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_principal()

        if opcion == "1":
            modulo_empleados()
        elif opcion == "2":
            modulo_tipos_permiso()
        elif opcion == "3":
            modulo_permisos()
        elif opcion == "4":
            modulo_estadisticas()
        elif opcion == "5":
            modulo_historial()
        elif opcion == "0":
            limpiar_pantalla()
            print("\n  ╔══════════════════════════════════════════════════════╗")
            print("  ║   Gracias por usar el Sistema de Permisos.           ║")
            print("  ║   ¡Hasta luego!                                      ║")
            print("  ╚══════════════════════════════════════════════════════╝\n")
            sys.exit(0)
        else:
            print("\n  ⚠  Opción no válida. Intente nuevamente.")
            import time; time.sleep(1)


if __name__ == "__main__":
    main()
