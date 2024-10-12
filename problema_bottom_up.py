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


def valor_max_sophia(coins):
    n = len(coins)
    # Crear una tabla DP para almacenar las soluciones a subproblemas
    dp = [[0] * n for _ in range(n)]

    # Llenar la tabla DP de abajo hacia arriba
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Caso base: una moneda
            if i == j:
                dp[i][j] = coins[i]
            # Caso base: dos monedas
            elif i + 1 == j:
                dp[i][j] = max(coins[i], coins[j])
            # La recurrencia basada en las elecciones de Sophia y Mateo
            else:
                a = (
                    coins[i] + dp[i + 2][j]
                    if coins[i + 1] >= coins[j]
                    else 0  # noqa: E501
                )
                b = (
                    coins[i] + dp[i + 1][j - 1]
                    if coins[i + 1] < coins[j]
                    else 0  # noqa: E501
                )
                c = (
                    coins[j] + dp[i + 1][j - 1]
                    if coins[i] >= coins[j - 1]
                    else 0  # noqa: E501
                )
                d = (
                    coins[j] + dp[i][j - 2]
                    if coins[i] < coins[j - 1]
                    else 0  # noqa: E501
                )
                dp[i][j] = max(a, b, c, d)

    # El resultado está en dp[0][n-1]
    return dp


if __name__ == "__main__":
    coins = sys.argv[1]
    coins = list(map(int, coins.split(";")))
    dp = valor_max_sophia(coins)

    valor_sophia = dp[0][len(coins) - 1]
    print(f"Ganancia Sophia: {valor_sophia}")

    valor_mateo = sum(coins) - valor_sophia
    print(f"Ganancia Mateo: {valor_mateo}")

    print("Matriz de programación dinámica:")
    for row in dp:
        print(row)

    decisiones = reconstruccion(coins, dp)
    for decision in decisiones:
        print(decision)
