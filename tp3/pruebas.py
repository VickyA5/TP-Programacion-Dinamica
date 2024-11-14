import sys
from problema_backtracking import backtrack

types = ["demandas_filas", "demandas_columnas", "barcos"]


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


def test(filename):
    print(f"Testeando {filename}")

    row_demand, col_demand, ships = open_file(filename)

    n = len(row_demand)
    m = len(col_demand)
    board = [[0] * m for _ in range(n)]

    print("Filas:", row_demand)
    print("Columnas:", col_demand)

    board = [[0] * m for _ in range(n)]
    solution = [[0] * m for _ in range(n)]
    min_unmet = [float("inf")]
    total_demanda = sum(row_demand) + sum(col_demand)

    backtrack(board, ships, row_demand, col_demand, min_unmet, solution)

    for row in solution:
        print(row)

    demanda_satisfecha = total_demanda - min_unmet[0]

    print(f"Demanda total: {total_demanda}")
    print(f"Demanda cumplida: {demanda_satisfecha}")
    print(f"Demanda insatisfecha: {min_unmet[0]}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
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
            filename = "./tp3/test_cases/" + filename
            test(filename)
    else:
        filename = sys.argv[1]
        filename = "./tp3/test_cases/" + filename
        test(filename)
