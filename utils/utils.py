from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import os

# Este parámetro controla cuantas veces se ejecuta el algoritmo para cada
# tamaño. Esto es conveniente para reducir el error estadístico en la medición
# de tiempos. Al finalizar las ejecuciones, se promedian los tiempos obtenidos
RUNS_PER_SIZE = 10

# Ajustar este valor si se quiere usar más de un proceso para medir los tiempos
# de ejecución, o None para usar todos los procesadores disponibles. Si se usan
# varios procesos, tener cuidado con el uso de memoria del sistema.
MAX_WORKERS = (os.cpu_count() or 4) // 4


def _time_run(algorithm, board, barcos, row_demand, col_demand, mejor_solucion):
    start = time.time()
    algorithm(board, barcos, row_demand, col_demand, mejor_solucion)
    return time.time() - start


def time_algorithm(algorithm, sizes, get_args):
    futures = {}
    total_times = {i: 0 for i in sizes}

    # Usa un ProcessPoolExecutor para ejecutar las mediciones en paralelo
    # (el ThreadPoolExecutor no sirve por el GIL de Python)
    with ProcessPoolExecutor(MAX_WORKERS) as p:
        for i in sizes:
            for _ in range(RUNS_PER_SIZE):
                board, barcos, row_demand, col_demand, mejor_solucion = get_args(i)
                print(
                    "Obtained args: ",
                    board,
                    barcos,
                    row_demand,
                    col_demand,
                    mejor_solucion,
                )
                futures[
                    p.submit(
                        _time_run,
                        algorithm,
                        *get_args(i),
                    )
                ] = i

        for f in as_completed(futures):
            result = f.result()
            i = futures[f]
            total_times[i] += result

    return {s: t / RUNS_PER_SIZE for s, t in total_times.items()}
