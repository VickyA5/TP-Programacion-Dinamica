import sys
import os
from problema import valor_max_sophia


def tests(file_path):
    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                fila = list(int(i) for i in file.readline().strip().split(";") if i)
            else:
                fila = list(int(i) for i in first_line.split(";") if i)

            F = valor_max_sophia(fila)
            valor_sophia = F[0][len(fila) - 1]
            print(f"Ganancia Sophia: {valor_sophia}\n")
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Corriendo controles de prueba")

        for file_path in os.listdir("test_cases/catedra"):
            print("Leyendo archivo", file_path)
            tests(f"test_cases/catedra/{file_path}")
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        tests(file_path)
    else:
        print("Uso: python test.py [archivo]")
        print("Si no se especifica un archivo, se correrán los tests de la cátedra.")
