from pruebas import open_file, print_board
import sys

'''
 Ir a fila/columna de mayor demanda, y ubicar el barco de mayor longitud en dicha fila/columna
 en algún lugar válido. Si el barco de mayor longitud es más largo que dicha demanda, 
 simplemente saltearlo y seguir con el siguiente. Volver a aplicar hasta que no queden más barcos
 o no haya más demandas a cumplir.
'''

# TODO: Revisar, incluir en el informe, mediciones, y el tema de cuan buena aproximacion es 

def aproximar(row_demand, col_demand, ships, board):
    ships = sorted(ships, reverse=True) 

    while ships:
        max_row_demand = max(row_demand)
        max_col_demand = max(col_demand)
        
        if max_row_demand >= max_col_demand:
            # Encontrar el índice de la fila con la demanda máxima
            max_demand_index = row_demand.index(max_row_demand)
            # Intentar colocar los barcos en la fila con la demanda máxima
            for ship in ships:
                if ship <= max_row_demand:
                    # Intentar colocar el barco horizontalmente en la fila
                    for j in range(len(board[0])):
                        # Verificar si hay espacio suficiente y está vacío
                        if all(board[max_demand_index][j + k] == 0 for k in range(ship)):
                            for k in range(ship):
                                board[max_demand_index][j + k] = ship
                            row_demand[max_demand_index] -= ship
                            ships.remove(ship)
                            break
                    else:
                        # Continuar con el siguiente barco si no se pudo colocar
                        continue
                    break
            else:
                # Si no se pudo colocar ningún barco, salir del bucle
                break
        else:
            max_demand_index = col_demand.index(max_col_demand)
            # Intentar colocar los barcos en la columna con la demanda máxima
            for ship in ships:
                if ship <= max_col_demand:
                    # Intentar colocar el barco verticalmente en la columna
                    for i in range(len(board)):
                        # Verificar si hay espacio suficiente y está vacío
                        if all(board[i + k][max_demand_index] == 0 for k in range(ship)):
                            for k in range(ship):
                                board[i + k][max_demand_index] = ship
                            col_demand[max_demand_index] -= ship
                            # Eliminar el barco de la lista
                            ships.remove(ship)
                            break
                    else:
                        # Continuar con el siguiente barco si no se pudo colocar
                        continue
                    break
            else:
                # Si no se pudo colocar ningún barco
                break
    return board


if __name__ == "__main__":

    filename = sys.argv[1]
    filename = "./test_cases/" + filename

    row_demand, col_demand, ships = open_file(filename)
    n = len(row_demand)
    m = len(col_demand)
    board = [[0] * m for _ in range(n)]
    board_final = aproximar(row_demand, col_demand, ships, board)
    print_board(board_final, row_demand, col_demand)