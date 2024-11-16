import sys
from random import randint


def generate_tests(
    n, m, b, row_demand_values=[0, 10], col_demand_values=[0, 10], ships_values=[1, 3]
):
    with open(f"./test_cases/generated_{n}_{m}_{b}.txt", "w") as f:
        for _ in range(n):
            random = randint(row_demand_values[0], row_demand_values[1])
            f.write(f"{random}\n")

        f.write("\n")

        for _ in range(m):
            random = randint(col_demand_values[0], col_demand_values[1])
            f.write(f"{random}\n")

        f.write("\n")

        for _ in range(b):
            random = randint(ships_values[0], ships_values[1])
            f.write(f"{random}\n")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python generate_tests.py n m b")
        sys.exit(1)

    # Parse the arguments
    n = int(sys.argv[1])
    m = int(sys.argv[2])
    b = int(sys.argv[3])

    # Generate the test cases
    generate_tests(n, m, b)
