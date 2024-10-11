"""
OPT(i, j) = max(
    coins[i] + min( OPT(i+2, j), OPT(i+1, j-1) ),  Agarrar izquierda
    coins[j] + min( OPT(i, j-2), OPT(i+1, j-1) )   Agarrar derecha
)
"""

"""
OPT(i,j) = max(
    coins[i] + OPT(i+2, j) if coins[i+1] >= coins[j] else 0,
    coins[i] + OPT(i+1, j-1) if coins[i+1] < coins[j] else 0,
    coins[j] + OPT(i+1, j-1) if coins[i] >= coins[j-1] else 0,
    coins[j] + OPT(i, j-2) if coins[i] < coins[j-1] else 0
)
"""

import sys
from reconstruccion import reconstruccion

# FALTA LA RECONSTRUCCION


def valor_max_sophia(coins):
    n = len(coins)
    # Crear una tabla DP para almacenar las soluciones a subproblemas
    dp = [[0] * n for _ in range(n)]

    # Llenar la tabla DP de abajo hacia arriba
    for length in range(1, n + 1):  # length es el tamaño de la subsecuencia
        for i in range(n - length + 1):
            j = i + length - 1
            print("i = ", i, "j = ", j)
            if i == j:
                print("Caso base, una moneda: ", coins[i])
                dp[i][j] = coins[i]  # Caso base: una moneda
            elif i + 1 == j:
                print(
                    f"Caso base, dos monedas: {coins[i]} {coins[j]} {max(coins[i], coins[j])}"
                )
                dp[i][j] = max(coins[i], coins[j])  # Caso base: dos monedas
            else:
                print(
                    f"Comparando max({coins[i]} + min({dp[i+2][j]}, {dp[i+1][j-1]}), {coins[j]} + min({dp[i][j-2]}, {dp[i+1][j-1]}))"
                )
                # La recurrencia basada en las elecciones de Sophia y Mateo
                dp[i][j] = max(
                    coins[i]
                    + min(
                        dp[i + 2][j] if i + 2 <= j else 0,
                        dp[i + 1][j - 1] if i + 1 <= j - 1 else 0,
                    ),
                    coins[j]
                    + min(
                        dp[i + 1][j - 1] if i + 1 <= j - 1 else 0,
                        dp[i][j - 2] if i <= j - 2 else 0,
                    ),
                )
                print("dp[", i, "][", j, "] = ", dp[i][j])

    # El resultado está en dp[0][n-1], que es el máximo valor que Sophia puede obtener
    return dp

    # length = [1,2,3]
    # length = 2
    # i = [0,1]
    # i = 0
    # j = 1
    # ... pick coins
    # pick_i = coins[0] + min(F[2][1], F[1][0]) = 1
    # pick_j = coins[1] + min(F[0][1], F[1][0]) = 10 + min(10, 0) = 10
    # F[0][1] = max(1, 10) = 10
    # i = 1
    # j = 2
    # ... pick coins
    # pick_i = coins[1] + min(F[3][2], F[2][1]) = 10 + min(0, 0) = 10
    # pick_j = coins[2] + min(F[1][2], F[2][1]) = 5 + min(0, 0) = 5
    # F[1][2] = max(10, 5) = 10
    # length = 3
    # i = [0]
    # i = 0
    # j = 2
    # ... pick coins
    # pick_i = coins[0] + min(F[2][2], F[1][1]) = 1 + min(5, 10) = 6
    # pick_j = coins[2] + min(F[0][0], F[1][1]) = 5 + min(1, 10) = 6
    # F[0][2] = max(6, 6) = 6

    # El resultado óptimo está en F[0][n-1]


if __name__ == "__main__":
    coins = sys.argv[1]
    coins = list(map(int, coins.split(";")))
    F = valor_max_sophia(coins)

    valor_sophia = F[0][len(coins) - 1]
    print(f"Ganancia Sophia: {valor_sophia}")

    valor_mateo = sum(coins) - valor_sophia
    print(f"Ganancia Mateo: {valor_mateo}")

    print("Matriz de programación dinámica:")
    for row in F:
        print(row)

    decisiones = reconstruccion(coins, F)
    for decision in decisiones:
        print(decision)
