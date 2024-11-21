# TP3

Si se desean agregar casos de prueba, se debe agregar un .txt en la carpeta "test_cases" con el siguiente formato: n filas con las demandas de las filas (cada demanda en un renglón diferente), luego m filas con las demandas de las columnas (cada demanda en un renglón diferente) y luego k filas con el largo de los barcos (cada largo en un renglón diferente), separadas por una línea en blanco.

El resultado se visualizará como una matriz con las demandas, donde los espacios ocupados por barcos se representarán con el índice del barco correspondiente en el vector de largos de los barcos. Esto comenzando desde 1, es decir el primer barco del vector se representará con el número 1, el segundo con un 2, etc.

Para generar automáticamente casos de prueba, ejecutar:

```bash
python3 generate_tests.py n m b
```
Donde n será la cantidad de filas, m la cantidad de columnas, y b la cantidad de barcos.

## Backtracking

Para ejecutar **todas las pruebas de la catedra**, ejecutar (siempre desde el root del repositorio)

```bash
python3 pruebas.py
```

Para ejecutar alguna prueba especifica, dejar el archivo .txt (debe respetar el formato de la catedra) en `./test_cases` y ejecutar

```bash
python3 pruebas.py <nombre del .txt>
```

Por ejemplo, para ejecutar una prueba de `./test_cases/3_3_2.txt`, se debe ejecutar:

```bash
python3 pruebas.py 3_3_2.txt
```

## Aproximación

Para ejecutar el algoritmo de aproximación con alguna de las pruebas, por ejemplo 

`./test_cases/3_3_2.txt`, se debe ejecutar:

```bash
python3 aproximacion.py 3_3_2.txt
```