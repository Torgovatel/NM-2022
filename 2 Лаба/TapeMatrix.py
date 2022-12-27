"""Определение класса симметричной ленточной матрицы"""

import random


class TapeMatrix:
    # Инициализатор:
    # N - размерность матрицы
    # L - половина ширины ленты (с учетом главной диагонали)
    # value - значение по умолчанию
    def __init__(self, N, L, value=0):
        self.N = N
        self.L = L
        # A - матрица ленты
        self.A = [[value for j in range(L)] for i in range(N)]

    # Конвертация строки в матрицу
    def from_str(self, str):
        elems = str.strip().split()
        if len(elems) != self.N ** 2:
            raise ValueError(f"Для записи матрицы было необходимо {self.N**2} значений")
        # Обход по столбцам матрицы self.A
        for i in range(self.L):
            for j in range(self.N - i):
                ind = self.N * j + i + j
                self.A[j + i][-1 - i] = float(elems[ind])

    # Получение элемента по индексам с внутреннего буфера
    def get_elem(self, i, j):
        if not(0 <= i < self.N and 0 <= j < self.N):
            raise IndexError("Выход за границы матрицы")
        if abs(i - j) >= self.L:
            return 0
        else:
            if i < j:
                i, j = j, i
            return self.A[i][-1 - i + j]

    # Аналог получения элемента по индексам с внешнего буфера
    @staticmethod
    def gget_elem(arr, i, j, N, L):
        if not(0 <= i < N and 0 <= j < N):
            raise IndexError("Выход за границы матрицы")
        if abs(i - j) >= L:
            return 0
        else:
            if i < j:
                i, j = j, i
            return arr[i][-1 - i + j]

    # Переопределение пользовательского строчного представления (вывода)
    def __str__(self):
        res = ""
        # Находим максимальную длину строкового представления числа (для форматирования вывода)
        max_length = max([len(str(self.A[i][j])) for i in range(self.N) for j in range(self.L)]) + 1
        for i in range(self.N):
            for j in range(self.N):
                elem = self.get_elem(i, j)
                s_elem = str(elem)
                if elem >= 0:
                    s_elem = ' ' + s_elem
                res += s_elem.ljust(max_length) + ' '
            res += '\n'
        return res


    # Переопределение вывода отладочной информации
    def __repr__(self):
        return self.A.__repr__()

    # Переопределение умножения
    def __mul__(self, x):
        if type(x) != list and type(x) != tuple():
            raise TypeError("Умножение возможно только в случае Matrix * tuple/list")
        if len(x) != self.N:
            raise ValueError(f"Размерность вектора должна быть = {self.N}")
        f = [0 for _ in range(self.N)]
        x = [0 for _ in range(self.L - 1)] + x
        for i in range(self.N):
            sum_horizontal = 0
            sum_diagonal = 0
            for j in range(self.L):
                sum_horizontal += self.A[i][j] * x[i+j]
                if i + j < self.N:
                    sum_diagonal += self.A[i+j][-1 - j] * x[i + j + self.L - 1]
            f[i] = sum_diagonal + sum_horizontal - self.A[i][self.L - 1] * x[i + self.L - 1]
        return f

    # Решение системы методом Холецкого
    def sbh(self, f):
        f = f[:]
        # Заполнение матрицы B (обозначим ее в коде как H)
        H = [[0 for _ in range(self.L)] for _ in range(self.N)]
        for ii in range(self.N):
            for jj in range(self.L - 1, -1, -1):
                if ii < jj:
                    continue
                i = ii
                j = i - jj
                a = self.get_elem(i, j)
                sm = 0
                for k in range(j):
                    bik = self.gget_elem(H, i, k, self.N, self.L)
                    bjk = self.gget_elem(H, j, k, self.N, self.L)
                    bkk = self.gget_elem(H, k, k, self.N, self.L)
                    sm += bik * bjk / bkk
                H[ii][-1 - jj] = a - sm
        # Восстановление ответа
        y = [0 for _ in range(self.N)]
        x = [0 for _ in range(self.N)]
        for i in range(self.N):
            sm = 0
            for k in range(i):
                bik = self.gget_elem(H, i, k, self.N, self.L)
                sm += bik * y[k]
            bii = self.gget_elem(H, i, i, self.N, self.L)
            y[i] = (f[i] - sm) / bii

        for i in range(self.N - 1, -1, -1):
            sm = 0
            for k in range(i + 1, self.N):
                bki = self.gget_elem(H, k, i, self.N, self.L)
                bii = self.gget_elem(H, i, i, self.N, self.L)
                sm += bki * x[k] / bii
            x[i] = y[i] - sm
        return x

    # Заполнение матрицы случайными числами по заданным флагам
    def fill_rand(self, a, b, k=None, by_float=False, good=True):
        if k is None:
            k = 2
        if by_float:
            for i in range(self.N):
                for j in range(self.L):
                    if i < j:
                        continue
                    while self.A[i][-1 - j] == 0:
                        self.A[i][-1 - j] = random.uniform(float(a), float(b))
        else:
            for i in range(self.N):
                for j in range(self.L):
                    if i < j:
                        continue
                    while self.A[i][-1 - j] == 0:
                        self.A[i][-1 - j] = random.randint(int(a), int(b) + 1)
        if not good:
            k = 10**k
            for i in range(self.N):
                self.A[i][-1] /= k
