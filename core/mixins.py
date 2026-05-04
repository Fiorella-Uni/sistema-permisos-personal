import datetime
from typing import Any


class LoggerMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log_historial: list = []

    def log(self, nivel: str, mensaje: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada = f"[{timestamp}] [{nivel.upper()}] {mensaje}"
        self._log_historial.append(entrada)

    def log_info(self, mensaje: str) -> None:
        self.log("INFO", mensaje)

    def log_error(self, mensaje: str) -> None:
        self.log("ERROR", mensaje)

    def log_advertencia(self, mensaje: str) -> None:
        self.log("ADVERTENCIA", mensaje)

    def obtener_historial(self) -> list:
        return self._log_historial.copy()

    def mostrar_historial(self) -> None:
        if not self._log_historial:
            print("  (Sin registros en el historial)")
            return
        for entrada in self._log_historial[-20:]:
            print(f"  {entrada}")


class ValidationMixin:

    @staticmethod
    def validar_no_vacio(valor: Any, nombre_campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo '{nombre_campo}' es obligatorio y no puede estar vacío.")
        return valor.strip()

    @staticmethod
    def validar_numero_positivo(valor: Any, nombre_campo: str) -> float:
        try:
            numero = float(valor)
        except (ValueError, TypeError):
            raise ValueError(f"El campo '{nombre_campo}' debe ser un número válido.")
        if numero <= 0:
            raise ValueError(f"El campo '{nombre_campo}' debe ser un valor mayor que cero.")
        return numero

    @staticmethod
    def validar_opcion(valor: str, opciones: list, nombre_campo: str) -> str:
        valor_upper = valor.strip().upper()
        if valor_upper not in [op.upper() for op in opciones]:
            raise ValueError(
                f"El campo '{nombre_campo}' debe ser uno de: {', '.join(opciones)}. "
                f"Se recibió: '{valor}'."
            )
        return valor_upper

    @staticmethod
    def validar_fecha(fecha_str: str, nombre_campo: str) -> datetime.date:
        formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
        for fmt in formatos:
            try:
                return datetime.datetime.strptime(fecha_str.strip(), fmt).date()
            except ValueError:
                continue
        raise ValueError(
            f"El campo '{nombre_campo}' tiene formato de fecha inválido. "
            f"Use DD/MM/YYYY o YYYY-MM-DD."
        )

    @staticmethod
    def validar_rango_fechas(fecha_inicio: datetime.date, fecha_fin: datetime.date) -> None:
        if fecha_inicio > fecha_fin:
            raise ValueError(
                f"La fecha de inicio ({fecha_inicio}) no puede ser posterior "
                f"a la fecha fin ({fecha_fin})."
            )

    @staticmethod
    def validar_cedula_ecuatoriana(cedula: str) -> str:
        cedula = cedula.strip()

        if not cedula.isdigit():
            raise ValueError("La cédula debe contener únicamente dígitos numéricos.")

        if len(cedula) != 10:
            raise ValueError("La cédula ecuatoriana debe tener exactamente 10 dígitos.")

        provincia = int(cedula[:2])
        if provincia < 1 or provincia > 24:
            raise ValueError(
                f"Los primeros dos dígitos de la cédula ({cedula[:2]}) "
                f"no corresponden a una provincia válida (01-24)."
            )

        tercer_digito = int(cedula[2])
        if tercer_digito >= 6:
            raise ValueError(
                f"El tercer dígito de la cédula ({tercer_digito}) debe ser menor que 6 "
                f"para personas naturales."
            )

        coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
        suma = 0
        for i, coef in enumerate(coeficientes):
            producto = int(cedula[i]) * coef
            if producto >= 10:
                producto -= 9
            suma += producto

        digito_verificador_calculado = (10 - (suma % 10)) % 10
        digito_verificador_real = int(cedula[9])

        if digito_verificador_calculado != digito_verificador_real:
            raise ValueError(
                f"La cédula '{cedula}' no es válida. "
                f"El dígito verificador no coincide (esperado: {digito_verificador_calculado}, "
                f"recibido: {digito_verificador_real})."
            )

        return cedula
