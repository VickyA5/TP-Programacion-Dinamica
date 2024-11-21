import sys
from problema_backtracking import problema as problema_backtracking
from problema_pl import problema as problema_pl
import time


def print_board(board, row_demand, col_demand):
    print("\nMejor solución:\n")
    row_inicial = "    " + " ".join(f"{x:02}" for x in col_demand)
    print(row_inicial)
    row_inicial = "    " + " ".join(["--" for _ in col_demand])
    print(row_inicial)
    i = 0
    for row in board:
        row = (
            f"{row_demand[i]:02}"
            + " |"
            + " ".join([" ." if x == 0 else f"{x:02}" for x in row])
        )
        print(row)
        i += 1
    print()


def open_file(filename):
    rows = []
    cols = []
    barcos = []

    line_breaks = 0

    with open(filename, "r") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.startswith("#"):
                continue

            if line == "":
                line_breaks += 1
                continue

            if line_breaks == 0:
                rows.append(int(line))

            elif line_breaks == 1:
                cols.append(int(line))

            elif line_breaks == 2:
                barcos.append(int(line))

    return rows, cols, barcos


def test(filename, problema):
    print(f"Testeando {filename}")

    row_demand, col_demand, ships = open_file(filename)
    n = len(row_demand)
    m = len(col_demand)

    total_demanda = sum(row_demand) + sum(col_demand)
    row_demand_inicial = row_demand.copy()
    col_demand_inicial = col_demand.copy()

    print("Filas:", row_demand_inicial)
    print("Columnas:", col_demand_inicial)
    print("Barcos:", ships)

    if problema == "b":
        board = [[0] * m for _ in range(n)]
        barcos = [(i + 1, length) for i, length in enumerate(ships)]
        mejor_solucion = [board, float("inf")]
        init_time = time.time()
        problema_backtracking(
            board,
            barcos,
            row_demand,
            col_demand,
            mejor_solucion,
        )
        end_time = time.time()

        print_board(mejor_solucion[0], row_demand_inicial, col_demand_inicial)

        print(f"Demanda total: {total_demanda}")
        print(f"Demanda cumplida: {total_demanda - mejor_solucion[1]}")
        print(f"Demanda insatisfecha: {mejor_solucion[1]}")

        print(f"Tiempo de ejecución: {end_time - init_time:.2f} segundos")

    if problema == "pl":
        init_time = time.time()
        problema_pl(
            n,
            m,
            demandas_filas=row_demand,
            demandas_columnas=col_demand,
            barcos=ships,
        )
        end_time = time.time()

        print(f"Tiempo de ejecución: {end_time - init_time:.2f} segundos")


if __name__ == "__main__":
    if sys.argv[1] == "pl":
        problema = "pl"
    elif sys.argv[1] == "b":
        problema = "b"
    else:
        print("Modo de uso: python pruebas.py <b/pl> <archivo>")
        exit()

    if len(sys.argv) == 2:
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
            filename = "./test_cases/" + filename
            test(filename, problema)
            print()
    else:
        filename = sys.argv[2]
        filename = "./test_cases/" + filename
        test(filename)
