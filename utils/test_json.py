from CORE.json_manager import load, save

ruta = "DATA/entidades.json"

datos = load(ruta)
print("Datos antes:", datos)

nuevo = {"id": 1, "nombre": "Ejemplo"}
datos.append(nuevo)

save(ruta, datos)

datos_actualizados = load(ruta)
print("Datos después:", datos_actualizados)
