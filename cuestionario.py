import json
import threading
import sys
import select


# Cargar preguntas desde un archivo JSON
def cargar_preguntas(archivo="preguntas.json"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            preguntas = json.load(f)
        return preguntas
    except FileNotFoundError:
        print("Archivo de preguntas no encontrado.")
        return []

def mostrar_pregunta(pregunta):
    print("\n" + pregunta["pregunta"])
    for opcion in pregunta["opciones"]:
        print(opcion)


def input_con_tiempo(pregunta, limite=20):
    respuesta = [None]

    def leer():
        respuesta[0] = input(pregunta).upper()

    hilo = threading.Thread(target=leer)
    hilo.daemon = True
    hilo.start()
    hilo.join(limite)

    if hilo.is_alive():  # Se acaba el tiempo
        print("\n⏰ Tiempo agotado (20 segundos)")
        return None
    return respuesta[0]

def corregir_respuesta(respuesta, correcta):
    return respuesta == correcta

def mostrar_resultados(aciertos, total):
    porcentaje = (aciertos / total) * 100 if total > 0 else 0
    print("\n--- RESULTADOS ---")
    print(f"Preguntas totales: {total}")
    print(f"Aciertos: {aciertos}")
    print(f"Porcentaje: {porcentaje:.2f}%")
    if porcentaje >= 90:
        print("¡Muy bien! ")
    elif porcentaje >= 60:
        print("Buen trabajo, pero puedes mejorar.")
    else:
        print("Necesitas practicar más.")
    return porcentaje

def guardar_resultado(nombre, porcentaje, archivo="ranking.txt"):
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(f"{nombre},{porcentaje:.2f}\n")

def mostrar_ranking(archivo="ranking.txt"):
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        resultados = []
        for linea in lineas:
            nombre, punt = linea.strip().split(",")
            resultados.append((nombre, float(punt)))
        resultados.sort(key=lambda x: x[1], reverse=True)
        print("\n=== RANKING DE USUARIOS ===")
        print(f"{'Pos.':<5}{'Nombre':<15}{'Puntuación (%)':>15}")
        for i, (nombre, punt) in enumerate(resultados[:10], start=1):
            print(f"{i:<5}{nombre:<15}{punt:>15.2f}")
        print("===========================\n")
    except FileNotFoundError:
        print("No hay resultados guardados aún.")

# Para hacer salto de linea cuando se acaba el tiempo
def input_con_tiempo(pregunta, limite=20): 
    print(pregunta, end="", flush=True)
    i, _, _ = select.select([sys.stdin], [], [], limite)
    if i:
        return sys.stdin.readline().strip().upper()
    else:
        print("\n⏰ Tiempo agotado (20 segundos)")
        return None

def ejecutar_cuestionario():
    preguntas = cargar_preguntas()
    if not preguntas:
        print("No hay preguntas para mostrar.")
        return
    aciertos = 0
    total = len(preguntas)
    for p in preguntas:
        mostrar_pregunta(p)
        respuesta = input_con_tiempo("Tu respuesta (A, B, C, D): ", 20)

        if respuesta is None:  # No contestó a tiempo
            print("❌ Incorrecto. La respuesta correcta era", p["respuesta_correcta"])
        elif corregir_respuesta(respuesta, p["respuesta_correcta"]):
            print("✅ ¡Correcto!")
            aciertos += 1
        else:
            print(f"❌ Incorrecto. La respuesta correcta era {p['respuesta_correcta']}.")

    porcentaje = mostrar_resultados(aciertos, total)
    nombre = input("Introduce tu nombre para guardar el resultado: ")
    guardar_resultado(nombre, porcentaje)
    print("Resultado guardado.\n")

def main():
    while True:
        print("### MENÚ ###")
        print("1 - Empezar cuestionario (20 segundos por respuesta)")
        print("2 - Ranking")
        print("3 - Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            ejecutar_cuestionario()
        elif opcion == "2":
            mostrar_ranking()
        elif opcion == "3":
            print("¡Adiós!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.\n")

if __name__ == "__main__":
    main()