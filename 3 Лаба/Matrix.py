"""Модуль Matrix.py определяет специальные методы"""

import random
from typing import List

class Matrix:
    # Инициализатор, с полями:
    # n - размерность матрицы
    # a - буфер с матрицей
    def __init__(self, n: int):
        self.n = n
        self.a = []
        self.clear(0)

    # Заполнение матрицы нулями
    def clear(self, basic_value=0) -> None:
        self.A = [[basic_value for j in range(self.N)] for i in range(self.N)]

    # Конвертация строки в матрицу
    def read_str(self, string: str) -> None:
        elems = string.strip().split()
        if len(elems) != self.N ** 2:
            raise ValueError(f"Для записи матрицы было необходимо {self.N**2} значений")
        elem_ind = 0
        for i in range(self.N):
            for j in range(self.N):
                self.A[i][j] = float(elems[elem_ind])
                elem_ind += 1

    # Преобразование матрицы в строку для вывода по заданному буферу
    def __to_str__(self, arr: List[List[float]]) -> str:
        res = ""
        # Находим максимальную длину строкового представления числа (для форматирования вывода)
        max_length = max([len(str(arr[i][j])) for i in range(self.N) for j in range(self.N)]) + 1
        for i in range(self.N):
            for j in range(self.N):
                elem = arr[i][j]
                s_elem = str(elem)
                if elem >= 0:
                    s_elem = ' ' + s_elem
                res += s_elem.ljust(max_length) + ' '
            res += '\n'
        return res

    # Переопределение строкового представления
    def __str__(self):
        return self.__to_str__(self.A)

    # Переопределение вывода отладочной информации
    def __repr__(self):
        return self.A.__repr__()

    # Переопределение умножения
    def __mul__(self, x):
        if type(x) == Matrix:
            C = Matrix(self.N, self.L)
            for i in range(self.N):
                for j in range(self.N):
                    for k in range(self.N):
                        C.A[i][j] += self.A[i][k] * x.A[k][j]
            return C
        # Проверяем условия когда перемножать нельзя
        if type(x) != list and type(x) != tuple():
            raise TypeError("Умножение возможно только в случае Matrix * tuple/list")
        if len(x) != self.N:
            raise ValueError(f"Размерность вектора должна быть = {self.N}")
        # Перемножаем
        f = [0 for _ in range(self.N)]
        for num in range(self.N):
            f[num] = 0
            for j in range(self.N):
                f[num] += self.A[num][j] * x[j]
        return f

    # Заполнение матрицы случайными числами по заданным параметрам
    def fill_rand(self, a, b, sobst_values=None):
        if sobst_values is None:
            sobst_values = [random.randint(a, b + 1) for _ in range(self.N)]
