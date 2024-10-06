def max_value_sophia(coins):
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
    return F[0][n - 1]


# Ejemplo de uso
coins = [1, 3, 5]
print(max_value_sophia(coins))  # Salida: 6
