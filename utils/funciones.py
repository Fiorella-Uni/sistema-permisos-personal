import datetime
from functools import reduce
from typing import List, Any, Callable, Dict


def calcular_estadisticas_permisos(
    permisos: list,
    empleados: list,
    tipos_permiso: list
) -> Dict[str, Any]:
    total_empleados = len(empleados)
    total_permisos = len(permisos)

    ids_remunerados = set(
        map(lambda tp: tp.id, filter(lambda tp: tp.es_remunerado, tipos_permiso))
    )
    ids_no_remunerados = set(
        map(lambda tp: tp.id, filter(lambda tp: not tp.es_remunerado, tipos_permiso))
    )

    permisos_remunerados = list(
        filter(lambda p: p.id_tipo_permiso in ids_remunerados, permisos)
    )
    permisos_no_remunerados = list(
        filter(lambda p: p.id_tipo_permiso in ids_no_remunerados, permisos)
    )

    permisos_dias = list(filter(lambda p: p.tipo == "D", permisos))
    total_tiempo_dias = reduce(
        lambda acc, p: acc + p.tiempo, permisos_dias, 0.0
    ) if permisos_dias else 0.0

    permisos_horas = list(filter(lambda p: p.tipo == "H", permisos))
    total_tiempo_horas = reduce(
        lambda acc, p: acc + p.tiempo, permisos_horas, 0.0
    ) if permisos_horas else 0.0

    total_descuentos = reduce(
        lambda acc, p: acc + p.descuento, permisos_no_remunerados, 0.0
    ) if permisos_no_remunerados else 0.0

    sueldo_promedio = (
        reduce(lambda acc, e: acc + e.sueldo, empleados, 0.0) / total_empleados
        if total_empleados > 0 else 0.0
    )

    if total_permisos > 0 and total_empleados > 0:
        conteo_por_empleado = list(map(
            lambda emp: (emp, len(list(filter(
                lambda p: p.id_empleado == emp.id, permisos
            )))),
            empleados
        ))
        empleado_mas_permisos = reduce(
            lambda a, b: a if a[1] >= b[1] else b,
            conteo_por_empleado
        )
    else:
        empleado_mas_permisos = (None, 0)

    return {
        "total_empleados": total_empleados,
        "total_permisos": total_permisos,
        "permisos_remunerados": len(permisos_remunerados),
        "permisos_no_remunerados": len(permisos_no_remunerados),
        "total_tiempo_dias": total_tiempo_dias,
        "total_tiempo_horas": total_tiempo_horas,
        "total_descuentos": round(total_descuentos, 2),
        "sueldo_promedio": round(sueldo_promedio, 2),
        "empleado_mas_permisos": empleado_mas_permisos,
    }


def calcular_descuento(empleado, permiso, tipo_permiso) -> float:
    if tipo_permiso.es_remunerado:
        return 0.0

    if permiso.tipo == "H":
        descuento = empleado.valor_hora * permiso.tiempo
    else:
        sueldo_diario = empleado.sueldo / 30
        descuento = sueldo_diario * permiso.tiempo

    return round(descuento, 2)


def aplicar_a_lista(coleccion: list, transformacion: Callable) -> list:
    return list(map(transformacion, coleccion))


def filtrar_lista(coleccion: list, criterio: Callable) -> list:
    return list(filter(criterio, coleccion))


def acumular(coleccion: list, acumulador: Callable, valor_inicial: Any = 0) -> Any:
    if not coleccion:
        return valor_inicial
    return reduce(acumulador, coleccion, valor_inicial)


def formatear_fecha(fecha: datetime.date) -> str:
    return fecha.strftime("%d/%m/%Y")


def calcular_dias_habiles(fecha_inicio: datetime.date, fecha_fin: datetime.date) -> int:
    dias = 0
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        if fecha_actual.weekday() < 5:
            dias += 1
        fecha_actual += datetime.timedelta(days=1)
    return dias
