def reconstruccion(coins, F):
    decisiones = []
    i, j = 0, len(coins) - 1

    while i <= j:
        if F[i][j] == coins[j] + F[i][j - 2] or F[i][j] == coins[j] + F[i + 1][j - 1]:
            decisiones.append(f"Sophia toma {coins[j]} de la derecha")
            j -= 1
        else:
            decisiones.append(f"Sophia toma {coins[i]} de la izquierda")
            i += 1

        # Despues del juego de Sophia, juega Mateo
        if i <= j:
            if coins[i] >= coins[j]:
                decisiones.append(f"Mateo toma {coins[i]} de la izquierda")
                i += 1
            else:
                decisiones.append(f"Mateo toma {coins[j]} de la derecha")
                j -= 1

    return decisiones


if __name__ == "__main__":
    from problema_bottom_up import valor_max_sophia

    coins = [1, 10, 5, 12]
    F = valor_max_sophia(coins)
    decisiones = reconstruccion(coins, F)
    for decision in decisiones:
        print(decision)