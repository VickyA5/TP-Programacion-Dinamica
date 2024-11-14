# Función para verificar restricciones de colocación de un barco
def can_place(board, row, col, length, is_horizontal, row_demand, col_demand):
    max_row, max_col = len(board), len(board[0])

    # Coordenadas de cada celda ocupada por el barco
    ship_cells = [
        (row, col + i) if is_horizontal else (row + i, col) for i in range(length)
    ]

    # Verificar que el barco no se salga del tablero ni se superponga, ni incumpla demandas
    for r, c in ship_cells:
        if not (0 <= r < max_row and 0 <= c < max_col) or board[r][c] != 0:
            return False
        if row_demand[r] - 1 < 0 or col_demand[c] - 1 < 0:
            return False

    # Celdas adyacentes al barco (fila/columna contigua y diagonal)
    adjacent_offsets = [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]

    for r, c in ship_cells:
        # Verificar si hay barcos adyacentes en celdas contiguas y diagonales
        for dr, dc in adjacent_offsets:
            ar, ac = r + dr, c + dc
            if 0 <= ar < max_row and 0 <= ac < max_col and board[ar][ac] != 0:
                return False

    # Verificar que no haya barcos en las celdas antes y después del barco
    start_cell = (row, col - 1) if is_horizontal else (row - 1, col)
    end_cell = (row, col + length) if is_horizontal else (row + length, col)

    for r, c in [start_cell, end_cell]:
        if 0 <= r < max_row and 0 <= c < max_col and board[r][c] != 0:
            return False

    return True


# Función para actualizar demandas y tablero
def place_ship(board, row, col, length, is_horizontal, row_demand, col_demand):
    change = 1
    for i in range(length):
        r, c = (row, col + i) if is_horizontal else (row + i, col)
        board[r][c] += change
        row_demand[r] -= change
        col_demand[c] -= change


def unplace_ship(board, row, col, length, is_horizontal, row_demand, col_demand):
    change = -1
    for i in range(length):
        r, c = (row, col + i) if is_horizontal else (row + i, col)
        board[r][c] += change
        row_demand[r] -= change
        col_demand[c] -= change


# Algoritmo de backtracking para ubicar barcos
def backtrack(board, ships, row_demand, col_demand, min_unmet, solution):
    if not ships:
        unmet = sum(abs(d) for d in row_demand) + sum(abs(d) for d in col_demand)
        if unmet < min_unmet[0]:
            min_unmet[0] = unmet
            solution[:] = [row[:] for row in board]
        return

    # Caso: No colocar el barco actual
    backtrack(board, ships[1:], row_demand, col_demand, min_unmet, solution)

    # Caso: Intentar colocar el barco actual en el tablero
    length = ships[0]
    for r in range(len(board)):
        for c in range(len(board[0])):
            for is_horizontal in (True, False):
                if can_place(
                    board, r, c, length, is_horizontal, row_demand, col_demand
                ):
                    place_ship(
                        board, r, c, length, is_horizontal, row_demand, col_demand
                    )
                    backtrack(
                        board, ships[1:], row_demand, col_demand, min_unmet, solution
                    )
                    unplace_ship(
                        board,
                        r,
                        c,
                        length,
                        is_horizontal,
                        row_demand,
                        col_demand,
                    )


if __name__ == "__main__":

    # Ejemplo de uso
    n, m = 3, 3  # Dimensiones del tablero
    ships = [2, 1]  # Lista de longitudes de barcos
    row_demand = [2, 0, 1]  # Demanda en cada fila
    col_demand = [1, 2, 0]  # Demanda en cada columna

    board = [[0] * m for _ in range(n)]
    solution = [[0] * m for _ in range(n)]
    min_unmet = [float("inf")]

    backtrack(board, ships, row_demand, col_demand, min_unmet, solution)

    assert min_unmet[0] == 0
    assert solution == [[1, 1, 0], [0, 0, 0], [0, 1, 0]]

    # Ejemplo de uso
    n, m = 2, 2
    ships = [1, 1]
    row_demand = [1, 1]
    col_demand = [1, 1]

    board = [[0] * m for _ in range(n)]
    solution = [[0] * m for _ in range(n)]
    min_unmet = [float("inf")]

    backtrack(board, ships, row_demand, col_demand, min_unmet, solution)

    assert min_unmet[0] == 2
    assert solution == [[1, 0], [0, 0]]

    # Ejemplo de uso
    n, m = 2, 2  # Dimensiones del tablero
    ships = [2, 3]  # Lista de longitudes de barcos
    row_demand = [2, 0]  # Demanda en cada fila
    col_demand = [1, 1]  # Demanda en cada columna

    board = [[0] * m for _ in range(n)]
    solution = [[0] * m for _ in range(n)]
    min_unmet = [float("inf")]

    backtrack(board, ships, row_demand, col_demand, min_unmet, solution)

    assert min_unmet[0] == 0
    assert solution == [[1, 1], [0, 0]]

    # Ejemplo de uso
    n, m = 3, 2  # Dimensiones del tablero
    ships = [3, 3]  # Lista de longitudes de barcos
    row_demand = [2, 2, 2]  # Demanda en cada fila
    col_demand = [3, 3]  # Demanda en cada columna

    board = [[0] * m for _ in range(n)]
    solution = [[0] * m for _ in range(n)]
    min_unmet = [float("inf")]

    backtrack(board, ships, row_demand, col_demand, min_unmet, solution)

    assert min_unmet[0] == 6
    assert solution == [[1, 0], [1, 0], [1, 0]]
