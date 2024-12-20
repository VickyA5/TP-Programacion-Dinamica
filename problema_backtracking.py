# Función para verificar restricciones de colocación de un barco
def can_place(board, row, col, length, is_horizontal, row_demand, col_demand):
    is_vertical = not is_horizontal

    # Verificar que no salga del tablero
    if is_horizontal:
        if col + length > len(board[0]):
            return False

    if is_vertical:
        if row + length > len(board):
            return False

    # Verficiar las demandas
    if is_horizontal:
        if row_demand[row] - length < 0:
            return False

        for i in range(length):
            if col_demand[col + i] - 1 < 0:
                return False

        if col + length > len(board[0]):
            return False

    if is_vertical:
        for i in range(length):
            if row_demand[row + i] - 1 < 0:
                return False

        if col_demand[col] - length < 0:
            return False

        if row + length > len(board):
            return False

    # Verificar que no haya barcos adyacentes ni superpuestos
    for i in range(length):
        r, c = (row, col + i) if is_horizontal else (row + i, col)
        # Verificar que no haya barcos adyacentes en el borde del barco
        if i == 0 and is_horizontal:
            for dr, dc in ((0, -1), (-1, 0), (1, 0), (-1, -1), (1, -1)):
                if (
                    r + dr >= 0
                    and c + dc >= 0
                    and r + dr < len(board)
                    and c + dc < len(board[0])
                    and board[r + dr][c + dc] != 0
                ):
                    return False

        if i == 0 and is_vertical:
            for dr, dc in ((-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1)):
                if (
                    r + dr >= 0
                    and c + dc >= 0
                    and r + dr < len(board)
                    and c + dc < len(board[0])
                    and board[r + dr][c + dc] != 0
                ):
                    return False

        if i == length - 1 and is_horizontal:
            for dr, dc in ((0, 1), (-1, 1), (1, 1), (-1, 0), (1, 0)):
                if (
                    r + dr >= 0
                    and c + dc >= 0
                    and r + dr < len(board)
                    and c + dc < len(board[0])
                    and board[r + dr][c + dc] != 0
                ):
                    return False

        if i == length - 1 and is_vertical:
            for dr, dc in ((1, 0), (1, -1), (1, 1), (0, -1), (0, 1)):
                if (
                    r + dr >= 0
                    and c + dc >= 0
                    and r + dr < len(board)
                    and c + dc < len(board[0])
                    and board[r + dr][c + dc] != 0
                ):
                    return False

        # Verificar que la celda esten vacias
        if board[r][c] != 0:
            return False

        # Verificar que no haya barcos adyacentes
        if is_horizontal:
            # Hay un barco adyacente en la fila de arriba
            if r - 1 <= 0 and board[r - 1][c] != 0:
                return False
            # Hay un barco adyacente en la fila de abajo
            if r + 1 < len(board) and board[r + 1][c] != 0:
                return False

        if is_vertical:
            # Hay un barco adyacente en la columna de la izquierda
            if c - 1 >= 0 and board[r][c - 1] != 0:
                return False
            # Hay un barco adyacente en la columna de la derecha
            if c + 1 < len(board[0]) and board[r][c + 1] != 0:
                return False

    return True


# Función para actualizar demandas y tablero
def place_ship(
    board,
    row,
    col,
    barco,
    is_horizontal,
    row_demand,
    col_demand,
):
    index, length = barco
    for i in range(length):
        r, c = (row, col + i) if is_horizontal else (row + i, col)
        board[r][c] += index

    if is_horizontal:
        row_demand[r] -= length
        for i in range(length):
            col_demand[col + i] -= 1

    if not is_horizontal:
        col_demand[c] -= length
        for i in range(length):
            row_demand[row + i] -= 1


def unplace_ship(board, row, col, barco, is_horizontal, row_demand, col_demand):
    index, length = barco
    for i in range(length):
        r, c = (row, col + i) if is_horizontal else (row + i, col)
        board[r][c] -= index

    if is_horizontal:
        row_demand[r] += length
        for i in range(length):
            col_demand[col + i] += 1

    if not is_horizontal:
        col_demand[c] += length
        for i in range(length):
            row_demand[row + i] += 1


# Algoritmo de backtracking para ubicar barcos
def backtracking(board, barcos, row_demand, col_demand, mejor_solucion):
    demanda_insatisfecha = sum(d for d in row_demand) + sum(d for d in col_demand)

    # Actualizar mejor solución
    if demanda_insatisfecha < mejor_solucion[1]:
        mejor_solucion[1] = demanda_insatisfecha
        mejor_solucion[0] = [[cell for cell in row] for row in board]

    # Caso base
    if not barcos:
        return

    # backtrack
    if (
        demanda_insatisfecha - sum(barco[1] * 2 for barco in barcos)
        >= mejor_solucion[1]
    ):
        return

    # Caso: No colocar el barco actual
    backtracking(
        board,
        barcos[1:],
        row_demand,
        col_demand,
        mejor_solucion,
    )

    # Caso: Intentar colocar el barco actual en el tablero
    barco = barcos[0]
    for r in range(len(board)):
        if row_demand[r] == 0:
            continue
        for c in range(len(board[0])):
            if col_demand[c] == 0:
                continue
            for is_horizontal in (True, False):
                if can_place(
                    board, r, c, barco[1], is_horizontal, row_demand, col_demand
                ):
                    place_ship(
                        board,
                        r,
                        c,
                        barco,
                        is_horizontal,
                        row_demand,
                        col_demand,
                    )
                    backtracking(
                        board,
                        barcos[1:],
                        row_demand,
                        col_demand,
                        mejor_solucion,
                    )
                    unplace_ship(
                        board,
                        r,
                        c,
                        barco,
                        is_horizontal,
                        row_demand,
                        col_demand,
                    )


def problema(board, barcos, row_demand, col_demand, mejor_solucion):
    barcos.sort(key=lambda x: x[1], reverse=True)  # Ordenar por tamaño del barco
    backtracking(board, barcos, row_demand, col_demand, mejor_solucion)
