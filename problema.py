"""
OPT(i,j) = max(
    coins[i] + OPT(i+2, j) if coins[i+1] >= coins[j] else 0,
    coins[i] + OPT(i+1, j-1) if coins[i+1] < coins[j] else 0,
    coins[j] + OPT(i+1, j-1) if coins[i] >= coins[j-1] else 0,
    coins[j] + OPT(i, j-2) if coins[i] < coins[j-1] else 0
)
"""

import sys

# Desactivate max recursion depth
sys.setrecursionlimit(10**6)


def coin_game(coins, dp, i, j):
    if dp[i][j] != 0:
        return dp[i][j]

    if i == j:
        dp[i][j] = coins[i]
        return coins[i]

    if i + 1 == j:
        dp[i][j] = max(coins[i], coins[j])
        return max(coins[i], coins[j])

    a = coins[i] + coin_game(coins, dp, i + 2, j) if coins[i + 1] >= coins[j] else 0
    b = coins[i] + coin_game(coins, dp, i + 1, j - 1) if coins[i + 1] < coins[j] else 0
    c = coins[j] + coin_game(coins, dp, i + 1, j - 1) if coins[i] >= coins[j - 1] else 0
    d = coins[j] + coin_game(coins, dp, i, j - 2) if coins[i] < coins[j - 1] else 0

    dp[i][j] = max(a, b, c, d)
    return dp[i][j]


def valor_max_sophia(coins):
    n = len(coins)
    dp = [[0] * n for _ in range(n)]

    coin_game(coins, dp, 0, n - 1)

    return dp


if __name__ == "__main__":
    coins = sys.argv[1]
    coins = list(map(int, coins.split(";")))
    print(f"Monedas: {coins}")

    dp = valor_max_sophia(coins)
    max_value = dp[0][len(coins) - 1]
    print(f"Ganancia Sophia: {max_value}")

    valor_mateo = sum(coins) - max_value
    print(f"Ganancia Mateo: {valor_mateo}")
