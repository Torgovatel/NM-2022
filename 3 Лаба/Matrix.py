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
        self.a = [[basic_value for j in range(self.n)] for i in range(self.n)]

    # Конвертация строки в матрицу
    def read_str(self, string: str) -> None:
        elems = string.strip().split()
        if len(elems) != self.n ** 2:
            raise ValueError(f"Для записи матрицы было необходимо {self.n**2} значений")
        elem_ind = 0
        for i in range(self.n):
            for j in range(self.n):
                self.a[i][j] = float(elems[elem_ind])
                elem_ind += 1

    def transponent(self):
        c = Matrix(self.n)
        for i in range(self.n):
            for j in range(self.n):
                c.a[i][j] = self.a[i][j]
        for i in range(self.n):
            for j in range(i):
                c.a[i][j], c.a[j][i] = c.a[j][i], c.a[i][j]
        return c

    def random(self, a, b, h=None, ah=None, bh=None, hstep=None):
        # Заполнение h
        if bh is None:
            bh = b
        if ah is None:
            ah = a
        if hstep is None:
            hstep = (b - a) / self.n
        if h is None:
            h = []
        if h == []:
            for k in range(self.n):
                h.append(ah + k * hstep)
        # Генерация
        for i in range(self.n):
            self.a[i][i] = h[i]
        w = [random.randint(a, b + 1) for _ in range(self.n)]
        w_abs = sum(map(lambda x: x**2, w))**0.5
        w = list(map(lambda x: x / w_abs, w))
        H = [[0 for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    H[i][j] = 1
                H[i][j] -= 2*w[i]*w[j]
        Hshd = Matrix(self.n)
        Hshd.a = H
        HshdT = Hshd.transponent()
        self.a = (Hshd * self * HshdT).a
        print(h)


    # Преобразование матрицы в строку для вывода по заданному буферу
    def __to_str__(self, arr: List[List[float]]) -> str:
        res = ""
        # Находим максимальную длину строкового представления числа (для форматирования вывода)
        max_length = max([len(str(arr[i][j])) for i in range(self.n) for j in range(self.n)]) + 1
        for i in range(self.n):
            for j in range(self.n):
                elem = arr[i][j]
                s_elem = str(elem)
                if elem >= 0:
                    s_elem = ' ' + s_elem
                res += s_elem.ljust(max_length) + ' '
            res += '\n'
        return res

    # Переопределение строкового представления
    def __str__(self):
        return self.__to_str__(self.a)

    # Переопределение вывода отладочной информации
    def __repr__(self):
        return self.a.__repr__()

    # Переопределение умножения
    def __mul__(self, x):
        if type(x) == Matrix:
            if x.n != self.n:
                raise ValueError(f"Несоразмерные матрицы: self.n = {self.n}, x.n = {x.n}")
            res = Matrix(self.n)
            for i in range(self.n):
                for j in range(self.n):
                    for k in range(self.n):
                        res.a[i][j] += self.a[i][k] * x.a[k][j]
            return res
        # Проверяем условия когда перемножать нельзя
        if type(x) != list and type(x) != tuple():
            raise TypeError("Умножение возможно только в случае Matrix * tuple/list")
        if len(x) != self.N:
            raise ValueError(f"Размерность вектора должна быть = {self.N}")
        # Перемножаем
        f = [0 for _ in range(self.n)]
        for i in range(self.N):
            f[i] = self.a[0][i] * f[i]
        return f