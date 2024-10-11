import sys
import os
from problema import valor_max_sophia
from reconstruccion import reconstruccion


def tests(file_path, with_reconstruccion=False):
    try:
        with open(file_path, "r") as file:
            first_line = file.readline().strip()
            if first_line.startswith("#"):
                fila = list(int(i) for i in file.readline().strip().split(";") if i)
            else:
                fila = list(int(i) for i in first_line.split(";") if i)

            print(f"Monedas: {fila}")

            dp = valor_max_sophia(fila)

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
    try:
        if len(sys.argv) == 1 or (
            len(sys.argv) == 2 and sys.argv[1] == "--with-reconstruccion"
        ):
            for file_path in os.listdir("test_cases/catedra"):
                print("Leyendo archivo: ", file_path)
                tests(f"test_cases/catedra/{file_path}", True)
        elif len(sys.argv) == 2 and sys.argv[1] != "--with-reconstruccion":
            file_path = sys.argv[1]
            tests(file_path)
        elif len(sys.argv) == 3:
            if sys.argv[1] != "--with-reconstruccion":
                raise Exception("Argumento no reconocido")

            file_path = sys.argv[2]
            tests(file_path, True)
        else:
            raise Exception("Argumentos no reconocidos")

    except:
        print("Uso: python test.py [--with-reconstruccion] [archivo]")
        print("Si no se especifica un archivo, se correrán los tests de la catedra")
