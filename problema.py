'''
Ecuacion de recurrencia:

OPT(i, j) = max( coins[i] + min( OPT(i+2, j), OPT(i+1, j-1) ),   Agarrar izquierda
                coins[j] + min( OPT(i, j-2), OPT(i+1, j-1) ) )   Agarrar derecha
'''

import os
import sys

# FALTA LA RECONSTRUCCION

def valor_max_sophia(coins):
    n = len(coins)
    # Crear tabla de DP
    F = [[0] * n for _ in range(n)]

    # Caso base: cuando solo hay una moneda disponible
    for i in range(n):
        F[i][i] = coins[i]

    # Llenar la tabla para subsecuencias de longitud 2 hasta n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Aplicar la ecuación de recurrencia
            pick_i = coins[i] + min(
                F[i + 2][j] if i + 2 <= j else 0,
                F[i + 1][j - 1] if i + 1 <= j - 1 else 0,
            )
            pick_j = coins[j] + min(
                F[i][j - 2] if i <= j - 2 else 0,
                F[i + 1][j - 1] if i + 1 <= j - 1 else 0,
            )
            F[i][j] = max(pick_i, pick_j)

    # El resultado óptimo está en F[0][n-1]
    return F


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
        print("Argumentos incorrectos.\n" +
              "Para ejecutar el algoritmo con un txt: python3 problema.py <archivo_set_de_datos.txt>\n")
    else:
        file_path = sys.argv[1]
        tests(file_path)
