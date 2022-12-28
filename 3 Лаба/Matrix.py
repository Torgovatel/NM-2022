from __future__ import annotations

"""
Модуль Matrix.py.
Определяет базовую функциональность для реализации поставленной задачи.
"""

import random
from BaseFunctions import *
from typing import List


class Matrix:
    """
    Класс квадратной матрицы.

    Поля:
        n - размерность матрицы.
        a - буфер соответствующего этой матрице вложенного списка.
    """
    def __init__(self, n: int):
        """
        Инициализатор матрицы.
        Создает матрицу размера NxN, заполненную 0.

        Args:
            n: размер создаваемой матрицы.
        """
        self.n = n
        self.a = []
        self.clear(0)

    def clear(self, basic_value=0):
        """
        Метод очистки буфера матрицы (заполняет содержимое переданным элементом).

        Args:
            basic_value: целочисленное значение для заполнения матрицы.
        """
        self.a = [[basic_value for j in range(self.n)] for i in range(self.n)]

    def copy(self) -> Matrix:
        """
        Метод копирования объекта-матрицы.

        Returns:
            возвращает глубокую копию текущего объекта класса Matrix.
        """
        res = Matrix(self.n)
        for i in range(self.n):
            for j in range(self.n):
                res.a[i][j] = self.a[i][j]
        return res

    def read_str(self, string: str):
        """
        Метод заполнения содержимого матрицы строки.

        Args:
            string: строка с элементами для конвертации.
        """
        elems = string.strip().split()
        if len(elems) != self.n ** 2:
            raise ValueError(f"Для записи матрицы было необходимо {self.n**2} значений")
        elem_ind = 0
        for i in range(self.n):
            for j in range(self.n):
                self.a[i][j] = float(elems[elem_ind])
                elem_ind += 1

    def transponent(self) -> Matrix:
        """
        Метод транспонирования матрицы.

        Returns:
            Возвращает новый транспонированный объект типа Matrix.
        """
        T = self.copy()
        for i in range(self.n):
            for j in range(i):
                T.a[i][j], T.a[j][i] = T.a[j][i], T.a[i][j]
        return T

    def generate(self,
                 a: int,
                 b: int,
                 h=None,
                 ah=None,
                 bh=None,
                 hstep=None) -> Tuple[List[float], List[List[float]]]:
        """
        Метод генерации симметричной матрицы с предопределенными собственными значениями.
        Использует алгоритм: A = HhH где H = E - 2T(w)w - матрица Хаусхолдера.

        Args:
            a: целочисленная левая граница генерации вектора w
            b: целочисленная правая граница генерации вектора w
            h: вещественный вектор для заполнения его собственными значениями
            ah: целочисленная левая граница генерации вектора h
            bh: целочисленная правая граница генерации вектора h
            hstep: шаг генерации вектора h

        Returns:
            Возвращает список собственных значений матрицы и список соответствующих им собственных векторов.
        """
        # Заполнение h
        if bh is None:
            bh = self.n + 1
        if ah is None:
            ah = 1
        if hstep is None:
            hstep = (bh - ah) / self.n
        if h is None:
            h = []
        if h == []:
            for k in range(self.n):
                h.append(ah + k * hstep)
        # Генерация
        for i in range(self.n):
            self.a[i][i] = h[i]
        w = [random.randint(a, b + 1) for _ in range(self.n)]
        w = normalize(w)
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
        print(Hshd)
        X = [[Hshd.a[j][i] for j in range(self.n)] for i in range(self.n)]
        return h, X


    def __to_str__(self, arr: List[List[float]]) -> str:
        """
        Метод преобразования матрицы в строку по заданному буферу - вложенному вещественному списку.

        Args:
            arr: вложенный вещественный список (квадратная матрица) для преобразования.

        Returns:
            строку с элементами матрицы, разделенными в грамотной пропорции символами-разделителями.
        """
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


    def __str__(self) -> str:
        """
        Переопределение пользовательского строкового представления.
        Returns:
            строку из исходной матрицы (см. __to_str__).
        """
        return self.__to_str__(self.a)


    def __repr__(self) -> str:
        """
        Переопределение вывода отладочной информации.

        Returns:
            отладочную информацию внутреннего буфера.
        """
        return self.a.__repr__()


    def __mul__(self, x: object) -> object:
        """
        Переопредление оператора умножения в нескольких формах:
            1. Matrix * Matrix
            2. Matrix * int
            3. Matrix * List[float]

        Args:
            x: объект, на который умножается матрица (число, список, или другая матрица).

        Returns:
            Matrix или List[float] в зависимости от переданного значения.
        """
        if type(x) == float:
            res = self.copy()
            for i in range(self.n):
                for j in range(self.n):
                    res.a[i][j] = self.a[i][j]*x
            return res
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
        if len(x) != self.n:
            raise ValueError(f"Размерность вектора должна быть = {self.n}")
        # Перемножаем
        f = [0 for _ in range(self.n)]
        for i in range(self.n):
            for k in range(self.n):
                f[i] += self.a[i][k] * x[k]
        return f
