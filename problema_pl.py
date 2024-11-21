from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value


def problema(n, m, demandas_filas, demandas_columnas, barcos):
    # MODELO
    problema = LpProblem("Minimizar_Demanda_Insatisfecha", LpMinimize)

    # VARIABLES
    # Posiciones iniciales de los barcos
    barcos_h = LpVariable.dicts(
        "y",
        [(i, j, k) for i in range(n) for j in range(m) for k in range(len(barcos))],
        0,
        1,
        cat="Binary",
    )

    # Variables que representa si un barco es posicionado de forma horizontal o vertical
    barcos_v = LpVariable.dicts(
        "h",
        [(i, j, k) for i in range(n) for j in range(m) for k in range(len(barcos))],
        0,
        1,
        cat="Binary",
    )

    # Variables de demanda insatisfecha para filas y columnas
    d_filas = LpVariable.dicts("d_filas", range(n), 0, None, cat="Integer")
    d_columnas = LpVariable.dicts("d_columnas", range(m), 0, None, cat="Integer")

    # FUNCIÓN OBJETIVO: minimizar la demanda insatisfecha total
    problema += (
        lpSum(d_filas[i] for i in range(n)) + lpSum(d_columnas[j] for j in range(m)),
        "Demanda_Insatisfecha_Total",
    )

    # RESTRICCIONES
    # Demandas instafisfecha por filas
    for i in range(n):
        problema += (
            lpSum(
                barcos_h[i, j, k] * barcos[k]
                for j in range(m)
                for k in range(len(barcos))
            )  # Barcos horizontales caso facil
            + lpSum(
                (
                    barcos_v[i - l, j, k] if i - l >= 0 else 0
                    for l in range(barcos[k])
                    for j in range(m)
                )
                for k in range(len(barcos))
            )  # Barcos verticales ir viendo filas de arriba si algun barco vertical corta esta fila
            + d_filas[i]
            == demandas_filas[i],
            f"Demanda_Fila_{i}",
        )

    # Demandas instafisfecha por columnas
    for j in range(m):
        problema += (
            lpSum(
                (
                    barcos_h[i, j - l, k] if j - l >= 0 else 0
                    for l in range(barcos[k])
                    for i in range(n)
                )
                for k in range(len(barcos))
            )
            + lpSum(
                barcos_v[i, j, k] * barcos[k]
                for i in range(n)
                for k in range(len(barcos))
            )
            + d_columnas[j]
            == demandas_columnas[j],
            f"Demanda_Columna_{j}",
        )

    for i in range(n):
        for j in range(m):
            for k in range(len(barcos)):
                problema += (
                    barcos_h[i, j, k] + barcos_v[i, j, k] <= 1,
                    f"Barco_{k}_en_posicion_{i}_{j}_es_H_o_V",
                )

    # Verificar que los barcos entren en la fila
    for k in range(len(barcos)):
        for i in range(n):
            for j in range(m):
                problema += (
                    barcos_h[i, j, k] * barcos[k] <= m - j,
                    f"Barco_H_{k}_en_posicion_{i}_{j}_entra_en_fila",
                )
                problema += (
                    barcos_v[i, j, k] <= m - j,
                    f"Barco_V_{k}_en_posicion_{i}_{j}_entra_en_fila",
                )
                problema += (
                    barcos_h[i, j, k] <= n - i,
                    f"Barco_H_{k}_en_posicion_{i}_{j}_entra_en_columna",
                )
                problema += (
                    barcos_v[i, j, k] * barcos[k] <= n - i,
                    f"Barco_V_{k}_en_posicion_{i}_{j}_entra_en_columna",
                )

    for k in range(len(barcos)):
        # No puede haber mas de una posicion de barco horizontal
        problema += (
            lpSum(barcos_h[i, j, k] for i in range(n) for j in range(m)) <= 1,
            f"Suma_de_posiciones_barco_H_{k}<=1",
        )

        # No puede haber mas de una posicion de barco vertical
        problema += (
            lpSum(barcos_v[i, j, k] for i in range(n) for j in range(m)) <= 1,
            f"Suma_de_posiciones_barco_V_{k}<=1",
        )

        # Mismo barco no puede ser horizontal y vertical a la vez
        problema += (
            lpSum(barcos_h[i, j, k] for i in range(n) for j in range(m))
            + lpSum(barcos_v[i, j, k] for i in range(n) for j in range(m))
            <= 1,
            f"H_{i}_{j}_{k}+V_{i}_{j}_{k}<=1",
        )

        # Si en h es 1, en v es 0 y viceversa
        for i in range(n):
            for j in range(m - barcos[k] + 1):
                problema += (
                    barcos_h[i, j, k] + barcos_v[i, j, k] <= 1,
                    f"Si_H_{i}_{j}_{k}_es_1_entonces_V_{i}_{j}_{k}_es_0",
                )

    # Restricciones de adyacencia de barcos horizontales
    for k in range(len(barcos)):
        for i in range(n):
            for j in range(m):
                largo = barcos[k]
                for k_otro in range(len(barcos)):
                    if k == k_otro:
                        continue

                    if i + 1 < n and j + largo + 1 < m:
                        problema += (
                            barcos_h[i, j, k] + barcos_h[i + 1, j + largo + 1, k_otro]
                            <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i}_{j}_caso_borde_encontrado_1",
                        )
                        problema += (
                            barcos_h[i, j, k] + barcos_v[i + 1, j + largo + 1, k_otro]
                            <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i}_{j}_caso_borde_encontrado_1",
                        )

                    for l in range(largo):
                        if i - 1 >= 0 and j + l < m:
                            problema += (
                                barcos_h[i, j, k] + barcos_h[i - 1, j + l, k_otro] <= 1,
                                f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i - 1}_{j + l}",
                            )
                            problema += (
                                barcos_h[i, j, k] + barcos_v[i - 1, j + l, k_otro] <= 1,
                                f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i - 1}_{j + l}",
                            )
                        if i + 1 < n and j + l < m:
                            problema += (
                                barcos_h[i, j, k] + barcos_h[i + 1, j + l, k_otro] <= 1,
                                f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + 1}_{j + l}",
                            )
                            problema += (
                                barcos_h[i, j, k] + barcos_v[i + 1, j + l, k_otro] <= 1,
                                f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + 1}_{j + l}",
                            )

                    if j + largo < m:
                        problema += (
                            barcos_h[i, j, k] + barcos_h[i, j + largo, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i}_{j + largo}",
                        )
                        problema += (
                            barcos_h[i, j, k] + barcos_v[i, j + largo, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i}_{j + largo}",
                        )
                        if i - 1 >= 0:
                            problema += (
                                barcos_h[i, j, k] + barcos_h[i - 1, j + largo, k_otro]
                                <= 1,
                                f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i - 1}_{j + largo}",
                            )
                            problema += (
                                barcos_h[i, j, k] + barcos_v[i - 1, j + largo, k_otro]
                                <= 1,
                                f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i - 1}_{j + largo}",
                            )

                    # No se pueden superponer barcos
                    problema += (
                        barcos_h[i, j, k] + barcos_h[i, j, k_otro] <= 1,
                        f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i}_{j}",
                    )
                    problema += (
                        barcos_h[i, j, k] + barcos_v[i, j, k_otro] <= 1,
                        f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i}_{j}",
                    )

                    if j - 1 >= 0:
                        problema += (
                            barcos_h[i, j, k] + barcos_h[i, j - 1, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i}_{j - 1}",
                        )
                        problema += (
                            barcos_h[i, j, k] + barcos_v[i, j - 1, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i}_{j - 1}",
                        )

                    if i - 1 >= 0 and j - 1 >= 0:
                        problema += (
                            barcos_h[i, j, k] + barcos_h[i - 1, j - 1, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i - 1}_{j - 1}",
                        )
                        problema += (
                            barcos_h[i, j, k] + barcos_v[i - 1, j - 1, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i - 1}_{j - 1}",
                        )
                    if i + 1 < n and j - 1 >= 0:
                        problema += (
                            barcos_h[i, j, k] + barcos_h[i + 1, j - 1, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + 1}_{j - 1}",
                        )
                        problema += (
                            barcos_h[i, j, k] + barcos_v[i + 1, j - 1, k_otro] <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + 1}_{j - 1}",
                        )

    # Restricciones de adyacencia de barcos verticales
    for k in range(len(barcos)):
        for i in range(n):
            for j in range(m):
                largo = barcos[k]
                for k_otro in range(len(barcos)):
                    if k == k_otro:
                        continue

                    problema += (
                        barcos_v[i, j, k] + barcos_v[i, j, k_otro] <= 1,
                        f"barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i}_{j}_caso_borde_encontrado_2",
                    )

                    if i + largo < n and j + 1 < m:
                        problema += (
                            barcos_v[i, j, k] + barcos_v[i + largo, j + 1, k_otro] <= 1,
                            f"barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + 1}_{j + 1}_caso_borde_encontrado_1",
                        )
                        problema += (
                            barcos_v[i, j, k] + barcos_h[i + largo, j + 1, k_otro] <= 1,
                            f"barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + 1}_{j + 1}_caso_borde_encontrado_1",
                        )

                    if i + largo < n:
                        problema += (
                            barcos_v[i, j, k] + barcos_v[i + largo, j, k_otro] <= 1,
                            f"barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + largo}_{j}_caso_borde_encontrado_1",
                        )
                        problema += (
                            barcos_v[i, j, k] + barcos_h[i + largo, j, k_otro] <= 1,
                            f"barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + largo}_{j}_caso_borde_encontrado_1",
                        )

                    for l in range(largo):
                        if j - 1 >= 0 and i + l < n:
                            problema += (
                                barcos_v[i, j, k] + barcos_h[i + l, j - 1, k_otro] <= 1,
                                f"adyacencia1: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + l}_{j - 1}",
                            )
                            problema += (
                                barcos_v[i, j, k] + barcos_v[i + l, j - 1, k_otro] <= 1,
                                f"adyacencia2: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + l}_{j - 1}",
                            )
                        if j + 1 < m and i + l < n:
                            problema += (
                                barcos_v[i, j, k] + barcos_h[i + l, j + 1, k_otro] <= 1,
                                f"adyacencia3: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + l}_{j + 1}",
                            )
                            problema += (
                                barcos_v[i, j, k] + barcos_v[i + l, j + 1, k_otro] <= 1,
                                f"adyacencia4: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + l}_{j + 1}",
                            )

                    if i + largo + 1 < n:
                        problema += (
                            barcos_v[i, j, k] + barcos_v[i + largo + 1, j, k_otro] <= 1,
                            f"adyacencia13: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + largo + 1}_{j}",
                        )
                        problema += (
                            barcos_v[i, j, k] + barcos_h[i + largo + 1, j, k_otro] <= 1,
                            f"adyacencia14: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + largo + 1}_{j}",
                        )

                        if j - 1 >= 0:
                            problema += (
                                barcos_v[i, j, k]
                                + barcos_v[i + largo + 1, j - 1, k_otro]
                                <= 1,
                                f"adyacencia5: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i}_{j + largo}",
                            )
                            problema += (
                                barcos_v[i, j, k]
                                + barcos_h[i + largo + 1, j - 1, k_otro]
                                <= 1,
                                f"adyacencia6: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + largo + 1}_{j -1}",
                            )

                        if j + 1 < m:
                            problema += (
                                barcos_v[i, j, k]
                                + barcos_v[i + largo + 1, j + 1, k_otro]
                                <= 1,
                                f"adyacencia15: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i + largo + 1}_{j+1}",
                            )
                            problema += (
                                barcos_v[i, j, k]
                                + barcos_h[i + largo + 1, j + 1, k_otro]
                                <= 1,
                                f"adyacencia16: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i + largo + 1}_{j+1}",
                            )

                    if i - 1 >= 0:
                        problema += (
                            barcos_v[i, j, k] + barcos_v[i - 1, j, k_otro] <= 1,
                            f"adyacencia7: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i - 1}_{j}",
                        )
                        problema += (
                            barcos_v[i, j, k] + barcos_h[i - 1, j, k_otro] <= 1,
                            f"adyacencia8: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i - 1}_{j}",
                        )
                    if i - 1 >= 0 and j - 1 >= 0:
                        problema += (
                            barcos_v[i, j, k] + barcos_v[i - 1, j - 1, k_otro] <= 1,
                            f"adyacencia9: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i - 1}_{j - 1}",
                        )
                        problema += (
                            barcos_v[i, j, k] + barcos_h[i - 1, j - 1, k_otro] <= 1,
                            f"adyacencia10: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i - 1}_{j - 1}",
                        )
                    if i - 1 >= 0 and j + 1 < m:
                        problema += (
                            barcos_v[i, j, k] + barcos_v[i - 1, j + 1, k_otro] <= 1,
                            f"adyacencia11: barco_V_{k}_{i}_{j}_contra_barco_V_{k_otro}_{i - 1}_{j + 1}",
                        )
                        problema += (
                            barcos_v[i, j, k] + barcos_h[i - 1, j + 1, k_otro] <= 1,
                            f"adyacencia12: barco_V_{k}_{i}_{j}_contra_barco_H_{k_otro}_{i - 1}_{j + 1}",
                        )

    # RESOLVER
    problema.solve()

    # IMPRIMIR RESULTADOS
    print("Demandas filas:", demandas_filas)
    print("Demandas columnas:", demandas_columnas)
    demanda_cumplida = (
        sum(demandas_filas) + sum(demandas_columnas) - value(problema.objective)
    )
    print(
        "Demanda cumplida:",
        demanda_cumplida,
    )
    print("Demanda insatisfecha:", value(problema.objective))
    print("Demanda insatisfecha por filas:", [value(d_filas[i]) for i in range(n)])
    print(
        "Demanda insatisfecha por columnas:", [value(d_columnas[j]) for j in range(m)]
    )

    # IMPRIMIR TABLERO
    tablero = [[0 for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(barcos)):
                if barcos_h[i, j, k].varValue == 1:
                    if barcos_v[i, j, k].varValue == 1:
                        print("ERROR: Barco en posición no válida")
                    for l in range(barcos[k]):
                        tablero[i][j + l] = k + 1
                elif barcos_v[i, j, k].varValue == 1:
                    for l in range(barcos[k]):
                        tablero[i + l][j] = k + 1

    print("Tablero:")
    for fila in tablero:
        print(fila)

    print("Barcos colocados H:")
    for i in range(n):
        for j in range(m):
            for k in range(len(barcos)):
                if barcos_h[i, j, k].varValue == 1:
                    print(f"Barco {k+1} en posición {i},{j}")

    print("Barcos colocados V:")
    for i in range(n):
        for j in range(m):
            for k in range(len(barcos)):
                if barcos_v[i, j, k].varValue == 1:
                    print(f"Barco {k+1} en posición {i},{j}")

    return tablero, demanda_cumplida
