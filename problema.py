"""
Ecuacion de recurrencia:

OPT(i, j) = max( 
    coins[i] + min( OPT(i+2, j), OPT(i+1, j-1) ),  Agarrar izquierda
    coins[j] + min( OPT(i, j-2), OPT(i+1, j-1) )   Agarrar derecha
)
"""

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

def run(file_path):

        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                fila = list(int(i) for i in file.readline().strip().split(";") if i)
            else:
                fila = list(int(i) for i in first_line.split(";") if i)
            dp = valor_max_sophia(fila)
            valor_sophia = dp[0][len(fila) - 1]

            print(f"Corriendo algoritmo con el contenido del archivo {file_path}\n")

            print(f"Ganancia Sophia: {valor_sophia}")

        

if __name__ == "__main__":
    file_path = sys.argv[1]
    run(file_path)




'''

Alternativa: 

OPT(i, j) = max(
            coins[i] + (if coins[i+1] > coins[j] then OPT(i+2, j) else OPT(i+1, j-1)),
            coins[j] + (if coins[i] > coins[j-1] then OPT(i+1, j-1) else OPT(i, j-2))
            )

def valor_max_sophia(coins):
    n = len(coins)
    dp = [[0] * n for _ in range(n)]  # Matriz para almacenar los valores máximos

    # Llenar los casos base (cuando i == j, sólo una moneda disponible)
    for i in range(n):
        dp[i][i] = coins[i]

    # Rellenar la matriz de abajo hacia arriba
    for length in range(2, n + 1):  # Longitud de la subfila (de 2 a n)
        for i in range(n - length + 1):
            j = i + length - 1

            # Si Sophia toma la moneda en el extremo izquierdo
            if coins[i + 1] > coins[j]:
                option1 = coins[i] + dp[i + 2][j]  # Mateo toma coins[i+1]
            else:
                option1 = coins[i] + dp[i + 1][j - 1]  # Mateo toma coins[j]

            # Si Sophia toma la moneda en el extremo derecho
            if coins[i] > coins[j - 1]:
                option2 = coins[j] + dp[i + 1][j - 1]  # Mateo toma coins[i]
            else:
                option2 = coins[j] + dp[i][j - 2]  # Mateo toma coins[j-1]

            # Tomar la mejor opción para Sophia
            dp[i][j] = max(option1, option2)

    return dp
'''