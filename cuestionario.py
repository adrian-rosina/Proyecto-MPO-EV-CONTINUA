import json
import signal

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

def obtener_respuesta():
    while True:
        respuesta = input("Tu respuesta (A, B, C, D): ").upper()
        if respuesta in ["A", "B", "C", "D"]:
            return respuesta
        print("Respuesta inválida. Por favor ingresa A, B, C o D.")

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

def ejecutar_cuestionario():
    preguntas = cargar_preguntas()
    if not preguntas:
        print("No hay preguntas para mostrar.")
        return
    aciertos = 0
    total = len(preguntas)
    for p in preguntas:
        mostrar_pregunta(p)
        respuesta = obtener_respuesta()
        if corregir_respuesta(respuesta, p["respuesta_correcta"]):
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
        print("1 - Empezar cuestionario")
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
