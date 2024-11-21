from problema_backtracking import backtracking
from aproximacion import aproximar
from pruebas import open_file


import copy

def calculate_approximation_factor():
    mean_factor = 0
    for filename in (
            "3_3_2.txt",
            "5_5_6.txt",
            "8_7_10.txt",
            "10_3_3.txt",
            "10_10_10.txt",
            "12_12_21.txt",
            "15_10_15.txt",
            "20_20_20.txt",
            "20_25_30.txt",
            "30_25_25.txt",
        ):
        path = "./test_cases/" + filename
        row_demand, col_demand, ships = open_file(path)

        n = len(row_demand)
        m = len(col_demand)

        total_demanda = sum(row_demand) + sum(col_demand)
        row_demand_inicial = copy.deepcopy(row_demand)
        col_demand_inicial = copy.deepcopy(col_demand)

        board = [[0] * m for _ in range(n)]
        board_original = copy.deepcopy(board)
        barcos = [(i + 1, length) for i, length in enumerate(ships)]
        barcos_original = copy.deepcopy(barcos)
        mejor_solucion = [copy.deepcopy(board), float("inf")]

        backtracking(
            board,
            barcos,
            row_demand,
            col_demand,
            mejor_solucion
        )

        demanda_cumplida_backtracking = total_demanda - mejor_solucion[1]
        demanda_cumplida_aproximacion = aproximar(row_demand_inicial, col_demand_inicial, barcos_original, board_original)[1]
        
        factor = demanda_cumplida_aproximacion / demanda_cumplida_backtracking
        mean_factor += factor
        
        print(f"El factor para {filename}" + " es: " + str(factor))
    
    return mean_factor / 10




if __name__ == "__main__":
    mean_factor = calculate_approximation_factor()
    print(f"\nEl factor de aproximación promedio es: {mean_factor}")
