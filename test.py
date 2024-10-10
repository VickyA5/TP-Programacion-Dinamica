import sys
import os
from problema import valor_max_sophia


def tests(file_path):
    output_folder = "outputs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                fila = list(int(i) for i in file.readline().strip().split(";") if i)
            else:
                fila = list(int(i) for i in first_line.split(";") if i)

            F = valor_max_sophia(fila)
            valor_sophia = F[0][len(fila) - 1]

            print(f"Corriendo algoritmo con el contenido del archivo {file_path}\n")
            print(f"Ganancia Sophia: {valor_sophia}\n")

            # output_filename = os.path.basename(file_path).replace(".txt", "_resultado.txt")
            # with open(f"{output_folder}/{output_filename}", "w") as output_file:
            #   output_file.write(f"Esperados: {'; '.join(map(str, esperados))}\n")
            # print(f"\nLos resultados de las acciones individuales de cada jugador se encuentran en outputs/{output_filename}.\n")
    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Corriendo controles de prueba")

        for file_path in os.listdir("test_cases/catedra"):
            print("Leyendo archivo", file_path)
            tests(f"test_cases/catedra/{file_path}")
    else:
        file_path = sys.argv[1]
        tests(file_path)
