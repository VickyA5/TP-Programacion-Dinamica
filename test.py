import os
from problema_top_down import valor_max_sophia as problema_top_down
from problema_bottom_up import valor_max_sophia as problema_bottom_up
from reconstruccion import reconstruccion
import argparse


def tests(file_path, problema, with_reconstruccion=False):
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

    except Exception as e:
        print(f"Error al procesar el archivo {file_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CLI tool with options for reconstruction, bottom-up, top-down and file path."
    )

    # Add optional flags
    parser.add_argument(
        "--with-reconstruction",
        action="store_true",
        help="Enable reconstruction process.",
    )
    parser.add_argument(
        "--bottom-up", action="store_true", help="Enable bottom-up approach."
    )
    parser.add_argument(
        "--top-down", action="store_true", help="Enable top-down approach."
    )

    # Optional positional argument for file path
    parser.add_argument(
        "file_path",
        nargs="?",  # Makes the file_path optional
        type=str,
        default=None,
        help="Optional file path for the operation.",
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.file_path:
        if args.bottom_up:
            print("Bottom-up approach")
            tests(args.file_path, problema_bottom_up, args.with_reconstruction)
        elif args.top_down:
            print("Top-down approach")
            tests(args.file_path, problema_top_down, args.with_reconstruction)
        else:
            print("Bottom-up approach")
            tests(args.file_path, problema_bottom_up, args.with_reconstruction)
    else:
        for file in os.listdir("test_cases/catedra"):
            if file.endswith(".txt"):
                print(f"File: test_cases/catedra/{file}")
                tests(
                    f"test_cases/catedra/{file}",
                    problema_bottom_up,
                    args.with_reconstruction,
                )
                print()
