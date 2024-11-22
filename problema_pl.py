# pylint: disable=consider-using-enumerate
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, PULP_CBC_CMD


def problema(n, m, demandas_filas, demandas_columnas, barcos):
    # Crear problema de programación lineal
    problema = LpProblem("Minimizar_Demanda_Insatisfecha", LpMinimize)

    # Posiciones iniciales de los barcos tanto horizontales como verticales
    barcos_h = LpVariable.dicts(
        "y",
        [(i, j, k) for i in range(n) for j in range(m) for k in range(len(barcos))],
        0,
        1,
        cat="Binary",
    )
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

    # Funcion objetivo: minimizar la demanda insatisfecha total
    problema += (
        lpSum(d_filas[i] for i in range(n)) + lpSum(d_columnas[j] for j in range(m)),
        "Demanda_Insatisfecha_Total",
    )

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

    # Verificar que los barcos entren en las filas y las columnas
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
        # Mismo barco no puede ser horizontal y vertical a la vez
        problema += (
            lpSum(barcos_h[i, j, k] for i in range(n) for j in range(m))
            + lpSum(barcos_v[i, j, k] for i in range(n) for j in range(m))
            <= 1,
            f"H_{i}_{j}_{k}+V_{i}_{j}_{k}<=1",
        )

    # Restricciones de adyacencia de barcos horizontales
    for k in range(len(barcos)):
        for i in range(n):
            for j in range(m):
                largo = barcos[k]

                # Verificar que alrededor de la posicion inicial del barco no haya otro barco
                if i - 1 >= 0 and j - 1 >= 0:
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_h[i - 1, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_H_{k}_{i}_{j}_contra_barcos_H_{i - 1}_{j - 1}",
                    )
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_v[i - 1, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_H_{k}_{i}_{j}_contra_barcos_V_{i - 1}_{j - 1}",
                    )
                if j - 1 >= 0:
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_h[i, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_H_{k}_{i}_{j}_contra_barcos_H_{i}_{j - 1}_",
                    )
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_v[i, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_H_{k}_{i}_{j}_contra_barcos_V_{i}_{j - 1}",
                    )
                if i + 1 < n and j - 1 >= 0:
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_h[i + 1, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_H_{k}_{i}_{j}_contra_barcos_H_{i + 1}_{j - 1}",
                    )
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_v[i + 1, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_H_{k}_{i}_{j}_contra_barcos_V_{i + 1}_{j - 1}",
                    )

                # Verificar que a lo largo del barco no haya otro en la misma posicion, ni de forma adyacente
                for l in range(largo):
                    if j + l < m:
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                barcos_h[i, j + l, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barcos_H_{i}_{j + l}",
                        )
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                barcos_v[i, j + l, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"barco_H_{k}_{i}_{j}_contra_barcos_V_{i}_{j + l}",
                        )
                    if i - 1 >= 0 and j + l < m:
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                barcos_h[i - 1, j + l, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_H_{k}_{i}_{j}_contra_barcos_H_{i - 1}_{j + l}",
                        )
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                barcos_v[i - 1, j + l, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_H_{k}_{i}_{j}_contra_barcos_V_{i - 1}_{j + l}",
                        )
                    if i + 1 < n and j + l < m:
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                barcos_h[i + 1, j + l, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_H_{k}_{i}_{j}_contra_barcos_H_{i + 1}_{j + l}",
                        )
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                barcos_v[i + 1, j + l, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_H_{k}_{i}_{j}_contra_barcos_V_{i + 1}_{j + l}",
                        )

                    # Caso donde un barco vertical termina de forma adyacente a uno horizontal
                    if j + l < m:
                        problema += (
                            barcos_h[i, j, k]
                            + lpSum(
                                (
                                    barcos_v[i - barcos[k_otro], j + l, k_otro]
                                    if i - barcos[k_otro] >= 0
                                    else 0
                                )
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_H_{k}_{i}_{j}_contra_posicion_final_barcoss_V_altura_{l}",
                        )

                # Verificar que alrededor de la posicion final del barco no haya otro barco
                if j + largo < m:
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_h[i, j + largo, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_H_{k}_{i}_{j}_contra_barcos_H_{i}_{j + largo}",
                    )
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_v[i, j + largo, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_H_{k}_{i}_{j}_contra_barcos_V_{i}_{j + largo}",
                    )
                if i - 1 >= 0 and j + largo < m:
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_h[i - 1, j + largo, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_H_{k}_{i}_{j}_contra_barcos_H_{i - 1}_{j + largo}",
                    )
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_v[i - 1, j + largo, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_H_{k}_{i}_{j}_contra_barcos_V_{i - 1}_{j + largo}",
                    )
                if i + 1 < n and j + largo < m:
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_h[i + 1, j + largo, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_H_{k}_{i}_{j}_contra_barcos_H_{i + 1}_{j + largo}",
                    )
                    problema += (
                        barcos_h[i, j, k]
                        + lpSum(
                            barcos_v[i + 1, j + largo, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_H_{k}_{i}_{j}_contra_barcos_V_{i + 1}_{j + largo}",
                    )

    # Restricciones de adyacencia de barcos verticales
    for k in range(len(barcos)):
        for i in range(n):
            for j in range(m):
                largo = barcos[k]

                # Verificar que alrededor de la posicion inicial del barco no haya otro barco
                if i - 1 >= 0 and j - 1 >= 0:
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_v[i - 1, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_V_{k}_{i}_{j}_contra_barcos_V_{i - 1}_{j - 1}",
                    )
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_h[i - 1, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_V_{k}_{i}_{j}_contra_barcos_H_{i - 1}_{j - 1}",
                    )
                if i - 1 >= 0:
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_v[i - 1, j, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_V_{k}_{i}_{j}_contra_barcos_V_{i - 1}_{j}",
                    )
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_h[i - 1, j, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_V_{k}_{i}_{j}_contra_barcos_H_{i - 1}_{j}",
                    )
                if i - 1 >= 0 and j + 1 < m:
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_v[i - 1, j + 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_V_{k}_{i}_{j}_contra_barcos_V_{i - 1}_{j + 1}",
                    )
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_h[i - 1, j + 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posocion_inicial_barco_V_{k}_{i}_{j}_contra_barcos_H_{i - 1}_{j + 1}",
                    )

                # Verificar que a lo largo del barco no haya otro en la misma posicion, ni de forma adyacente
                for l in range(largo):
                    if i + l < n:
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                barcos_v[i + l, j, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"barco_V_{k}_{i}_{j}_contra_barcos_V_{i + l}_{j}",
                        )
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                barcos_h[i + l, j, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"barco_V_{k}_{i}_{j}_contra_barcos_H_{i + l}_{j}",
                        )
                    if i + l < n and j - 1 >= 0:
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                barcos_v[i + l, j - 1, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_V_{k}_{i}_{j}_contra_barcos_V_{i + l}_{j - 1}",
                        )
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                barcos_h[i + l, j - 1, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_V_{k}_{i}_{j}_contra_barcos_H_{i + l}_{j - 1}",
                        )

                    if i + l < n and j + 1 < m:
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                barcos_v[i + l, j + 1, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_V_{k}_{i}_{j}_contra_barcos_V_{i + l}_{j + 1}",
                        )
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                barcos_h[i + l, j + 1, k_otro]
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_V_{k}_{i}_{j}_contra_barcos_H_{i + l}_{j + 1}",
                        )

                    # Caso donde un barco horizontal termina de forma adyacente a uno vertical
                    if i + l < n:
                        problema += (
                            barcos_v[i, j, k]
                            + lpSum(
                                (
                                    barcos_h[i + l, j - barcos[k_otro], k_otro]
                                    if j - barcos[k_otro] >= 0
                                    else 0
                                )
                                for k_otro in range(len(barcos))
                                if k_otro != k
                            )
                            <= 1,
                            f"adyacencia_barco_V_{k}_{i}_{j}_contra_posicion_final_barcos_H_altura_{l}",
                        )

                # Verificar que al rededor de la posicion final del barco no haya otro barco
                if i + largo < n:
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_v[i + largo, j, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_V_{k}_{i}_{j}_contra_barcos_V_{i + largo}_{j}",
                    )
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_h[i + largo, j, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_V_{k}_{i}_{j}_contra_barcos_H_{i + largo}_{j}",
                    )
                if i + largo < n and j - 1 >= 0:
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_v[i + largo, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_V_{k}_{i}_{j}_contra_barcos_V_{i + largo}_{j - 1}",
                    )
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_h[i + largo, j - 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_V_{k}_{i}_{j}_contra_barcos_H_{i + largo}_{j - 1}",
                    )
                if i + largo < n and j + 1 < m:
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_v[i + largo, j + 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_V_{k}_{i}_{j}_contra_barcos_V_{i + largo}_{j + 1}",
                    )
                    problema += (
                        barcos_v[i, j, k]
                        + lpSum(
                            barcos_h[i + largo, j + 1, k_otro]
                            for k_otro in range(len(barcos))
                            if k_otro != k
                        )
                        <= 1,
                        f"posicion_final_barco_V_{k}_{i}_{j}_contra_barcos_H_{i + largo}_{j + 1}",
                    )

    # Resolver
    problema.solve(PULP_CBC_CMD(msg=0))

    # Generar tablero y demanda cumplida
    tablero = [[0 for j in range(m)] for i in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(barcos)):
                if barcos_h[i, j, k].varValue == 1:
                    if barcos_v[i, j, k].varValue == 1:
                        raise ValueError(
                            "Barco no puede ser horizontal y vertical a la vez"
                        )
                    for l in range(barcos[k]):
                        tablero[i][j + l] = k + 1
                elif barcos_v[i, j, k].varValue == 1:
                    if barcos_h[i, j, k].varValue == 1:
                        raise ValueError(
                            "Barco no puede ser horizontal y vertical a la vez"
                        )
                    for l in range(barcos[k]):
                        tablero[i + l][j] = k + 1

    demanda_cumplida = (
        sum(demandas_filas) + sum(demandas_columnas) - value(problema.objective)
    )

    print()
    return tablero, demanda_cumplida
