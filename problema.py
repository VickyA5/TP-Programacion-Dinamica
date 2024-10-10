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


if __name__ == "__main__":
    coins = sys.argv[1]
    coins = list(map(int, coins.split(";")))
    F = valor_max_sophia(coins)
    valor_sophia = F[0][len(coins) - 1]
    print(f"Ganancia Sophia: {valor_sophia}")
