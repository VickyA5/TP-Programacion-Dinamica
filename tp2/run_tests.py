import unittest
from problema import ganancia_sophia

class TestProblemaMonedas(unittest.TestCase):
    def leer_archivo(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            valores = list(map(int, lines[1].strip().split(';')))
        return valores
    
    def obtener_resultado_esperado(self, test_name):
        with open('ResultadosEsperados.txt', 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if line.strip().startswith(test_name):
                    while i < len(lines) and not lines[i].startswith("Ganancia Sophia:"):
                        i += 1
                    if i < len(lines):
                        return int(lines[i].split(":")[1].strip())
            return None

    def test_5(self):
        valores = self.leer_archivo('test_cases/catedra/5.txt')
        resultado_esperado = self.obtener_resultado_esperado("5.txt") 
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_10(self):
        valores = self.leer_archivo('test_cases/catedra/10.txt')
        resultado_esperado = self.obtener_resultado_esperado("10.txt") 
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_20(self):
        valores = self.leer_archivo('test_cases/catedra/20.txt')
        resultado_esperado = self.obtener_resultado_esperado("20.txt") 
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_25(self):
        valores = self.leer_archivo('test_cases/catedra/25.txt')
        resultado_esperado = self.obtener_resultado_esperado("25.txt") 
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_50(self):
        valores = self.leer_archivo('test_cases/catedra/50.txt')
        resultado_esperado = self.obtener_resultado_esperado("50.txt") #
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_100(self):
        valores = self.leer_archivo('test_cases/catedra/100.txt')
        resultado_esperado = self.obtener_resultado_esperado("100.txt") #
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_1000(self):
        valores = self.leer_archivo('test_cases/catedra/1000.txt')
        resultado_esperado = self.obtener_resultado_esperado("1000.txt") #
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)
    
    def test_2000(self):
        valores = self.leer_archivo('test_cases/catedra/2000.txt')
        resultado_esperado = self.obtener_resultado_esperado("2000.txt") #
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)
    
    def test_5000(self):
        valores = self.leer_archivo('test_cases/catedra/5000.txt')
        resultado_esperado = self.obtener_resultado_esperado("5000.txt") #
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

    def test_10000(self):
        valores = self.leer_archivo('test_cases/catedra/10000.txt')
        resultado_esperado = self.obtener_resultado_esperado("10000.txt") #
        resultado = ganancia_sophia(valores)
        self.assertEqual(resultado, resultado_esperado)

if __name__ == '__main__':
    unittest.main()