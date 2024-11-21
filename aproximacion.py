from pruebas import open_file, print_board
from problema_backtracking import can_place, place_ship
import sys
import time

'''
 Ir a fila/columna de mayor demanda, y ubicar el barco de mayor longitud en dicha fila/columna
 en algún lugar válido. Si el barco de mayor longitud es más largo que dicha demanda, 
 simplemente saltearlo y seguir con el siguiente. Volver a aplicar hasta que no queden más barcos
 o no haya más demandas a cumplir.
'''

def aproximar(row_demand, col_demand, ships, board):
    ships.sort(key=lambda x: x[1], reverse=True)  
    demanda_cumplida = 0
    ship_indices = list(range(len(ships))) 

    while ship_indices:
        max_row_demand = max(row_demand)
        max_col_demand = max(col_demand)
        
        if max_row_demand == 0 and max_col_demand == 0:
            break

        if max_row_demand >= max_col_demand:
            max_demand_index = row_demand.index(max_row_demand)
            placed_ship = False  

            for i in ship_indices:
                index, ship_size = ships[i]
                if ship_size <= max_row_demand:
                    # Intentar colocar el barco horizontalmente en la fila
                    for j in range(len(board[0])):
                        if can_place(board, max_demand_index, j, ship_size, True, row_demand, col_demand):
                            place_ship(board, max_demand_index, j, ships[i], True, row_demand, col_demand)
                            demanda_cumplida += ship_size
                            ship_indices.remove(i)  
                            placed_ship = True
                            break
                    if placed_ship:
                        break

            if not placed_ship:  # Si no se colocó ningún barco, salir del bucle
                break

        else:
            max_demand_index = col_demand.index(max_col_demand)
            placed_ship = False  

            # Intentar colocar los barcos en la columna con la demanda máxima
            for i in ship_indices:
                index, ship_size = ships[i]
                if ship_size <= max_col_demand:
                    # Intentar colocar el barco verticalmente en la columna
                    for j in range(len(board)):
                        if can_place(board, j, max_demand_index, ship_size, False, row_demand, col_demand):
                            place_ship(board, j, max_demand_index, ships[i], False, row_demand, col_demand)
                            demanda_cumplida += ship_size
                            ship_indices.remove(i)  
                            placed_ship = True
                            break
                    if placed_ship:
                        break

            if not placed_ship:  # Si no se colocó ningún barco, salir del bucle
                break
    
    return board, demanda_cumplida


def print_result(row_demand, 
                 col_demand, ships, 
                 board, 
                 total_demanda, 
                 demanda_cumplida, 
                 tiempo):
    print("Filas:", row_demand)
    print("Columnas:", col_demand)
    print("Barcos:", ships)
    print_board(board, row_demand, col_demand)
    print(f"Demanda total: {total_demanda}")
    print(f"Demanda cumplida: {demanda_cumplida}")
    print(f"Demanda insatisfecha: {total_demanda - demanda_cumplida}")
    print(f"Tiempo de ejecución: {tiempo:.2f} segundos")


if __name__ == "__main__":

    filename = sys.argv[1]
    filename = "./test_cases/" + filename

    row_demand, col_demand, ships = open_file(filename)
    original_row_demand = row_demand.copy()
    original_col_demand = col_demand.copy()
    original_ships = ships.copy()
    total_demanda = sum(row_demand) + sum(col_demand)
    n = len(row_demand)
    m = len(col_demand)
    barcos = [(i + 1, length) for i, length in enumerate(ships)]
    board = [[0] * m for _ in range(n)]

    init_time = time.time()
    board_final, demanda_cumplida = aproximar(row_demand, col_demand, barcos, board)
    end_time = time.time()

    print_result(original_row_demand, original_col_demand, original_ships, board_final,
                  total_demanda, demanda_cumplida, end_time - init_time)