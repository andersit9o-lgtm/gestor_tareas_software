import json
import os
from datetime import datetime

nombre_archivo = input("Ingrese el nombre del archivo para guardar las tareas: ")
ARCHIVO = nombre_archivo + ".json"


# Cargar tareas
def cargar_tareas():
    if os.path.exists(ARCHIVO):
        try:
            with open(ARCHIVO, "r") as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
            return []
    return []


# Guardar tareas
def guardar_tarea(tareas):
    try:
        with open(ARCHIVO, "w") as archivo:
            json.dump(tareas, archivo, indent=4)
    except Exception:
        print("Error al guardar las tareas.")


# Validar prioridad
def validar_prioridad(prioridad):
    prioridades_validas = ["Alta", "Media", "Baja"]

    if prioridad.capitalize() in prioridades_validas:
        return prioridad.capitalize()

    print("Prioridad inválida. Use Alta, Media o Baja.")
    return None


# Generar ID único
def generar_id(tareas):

    if not tareas:
        return 1

    return max(t["id"] for t in tareas) + 1


# Validar fecha
def validar_fecha(fecha):

    try:
        fecha_agregada = datetime.strptime(fecha, "%Y-%m-%d").date()

        if fecha_agregada < datetime.now().date():
            print("Solo se permiten fechas actuales o futuras.")
            return None

        return fecha_agregada.strftime("%Y-%m-%d")

    except ValueError:
        print("Formato inválido. Ingrese YYYY-MM-DD.")
        return None


# Crear tarea
def crear_tarea(tareas):

    descripcion = input("Descripción de la tarea de software: ")
    responsable = input("Responsable: ")

    while True:
        fecha = input("Fecha límite (YYYY-MM-DD): ")
        fecha_validada = validar_fecha(fecha)

        if fecha_validada:
            break

    while True:
        prioridad = input("Prioridad (Alta/Media/Baja): ")
        prioridad_validada = validar_prioridad(prioridad)

        if prioridad_validada:
            break

    tarea = {
        "id": generar_id(tareas),
        "descripcion": descripcion,
        "fecha_limite": fecha_validada,
        "responsable": responsable,
        "prioridad": prioridad_validada,
        "estado": "Pendiente"
    }

    tareas.append(tarea)

    guardar_tarea(tareas)

    print("Tarea creada exitosamente.")


# Mostrar todas las tareas
def visualizar_tareas(tareas):

    if not tareas:
        print("No hay tareas registradas.")
        return

    fecha_actual = datetime.now().date()

    for tarea in tareas:

        fecha_tarea = datetime.strptime(tarea["fecha_limite"], "%Y-%m-%d").date()

        dias_restantes = (fecha_tarea - fecha_actual).days

        estado_auto = ""

        if dias_restantes < 0:
            estado_auto = "Tarea vencida."

        elif dias_restantes <= 3:
            estado_auto = "Próximo a vencer."

        print("-------------------------------")
        print("ID:", tarea["id"])
        print("Descripción:", tarea["descripcion"])
        print("Fecha límite:", tarea["fecha_limite"], "(", dias_restantes, "días )", estado_auto)
        print("Responsable:", tarea["responsable"])
        print("Prioridad:", tarea["prioridad"])
        print("Estado:", tarea["estado"])
        print("-------------------------------")


# Actualizar tarea
def actualizar_tarea(tareas):

    try:
        id_tarea = int(input("Ingrese el ID de la tarea a actualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    for tarea in tareas:

        if tarea["id"] == id_tarea:

            tarea["descripcion"] = input("Nueva descripción: ")
            tarea["responsable"] = input("Nuevo responsable: ")

            while True:

                nueva_fecha = input("Nueva fecha límite (YYYY-MM-DD): ")

                fecha_validada = validar_fecha(nueva_fecha)

                if fecha_validada:
                    tarea["fecha_limite"] = fecha_validada
                    break

            while True:

                nueva_prioridad = input("Nueva prioridad (Alta/Media/Baja): ")

                prioridad_validada = validar_prioridad(nueva_prioridad)

                if prioridad_validada:
                    tarea["prioridad"] = prioridad_validada
                    break

            tarea["estado"] = input("Estado (Pendiente/Completo): ")

            guardar_tarea(tareas)

            print("Tarea actualizada.")

            return

    print("Tarea no encontrada.")


# Eliminar tarea
def eliminar_tarea(tareas):

    try:
        id_tarea = int(input("Ingrese el ID de la tarea a eliminar: "))
    except ValueError:
        print("ID inválido.")
        return

    for tarea in tareas:

        if tarea["id"] == id_tarea:

            tareas.remove(tarea)

            guardar_tarea(tareas)

            print("Tarea eliminada.")

            return

    print("Tarea no encontrada.")


# Buscar tareas por responsable
def buscar_por_responsable(tareas):

    nombre = input("Ingrese el nombre del responsable: ")

    encontrado = False

    for tarea in tareas:

        if tarea["responsable"].lower() == nombre.lower():

            print("-----------------------")
            print("ID:", tarea["id"])
            print("Descripción:", tarea["descripcion"])
            print("Fecha límite:", tarea["fecha_limite"])
            print("Prioridad:", tarea["prioridad"])
            print("Estado:", tarea["estado"])

            encontrado = True

    if not encontrado:
        print("No se encontraron tareas para ese responsable.")


# Mostrar tareas pendientes
def mostrar_pendientes(tareas):

    hay_pendientes = False

    for tarea in tareas:

        if tarea["estado"] == "Pendiente":

            print("-----------------------")
            print("ID:", tarea["id"])
            print("Descripción:", tarea["descripcion"])
            print("Responsable:", tarea["responsable"])
            print("Fecha límite:", tarea["fecha_limite"])

            hay_pendientes = True

    if not hay_pendientes:
        print("No hay tareas pendientes.")


# Marcar tarea como completada
def completar_tarea(tareas):

    try:
        id_tarea = int(input("Ingrese el ID de la tarea completada: "))
    except ValueError:
        print("ID inválido.")
        return

    for tarea in tareas:

        if tarea["id"] == id_tarea:

            tarea["estado"] = "Completo"

            guardar_tarea(tareas)

            print("Tarea marcada como completada.")

            return

    print("Tarea no encontrada.")


# MENÚ
def menu():

    tareas = cargar_tareas()

    while True:

        print("\n----- Gestor de tareas de desarrollo de software -----")
        print("1. Crear tarea")
        print("2. Mostrar tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Buscar tareas por responsable")
        print("6. Mostrar tareas pendientes")
        print("7. Marcar tarea como completada")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_tarea(tareas)

        elif opcion == "2":
            visualizar_tareas(tareas)

        elif opcion == "3":
            actualizar_tarea(tareas)

        elif opcion == "4":
            eliminar_tarea(tareas)

        elif opcion == "5":
            buscar_por_responsable(tareas)

        elif opcion == "6":
            mostrar_pendientes(tareas)

        elif opcion == "7":
            completar_tarea(tareas)

        elif opcion == "8":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
