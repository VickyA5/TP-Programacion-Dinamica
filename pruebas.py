import sys
from problema_backtracking import problema
import time


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
    mejor_solucion = {
        "board": [[0] * m for _ in range(n)],
        "demanda_insatisfecha": float("inf"),
    }
    barcos = [(i + 1, length) for i, length in enumerate(ships)]
    total_demanda = sum(row_demand) + sum(col_demand)

    print("Filas:", row_demand)
    print("Columnas:", col_demand)
    print("Barcos:", ships)

    init_time = time.time()
    problema(
        board,
        barcos,
        row_demand,
        col_demand,
        mejor_solucion,
    )
    end_time = time.time()

    print("Mejor solución:")
    for row in mejor_solucion["board"]:
        row = " ".join([" -" if x == 0 else f"{x:02}" for x in row])
        print(row)

    demanda_satisfecha = total_demanda - mejor_solucion["demanda_insatisfecha"]

    print(f"Demanda total: {total_demanda}")
    print(f"Demanda cumplida: {demanda_satisfecha}")
    print(f"Demanda insatisfecha: {mejor_solucion['demanda_insatisfecha']}")

    print(f"Tiempo de ejecución: {end_time - init_time:.2f} segundos")


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
            filename = "./test_cases/" + filename
            test(filename)
            print()
    else:
        filename = sys.argv[1]
        filename = "./test_cases/" + filename
        test(filename)
