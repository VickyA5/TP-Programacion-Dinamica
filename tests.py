import os
from problema import valor_max_sophia as problema
from reconstruccion import reconstruccion
import argparse


def tests(file_path, problema, with_reconstruccion=False, with_matrix=False):
    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                fila = list(int(i) for i in file.readline().strip().split(";") if i)
            else:
                fila = list(int(i) for i in first_line.split(";") if i)

            dp = problema(fila)

            valor_sophia = dp[0][len(fila) - 1]
            print(f"Ganancia Sophia: {valor_sophia}")

            valor_mateo = sum(fila) - valor_sophia
            print(f"Ganancia Mateo: {valor_mateo}")

            if with_reconstruccion:
                decisiones = reconstruccion(fila, dp)
                for decision in decisiones:
                    print(decision)

            if with_matrix:
                for row in dp:
                    print(row)

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI tool with options for reconstruction and file path."
    )

    parser.add_argument(
        "--with-reconstruction",
        action="store_true",
        help="Enable reconstruction process.",
    )
    parser.add_argument(
        "--with-matrix", action="store_true", help="Shows the matrix."
    )

    parser.add_argument(
        "file_path",
        nargs="?", 
        type=str,
        default=None,
        help="Optional file path for the operation.",
    )

    args = parser.parse_args()

    implementation = problema

    if args.file_path:
        tests(
            args.file_path,
            implementation,
            args.with_reconstruction,
            args.with_matrix,
        )
    else:
        sorted_files = sorted(os.listdir("test_cases/catedra"), key=lambda x: int(x.split('.')[0]))
        for file in sorted_files:
            file_path = os.path.join("test_cases/catedra", file)
            print(f"File: {file}")
            tests(
                file_path,
                implementation,
                args.with_reconstruction,
                args.with_matrix,
            )
            print()
